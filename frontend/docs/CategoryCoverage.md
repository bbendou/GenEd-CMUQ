# Component: `<CategoryCoverage>`

## Purpose

Displays a bar chart showing how many courses fulfill each requirement category for a selected major and semester. Uses Plotly for charting and dynamically fetches data from the backend via `/analytics/course-coverage`.

---
## Instructions
1. On the top of the page, select the *Analytics* tab.
2. Locate the *Category Coverage* section.
3. Click on the *Major* dropdown to select a major. This will display all the Core and Gen-Ed requirements on the graph, listed on the Y-axis. <br>
   <img width="200" alt="Screenshot 2025-04-19 at 1 11 48 PM" src="https://github.com/user-attachments/assets/471af2c3-429a-4856-8763-53d50974afdd" />

5. Click on the *Semester* dropdown to select a specific semester. This will update the graph to show the total count of how many courses satisfy each requirement category for your chosen major and semester. <br>
   <img width="100" alt="Screenshot 2025-04-19 at 1 12 00 PM" src="https://github.com/user-attachments/assets/c8975ad8-b921-4629-9d8b-246d4b2cd32f" />
   
6. Hovering over each bar will show the exact count of offered courses for the respective requirement. <br>
<img width="400" alt="Screenshot 2025-04-19 at 1 17 40 PM" src="https://github.com/user-attachments/assets/13a3c2c4-3f57-4645-b5ae-3bfce1ffc21e" />

<img width="800" alt="Screenshot 2025-04-19 at 1 11 43 PM" src="https://github.com/user-attachments/assets/431762a0-6fd1-49bf-b5cd-176b03a12548" />

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

