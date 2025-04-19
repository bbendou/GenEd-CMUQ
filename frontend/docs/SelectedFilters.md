# Component: `<SelectedFilters>`

## 📌 Purpose

Displays all currently applied filters (semesters, prerequisites, and requirement filters) as removable tags. Dynamically groups requirement tags by fully-selected groups and formats them visually.

---

## 🔧 Props

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

## 🧠 Logic Overview

- Uses `useMemo()` to build a nested tree of requirement groupings from `allRequirements`.
- Displays:
  - Semester tags
  - Prerequisite filter tag
  - Fully selected requirement groups (e.g., "All Analytical Reasoning Requirements")
  - Individual requirement filters
- Group tags can be removed as a batch. Individual filters can be removed independently.

---

## 📤 Example Usage

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

## 🧱 Related Components

- Used in conjunction with `<CourseTablePage>` and `<SearchBar>`

---

## 🧪 Related Tests

- `SelectedFilters.test.js` — tests:
  - Displaying correct tags
  - Clicking × removes individual and grouped filters
  - Conditional rendering

---

## 🎨 Styling

| Class | Description |
|-------|-------------|
| `selected-filters` | Main container for all tags |
| `filter-tag`       | Individual tag element |
| `filter-tag button` | Remove (×) button styling |

---

## 🚨 Notes

- Group tags are automatically detected if all values in that group are selected.
- Ensures consistent formatting by trimming the last two parts of the requirement hierarchy (e.g., `GenEd → Foundations → Scientific Reasoning` → `Foundations → Scientific Reasoning`).
