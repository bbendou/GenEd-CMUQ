# Component: `<CategoryCoverage>`

## Purpose

Displays a bar chart showing how many courses fulfill each requirement category for a selected major and semester. Uses Plotly for charting and dynamically fetches data from the backend via `/analytics/course-coverage`.

---

## Props

| Prop Name         | Type     | Required | Description |
|-------------------|----------|----------|-------------|
| `selectedMajor`   | String   | ✅       | The major currently selected (e.g., "CS") |
| `setSelectedMajor`| Function | ✅       | Updates the selected major |
| `majors`          | Object   | ✅       | Dictionary of major codes to names (e.g., `{ CS: "Computer Science" }`) |

---

## Logic Overview

- Fetches available semesters with data for the selected major
- Fetches requirement coverage data for the selected major + semester
- Aggregates the number of courses per requirement (based on the last node in path)
- Uses Plotly to render a horizontal bar chart, sorted by course count
- Dynamically switches content based on data availability and loading state

---

## Example Usage

```jsx
<CategoryCoverage
  selectedMajor={selectedMajor}
  setSelectedMajor={setSelectedMajor}
  majors={{ CS: "Computer Science", IS: "Information Systems" }}
/>
```

Used in the **Analytics** page to let users visually explore course distribution across requirement categories. You can change the major and limit by semester.

---

## Related Tests

- `CategoryCoverage.test.js` — test coverage includes:
  - Valid/invalid API responses
  - Dropdown behavior
  - Chart rendering based on dynamic data
  - Conditional “No Data” message

---

## Styling

| Class | Description |
|-------|-------------|
| `search-container` | Wrapper layout |
| `filter-control-group` | Wrapper for dropdowns |
| `search-dropdown` | Select element styling |
| `loading-spinner` | Visual feedback during API load |
| `filter-tag` | Display fallback “no data” status |

---

## Notes

- Filters out requirement categories with `num_courses === 0` to reduce noise
- Responsive to container size (`useResizeHandler`)
- Resets semester when major is changed
- Requires the backend endpoint:  
  `GET /analytics/course-coverage?major=CS&semester=F23`

