# Design Principles

## The Universal Interface Pattern

### Historical Precedent

| Product | Interface | Polymorphic Behavior |
|---------|-----------|---------------------|
| Google Search (1998) | One text box | Web, images, maps, calculator, weather, flights... |
| iPhone (2007) | Touch screen + apps | Everything via same gesture model |
| ChatGPT (2022) | One text input | Code, writing, analysis, roleplay, tutoring... |

**The insight**: As AI capability increases, UI complexity should decrease.

### Implementation Guidelines

**Single Entry Point**
```
Good: One prominent input field, full-width, centered
Bad: Dashboard with 12 widgets, sidebar with 8 menu items
```

**Intelligent Defaults**
```
Good: Auto-detect file type, infer intent, pre-fill likely values
Bad: Ask user to select category, mode, format before proceeding
```

**Progressive Disclosure**
```
Good: Show result first, offer "refine" options on demand
Bad: Require all parameters upfront before showing anything
```

## The Deletion Test

For every UI element, ask:

1. **What happens if we remove this?**
   - If nothing breaks → Remove it
   - If edge case breaks → Consider if edge case matters

2. **Who asked for this?**
   - If no one → Remove it
   - If one person → Question if it's truly necessary

3. **Can AI handle this instead?**
   - If yes → Let AI handle it, remove the UI

## The 30-Second Test

A new user with no training should be able to:
- Understand what the product does (5 seconds)
- Know where to start (5 seconds)
- Complete a basic task (20 seconds)

If this fails, the design is too complex.

## Joy as a Metric

Enterprise software has historically optimized for:
- Feature completeness
- Checkbox compliance
- Power user workflows

Forth AI optimizes for:
- Time to value
- Emotional response
- Return usage

**Practical joy indicators:**
- User smiles or says "nice" or "cool"
- User shows the product to someone else
- User completes task faster than expected
- User returns without being forced to

## Anti-Patterns to Avoid

### Feature-Soup Dashboard
Multiple widgets competing for attention. User doesn't know where to look.
**Fix**: One primary action, everything else secondary or hidden.

### Wizard Workflows
Multi-step forms that could be single-step with smart defaults.
**Fix**: Infer steps, allow override if wrong.

### Settings Graveyards
Dozens of configuration options that 95% of users never touch.
**Fix**: Opinionated defaults, AI-driven customization.

### Mode-Switching
Explicit "create mode" vs "edit mode" vs "view mode".
**Fix**: Context-aware interface that adapts automatically.

### Confirmation Dialogs
"Are you sure?" for every action.
**Fix**: Undo instead of confirm. Trust the user.
