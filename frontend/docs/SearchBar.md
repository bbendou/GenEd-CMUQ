# Component: `<SearchBar>`

## Purpose

Provides the search and filtering interface for the GenEd course list. Supports input by course code, department selection, and dropdown filters for location and course type (Core/GenEd). State is managed via props and updates are pushed to the parent component.

---
## Instructions
The search bar is located at the top of the page, above the course table. It allows users to refine their search using a combination of inputs and filters for more accurate results.<img width="772" alt="Screenshot 2025-04-19 at 2 44 29 PM" src="https://github.com/user-attachments/assets/15169f1c-df29-42f7-b0b2-2b6ea8c9db78" />

### Course Code Input
Enter a full or partial course code (e.g., 76-101, 101, or 76 101) to search for specific courses by number. The course code will appear as a removable tag once searched.

### Department Dropdown
Choose a department to filter courses offered by that department. Select one or multiple departments and click on the *Apply Filters* button. The selected departments will appear as a removable tag once applied. <br>
<img width="260" alt="Screenshot 2025-04-19 at 2 38 50 PM" src="https://github.com/user-attachments/assets/bbb4f12c-8f81-4475-8a20-2da1dc244633" />

### Location Checkboxes
Toggle the "Qatar" and "Pittsburgh" checkboxes and click on the *Apply Filters* button to filter courses based on the campus where they are offered. <br>
<img width="260" alt="Screenshot 2025-04-19 at 2 38 39 PM" src="https://github.com/user-attachments/assets/36038913-b58b-4324-9e13-a7a4d0a2d7f5" />

### Course Type Checkboxes:
Use the "Core" and "GenEd" checkboxes and click on the *Apply Filters* button to limit the results based on the type of requirement a course fulfills. <br>
<img width="262" alt="Screenshot 2025-04-19 at 2 38 30 PM" src="https://github.com/user-attachments/assets/35288bc9-8e90-4bff-a709-254dd80f7424" />

--- 

## Props

| Prop Name          | Type     | Required | Description |
|--------------------|----------|----------|-------------|
| `selectedDepartments` | Array  | ✅       | Selected department codes |
| `setSelectedDepartments` | Function | ✅ | Updates department filters |
| `searchQuery`      | String   | ✅       | Input value for course code search |
| `setSearchQuery`   | Function | ✅       | Updates course code query |
| `noPrereqs`        | Boolean/null | ✅   | Current prerequisite filter |
| `setNoPrereqs`     | Function | ✅       | Updates pre-requisite filter |
| `offeredQatar`     | Boolean/null | ✅   | Filter for Qatar campus |
| `setOfferedQatar`  | Function | ✅       | Updates Qatar location filter |
| `offeredPitts`     | Boolean/null | ✅   | Filter for Pittsburgh campus |
| `setOfferedPitts`  | Function | ✅       | Updates Pittsburgh location filter |
| `coreOnly`         | Boolean/null | ✅   | Core-only course filter |
| `setCoreOnly`      | Function | ✅       | Setter for Core filter |
| `genedOnly`        | Boolean/null | ✅   | GenEd-only course filter |
| `setGenedOnly`     | Function | ✅       | Setter for GenEd filter |

---

## Logic Overview

- Uses `useEffect` to fetch department list from the backend.
- Default selection sets Core and GenEd to `true` if unset.
- Formats course codes via `formatCourseCode()` utility.
- Handles user interaction:
  - Search by course code (supports 15122 or 15-122)
  - Multi-select dropdowns for departments, campus, and course type
  - Clear buttons for individual filters

---

## Related Components

- `<MultiSelectDropdown />` — reused for department, location, and course type

---


---

## Example Usage

```jsx
<SearchBar
  selectedDepartments={selectedDepartments}
  setSelectedDepartments={setSelectedDepartments}
  searchQuery={searchQuery}
  setSearchQuery={setSearchQuery}
  noPrereqs={noPrereqs}
  setNoPrereqs={setNoPrereqs}
  offeredQatar={offeredQatar}
  setOfferedQatar={setOfferedQatar}
  offeredPitts={offeredPitts}
  setOfferedPitts={setOfferedPitts}
  coreOnly={coreOnly}
  setCoreOnly={setCoreOnly}
  genedOnly={genedOnly}
  setGenedOnly={setGenedOnly}
/>
```

Used at the top of the course listing page to allow users to search and filter courses based on department, code, prerequisites, and location.


## Related Tests

- `SearchBar.test.js` – tests for:
  - Department and location dropdown rendering
  - Search field updates
  - Filter tags and removal logic

---

## Styling

| Class | Description |
|-------|-------------|
| `search-container` | Wrapper for the entire component |
| `search-header-row`, `search-content-row` | Organize layout into rows |
| `filter-group`, `filter-label` | Style each dropdown group |
| `text-input` | Style for the course code input field |
| `selected-filters`, `filter-tag` | Style for filter display and remove buttons |

---

## Notes

- The search is not manually triggered — it uses state change and `useEffect` in the parent.
- Enter key behavior is managed to blur the input but not submit anything.
- All dropdown filters support clearing and partial selection.
