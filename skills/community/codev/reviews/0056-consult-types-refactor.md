# Review: Spec 0056 - Consult Types Refactor

## Summary

Relocated consult review types from `codev/roles/review-types/` to `codev/consult-types/` with backward compatibility fallback and migration tooling.

## Changes Made

### Core Implementation

1. **New directory structure** (`codev-skeleton/consult-types/`)
   - `spec-review.md` - Specification review prompt
   - `plan-review.md` - Plan review prompt
   - `impl-review.md` - Implementation review prompt
   - `pr-ready.md` - Pre-PR self-check prompt
   - `integration-review.md` - Architect integration review prompt

2. **Consult CLI updates** (`packages/codev/src/commands/consult/index.ts`)
   - Updated `loadReviewTypePrompt()` to check `consult-types/` first
   - Added fallback to `roles/review-types/` with deprecation warning
   - Deprecation warning uses `console.error` with yellow chalk coloring

3. **Doctor command updates** (`packages/codev/src/commands/doctor.ts`)
   - Added `findProjectRoot()` helper function
   - Added `checkCodevStructure()` to verify project configuration
   - New "Codev Structure" section in doctor output
   - Warns if `consult-types/` directory is missing
   - Warns if deprecated `roles/review-types/` still exists

4. **Local project migration** (`codev/consult-types/`)
   - Moved review types from `codev/roles/review-types/`
   - Deleted old `roles/review-types/` directory

5. **Documentation updates**
   - `CLAUDE.md` - Updated Review Types section with new path and migration note
   - `AGENTS.md` - Same updates as CLAUDE.md

### Test Coverage

1. **Consult tests** (`packages/codev/src/__tests__/consult.test.ts`)
   - Test loading from primary location (`consult-types/`)
   - Test fallback to deprecated location (`roles/review-types/`)
   - Test preference of new location over old when both exist
   - Test fallback to embedded skeleton when not in local directories

2. **Doctor tests** (`packages/codev/src/__tests__/doctor.test.ts`)
   - Test warning when `consult-types/` directory is missing
   - Test warning when deprecated `roles/review-types/` still exists
   - Test "Project structure OK" when properly migrated

## Acceptance Criteria Verification

| Criterion | Status |
|-----------|--------|
| `consult --type spec-review` reads from `consult-types/` | PASS |
| Users can add custom types in `consult-types/` | PASS |
| Skeleton contains `consult-types/` directory | PASS |
| Documentation reflects new location | PASS |
| `codev doctor` warns if `consult-types/` missing | PASS |
| `codev doctor` warns if `roles/review-types/` exists | PASS |
| Fallback to old location with warning | PASS |

## Test Results

```
Test Files  20 passed (20)
Tests       248 passed (248)
```

All tests pass including 8 new tests for Spec 0056 functionality (5 consult, 3 doctor).

## External Consultation Results

### Gemini Review (APPROVE with feedback addressed)

**Initial Findings:**
- Looked for tests in `tests/e2e/` (incorrect location)
- Tests are in `packages/codev/src/__tests__/` using vitest

**Status:** Tests exist and are comprehensive. Gemini's feedback was based on incorrect file location assumption.

### Codex Review (REQUEST_CHANGES - addressed)

**Valid Feedback:**
1. Command documentation (`codev/docs/commands/consult.md`) missing new location - **FIXED**
2. Tests don't directly test `loadReviewTypePrompt` deprecation warning - **FIXED**

**Fixes Applied:**
- Updated `codev/docs/commands/consult.md` and `codev-skeleton/docs/commands/consult.md` with location and migration note
- Added test for deprecation warning behavior
- Improved `loadReviewTypePrompt` to properly distinguish local vs skeleton lookups using `hasLocalOverride`
- Fixed dry-run mode to skip CLI existence check (enables testing without CLIs installed)

## Lessons Learned

1. **Path fallback patterns**: The `readCodevFile` helper already provides local-then-skeleton fallback, but for deprecation warnings we need explicit path checking in the consumer code.

2. **Test isolation**: Doctor tests require careful mocking of `execSync` and `spawnSync` since they check for installed tools. Using a temp directory with proper setup/teardown ensures tests don't interfere.

3. **Skeleton sync**: Always run `npm run copy-skeleton` after modifying `codev-skeleton/` to keep the build artifact in sync.

## Files Changed

| File | Changes |
|------|---------|
| `codev-skeleton/consult-types/*.md` | Created (moved from review-types) |
| `codev-skeleton/roles/review-types/` | Deleted |
| `codev-skeleton/docs/commands/consult.md` | Added location info |
| `codev/consult-types/*.md` | Created (moved from review-types) |
| `codev/roles/review-types/` | Deleted |
| `codev/docs/commands/consult.md` | Added migration note |
| `packages/codev/src/commands/consult/index.ts` | Updated path lookup with fallback, import hasLocalOverride |
| `packages/codev/src/commands/doctor.ts` | Added structure checks |
| `packages/codev/src/__tests__/consult.test.ts` | Added 5 tests |
| `packages/codev/src/__tests__/doctor.test.ts` | Added 3 tests |
| `CLAUDE.md` | Updated Review Types section |
| `AGENTS.md` | Updated Review Types section |
