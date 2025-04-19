# Component: `<CourseTablePage>`

## Purpose

Acts as the main page controller for the CMU-Q GenEd frontend. Manages the UI state, filter logic, search behavior, course retrieval, and rendering of child components such as the search bar, table, and popups.

---

## Internal State

- `selectedDepartments`, `searchQuery`, `noPrereqs`, `coreOnly`, `genedOnly`, etc.: Manage user-selected filters
- `courses`, `requirements`: Store data fetched from backend
- `offeredOptions`: Populates semester dropdowns
- `sortMode`: Toggles between sorting by course code or requirements
- `compactViewMode`: Controls the display format of requirement text
- `toast`, `loading`, `showConfirmPopup`, `showClearPopup`: UI feedback and modals

---

## API Calls

- `/departments`: Fetch list of departments for dropdown
- `/requirements`: Fetch course requirement data
- `/courses/search`: Fetch filtered list of courses
- `/courses/semesters`: Get available semesters

All filters and search values are sent as query parameters.

---

## Lifecycle Effects

- `useEffect` saves user preferences to `localStorage` for persistence
- Search query is debounced using a `setTimeout` (350ms delay)
- Courses and requirements are re-fetched when filters change
- Paginated display updates when data length or page changes

---

## Handlers

| Handler | Purpose |
|---------|---------|
| `handleFilterChange` | Updates selected filters by major |
| `clearFilters` | Clears all filters for a major |
| `removeOfferedSemester` | Removes a selected semester |
| `removePrereqFilter` | Resets the pre-req filter to null |
| `handleRemoveCourse` | Removes a course from the local course list |
| `addCoursesToPlan` | Saves selected courses to localStorage |
| `toggleSortByReqs` | Toggles between sorting modes |
| `clearAllFilters` | Resets all filters to their defaults |

---

## Child Components

- `<SearchBar />`
- `<SelectedFilters />`
- `<CourseTable />`
- Toast and popup components for UI interaction

---

## Related Tests

- `CourseTablePage.test.js` – covers filter state logic, fetch behavior, and UI interaction
- Mocks localStorage and API calls for isolation

---

## Styling

| Class | Description |
|-------|-------------|
| `table-container` | Main container layout |
| `view-toolbar` | Toolbar with filters, sort and plan buttons |
| `toast-snackbar` | Small floating message box |
| `popup-overlay-2`, `popup-box` | Modal styles for confirmation dialogs |
| `no-results-msg` | Display when no matching courses |

---

## Notes

- Uses `AbortController` to cancel pending API fetches and avoid race conditions.
- Stores filter state in `localStorage` for persistence across page reloads.
- Modular design supports adding new filters or sorting methods with minimal refactoring.
