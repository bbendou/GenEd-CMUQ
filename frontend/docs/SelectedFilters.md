# Component: `<SelectedFilters>`

## Purpose

Displays all currently applied filters (semesters, prerequisites, and requirement filters) as removable tags. Dynamically groups requirement tags by fully-selected groups and formats them visually. It provides a quick summary of the current filtering criteria.

---
## Instructions
The selected filters section appears just above the course table and displays all active filters applied through the dropdowns or search bar. There are different types:
- Requirement Filters: Each selected requirement appears as a colored tag based on the associated major (e.g., CS, IS, BA, BS). These tags show a shortened version of the requirement path,  displaying only the last two levels for clarity.
- Offered Semester Filters: Selected semesters (e.g., F24, S25) are displayed as gray tags. These reflect your choices from the "Offered" dropdown column in the table header.
- Pre-req Filters: If you selected "No-Pre Reqs" or "Only with Pre-Req"s in the pre-req column, these will be displayed as gray tags.

These filters will appear on the search bar section:
- Department dropdown
- Course code input <br>
They will appear as tags directly below the search bar. These appear as black and indicate the current department and course being searched.

<br>
To remove these filters: click the × button on any tag to remove that specific filter. The course table will update immediately to reflect the change. <br>
<img width="424" alt="Screenshot 2025-04-19 at 2 38 09 PM" src="https://github.com/user-attachments/assets/30753490-c19e-4e55-932e-ff14d935ba35" />


---

## Props

| Prop Name                  | Type     | Required | Description |
|----------------------------|----------|----------|-------------|
| `selectedFilters`          | Object   | ✅       | Object of selected requirement filters by major |
| `handleFilterChange`       | Function | ✅       | Callback to update requirement filters |
| `selectedOfferedSemesters` | Array    | ✅       | List of selected semester filters |
| `removeOfferedSemester`    | Function | ✅       | Callback to remove a selected semester |
| `noPrereqs`                | Boolean/null | ✅   | Current state of the prerequisite filter |
| `removePrereqFilter`       | Function | ✅       | Callback to reset the pre-requisite filter |
| `allRequirements`          | Object   | ✅       | Full list of all requirement options, grouped by major |

---

## Logic Overview

- Uses `useMemo()` to build a nested tree of requirement groupings from `allRequirements`.
- Displays:
  - Semester tags
  - Prerequisite filter tag
  - Fully selected requirement groups (e.g., "All Analytical Reasoning Requirements")
  - Individual requirement filters
- Group tags can be removed as a batch. Individual filters can be removed independently.

---

## Example Usage

```jsx
<SelectedFilters
  selectedFilters={selectedFilters}
  handleFilterChange={handleFilterChange}
  selectedOfferedSemesters={selectedOfferedSemesters}
  removeOfferedSemester={removeOfferedSemester}
  noPrereqs={noPrereqs}
  removePrereqFilter={removePrereqFilter}
  allRequirements={requirements}
/>
```

Use this component underneath the search bar to show users which filters are active and let them remove individual or grouped filters.

---

## Related Components

- Used in conjunction with `<CourseTablePage>` and `<SearchBar>`

---

## Related Tests

- `SelectedFilters.test.js` — tests:
  - Displaying correct tags
  - Clicking × removes individual and grouped filters
  - Conditional rendering

---

## Styling

| Class | Description |
|-------|-------------|
| `selected-filters` | Main container for all tags |
| `filter-tag`       | Individual tag element |
| `filter-tag button` | Remove (×) button styling |

---

## 🚨 Notes

- Group tags are automatically detected if all values in that group are selected.
- Ensures consistent formatting by trimming the last two parts of the requirement hierarchy (e.g., `GenEd → Foundations → Scientific Reasoning` → `Foundations → Scientific Reasoning`).
