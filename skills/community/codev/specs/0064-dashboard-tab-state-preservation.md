# Spec 0064: Dashboard Tab State Preservation

## Problem Statement

When switching between tabs in the Agent Farm dashboard, annotation/editor tabs lose their state:
- Scroll position resets to the top
- Edit mode reverts to annotation mode
- Cursor position is lost
- Any in-progress edits are discarded

This happens because the dashboard destroys and recreates iframes when switching tabs, rather than hiding/showing them.

## Current Behavior

In `tabs.js`, `renderTabContent()` replaces the iframe HTML whenever the tab changes:

```javascript
if (currentTabPort !== tab.port || currentTabType !== tab.type) {
  content.innerHTML = `<iframe src="${url}" ...></iframe>`;
}
```

This destroys the previous iframe and all its state.

## Proposed Solution

### Keep All Iframes Alive

Instead of destroying iframes on tab switch, keep them all alive and use hide/show:

1. **Create iframe on first access** - When a tab is selected for the first time, create its iframe
2. **Hide/show instead of destroy** - When switching tabs, hide current iframe and show target
3. **Remove only on explicit close** - Iframe is destroyed only when user closes the tab

No LRU eviction or cache limits - modern browsers handle multiple iframes fine, and typical usage is 5-10 tabs.

### Implementation

#### HTML Structure

```html
<div id="tab-content">
  <!-- Iframes are created dynamically and hidden/shown -->
  <iframe id="tab-iframe-file-abc123" class="tab-iframe" src="..." style="display: none"></iframe>
  <iframe id="tab-iframe-builder-0055" class="tab-iframe" src="..." style="display: block"></iframe>
</div>
```

#### Tab Content Management

```javascript
const iframeCache = new Map(); // tabId -> { iframe, port }

function renderTabContent() {
  const tab = tabs.find(t => t.id === activeTabId);
  if (!tab) return;

  // Hide all iframes
  document.querySelectorAll('.tab-iframe').forEach(iframe => {
    iframe.style.display = 'none';
  });

  // Handle inline tabs (dashboard, activity)
  if (tab.type === 'dashboard' || tab.type === 'activity') {
    renderInlineTab(tab);
    return;
  }

  // Get or create iframe for this tab
  let cached = iframeCache.get(tab.id);
  if (cached) {
    cached.iframe.style.display = 'block';
  } else {
    // Create new iframe
    const iframe = createIframe(tab);
    iframeCache.set(tab.id, { iframe, port: tab.port });
    document.getElementById('tab-content').appendChild(iframe);
  }
}
```

### Handling Tab Closure

When a tab is closed, remove its iframe:

```javascript
function closeTab(tabId) {
  // ... existing close logic ...

  // Remove iframe
  const cached = iframeCache.get(tabId);
  if (cached) {
    cached.iframe.remove();
    iframeCache.delete(tabId);
  }
}
```

### Handling Port Changes

If a tab's port changes (e.g., builder restarts), the cached iframe must be invalidated:

```javascript
function buildTabsFromState() {
  // ... existing logic ...

  // Invalidate cached iframes if port changed
  for (const tab of tabs) {
    const cached = iframeCache.get(tab.id);
    if (cached && cached.port !== tab.port) {
      cached.iframe.remove();
      iframeCache.delete(tab.id);
    }
  }
}
```

## Acceptance Criteria

1. **State preserved on tab switch**: Switching away from an annotation tab and back preserves:
   - Scroll position
   - Edit mode vs annotation mode
   - Cursor position in editor
   - Unsaved changes indicator

2. **Tab close cleans up**: Closing a tab removes its iframe

3. **Port change invalidates**: If a tab's underlying service restarts on a new port, iframe is refreshed

4. **No visual flicker**: Tab switching should be instant (no loading spinner)

## Non-Goals

- Persisting state across page refresh (that would require localStorage)
- Persisting state across dashboard restart
- Terminal tab state preservation (xterm.js handles its own state)

## Testing

1. Open an annotation tab, scroll down, switch to another tab, switch back - scroll position preserved
2. Open annotation tab, enter edit mode, switch tabs, switch back - still in edit mode
3. Close a tab, verify iframe is cleaned up (check DOM)
4. Restart a builder, verify its iframe refreshes

## Files to Modify

- `packages/codev/templates/dashboard/js/tabs.js` - Main implementation
- `packages/codev/templates/dashboard/css/layout.css` - Iframe positioning styles

## Estimated Complexity

Low - Simple hide/show logic with cleanup on close and port change.
