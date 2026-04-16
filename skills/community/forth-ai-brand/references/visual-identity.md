# Visual Identity

## Color Palette

### Primary Colors

| Name | Hex | RGB | Usage |
|------|-----|-----|-------|
| **Forth Blue** | `#0066FF` | 0, 102, 255 | Primary actions, links, key UI elements |
| **Forth Orange** | `#FF6600` | 255, 102, 0 | Accent, CTAs, emphasis, energy |

### Neutral Colors

| Name | Hex | Usage |
|------|-----|-------|
| **Black** | `#0A0A0A` | Primary text, dark backgrounds |
| **Dark Gray** | `#404040` | Secondary text |
| **Medium Gray** | `#737373` | Tertiary text, borders |
| **Light Gray** | `#E5E5E5` | Subtle borders, dividers |
| **Off-White** | `#FAFAFA` | Backgrounds, cards |
| **White** | `#FFFFFF` | Primary background |

### Semantic Colors

| Name | Hex | Usage |
|------|-----|-------|
| **Success** | `#22C55E` | Positive states, confirmations |
| **Error** | `#EF4444` | Errors, destructive actions |
| **Warning** | `#F59E0B` | Cautions, alerts |
| **Info** | `#3B82F6` | Informational, tips |

### Tailwind Config

```javascript
colors: {
  forth: {
    blue: '#0066FF',
    orange: '#FF6600',
  },
  neutral: {
    950: '#0A0A0A',
    800: '#404040',
    500: '#737373',
    200: '#E5E5E5',
    50: '#FAFAFA',
  }
}
```

## Typography

### Font Stack

| Role | Font | Fallback | Weight |
|------|------|----------|--------|
| **Display/Headers** | Playfair Display | Georgia, serif | 600-700 |
| **Body** | Lora | Georgia, serif | 400 |
| **UI/Labels** | Bricolage Grotesque | system-ui, sans-serif | 500 |
| **Code** | JetBrains Mono | monospace | 400 |

### Type Scale

| Element | Size | Line Height | Weight |
|---------|------|-------------|--------|
| h1 | 48px / 3rem | 1.1 | 700 |
| h2 | 36px / 2.25rem | 1.2 | 600 |
| h3 | 24px / 1.5rem | 1.3 | 600 |
| h4 | 20px / 1.25rem | 1.4 | 600 |
| Body | 16px / 1rem | 1.6 | 400 |
| Small | 14px / 0.875rem | 1.5 | 400 |
| Caption | 12px / 0.75rem | 1.4 | 400 |

### Tailwind Config

```javascript
fontFamily: {
  display: ['Playfair Display', 'Georgia', 'serif'],
  body: ['Lora', 'Georgia', 'serif'],
  ui: ['Bricolage Grotesque', 'system-ui', 'sans-serif'],
  mono: ['JetBrains Mono', 'monospace'],
}
```

## Spacing

Use Tailwind's default spacing scale. Key values:
- `p-4` / `m-4` (16px) — Standard padding
- `p-6` / `m-6` (24px) — Section padding
- `gap-4` (16px) — Standard gap
- `space-y-6` (24px) — Section spacing

## Border Radius

| Element | Value | Tailwind |
|---------|-------|----------|
| Buttons | 8px | `rounded-lg` |
| Cards | 12px | `rounded-xl` |
| Inputs | 8px | `rounded-lg` |
| Modals | 16px | `rounded-2xl` |
| Pills/Tags | 9999px | `rounded-full` |

## Shadows

Use sparingly. Prefer borders or background color differentiation.

| Use Case | Tailwind |
|----------|----------|
| Cards (hover) | `shadow-lg` |
| Dropdowns | `shadow-xl` |
| Modals | `shadow-2xl` |

## Contrast Requirements

All text must meet WCAG 2.1 AA:
- Normal text: 4.5:1 minimum
- Large text (18px+): 3:1 minimum
- UI components: 3:1 minimum

**Verified combinations:**
- `#0A0A0A` on `#FFFFFF` → 19.4:1 ✓
- `#0066FF` on `#FFFFFF` → 4.5:1 ✓
- `#FFFFFF` on `#0066FF` → 4.5:1 ✓
- `#FF6600` on `#0A0A0A` → 4.8:1 ✓

## Avoid

- Inter, Roboto, Open Sans (generic AI look)
- Purple gradients on white (AI cliché)
- Rounded rectangles with drop shadows everywhere
- Pastel color schemes
- Excessive whitespace without purpose
