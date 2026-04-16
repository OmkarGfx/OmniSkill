# Tech Stack

## Required Technologies

| Technology | Version | Purpose |
|------------|---------|---------|
| **React** | 19 | Component architecture |
| **RTK Query** | 2.10 | Data fetching, caching, state |
| **Tailwind CSS** | 4.1 | Utility-first styling |
| **Vite** | 7.2.2 | Build tooling, dev server |

## Project Setup

### Package.json Dependencies

```json
{
  "dependencies": {
    "react": "^19.0.0",
    "react-dom": "^19.0.0",
    "@reduxjs/toolkit": "^2.10.0"
  },
  "devDependencies": {
    "vite": "^7.2.2",
    "@vitejs/plugin-react": "^4.0.0",
    "tailwindcss": "^4.1.0",
    "autoprefixer": "^10.4.0",
    "postcss": "^8.4.0"
  }
}
```

### Vite Config

```typescript
// vite.config.ts
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  css: {
    postcss: './postcss.config.js'
  }
})
```

### Tailwind Config

```javascript
// tailwind.config.js
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        forth: {
          blue: '#0066FF',
          orange: '#FF6600',
        }
      },
      fontFamily: {
        display: ['Playfair Display', 'Georgia', 'serif'],
        body: ['Lora', 'Georgia', 'serif'],
        ui: ['Bricolage Grotesque', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace'],
      }
    }
  },
  plugins: []
}
```

## RTK Query Setup

```typescript
// src/store/api.ts
import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react'

export const api = createApi({
  reducerPath: 'api',
  baseQuery: fetchBaseQuery({ baseUrl: '/api' }),
  endpoints: (builder) => ({
    // Define endpoints here
  }),
})
```

```typescript
// src/store/store.ts
import { configureStore } from '@reduxjs/toolkit'
import { api } from './api'

export const store = configureStore({
  reducer: {
    [api.reducerPath]: api.reducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware().concat(api.middleware),
})
```

## Component Patterns

### Functional Components Only

```tsx
// Good
export function Button({ children, onClick }: ButtonProps) {
  return (
    <button
      onClick={onClick}
      className="bg-forth-blue text-white px-4 py-2 rounded-lg font-ui"
    >
      {children}
    </button>
  )
}

// Avoid: Class components, HOCs, render props (unless necessary)
```

### Hooks for State

```tsx
// Local state
const [value, setValue] = useState('')

// Server state (RTK Query)
const { data, isLoading } = useGetDataQuery()

// Avoid: Redux for local UI state, prop drilling beyond 2 levels
```

### Tailwind for Styling

```tsx
// Good: Utility classes
<div className="flex items-center gap-4 p-6 bg-white rounded-xl">

// Avoid: Inline styles, CSS modules, styled-components
```

## File Structure

```
src/
├── components/       # Reusable UI components
│   ├── Button.tsx
│   ├── Input.tsx
│   └── Card.tsx
├── features/         # Feature-specific components
│   └── chat/
│       ├── ChatInput.tsx
│       └── ChatMessage.tsx
├── store/            # Redux/RTK Query setup
│   ├── store.ts
│   └── api.ts
├── hooks/            # Custom hooks
├── utils/            # Helper functions
├── App.tsx
└── main.tsx
```

## Performance Guidelines

- Lazy load routes and heavy components
- Use `React.memo` only when profiler shows re-render issues
- RTK Query handles caching; don't duplicate
- Images: Use WebP, lazy load below fold
- Target: 90+ Lighthouse performance score

## Accessibility Requirements

- All interactive elements keyboard accessible
- ARIA labels on icon-only buttons
- Focus indicators visible
- Skip links for main content
- Semantic HTML (nav, main, article, etc.)
- Color not sole indicator of state
