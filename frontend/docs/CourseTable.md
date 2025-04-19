# Component: `<CourseTable>`

## Purpose

Renders the main table displaying filtered courses. Includes interactive filters per major, prerequisite status, and semester offerings. Each row supports a popup to show detailed course or requirement information. Also adapts behavior for “Plan” and “View” tabs.

---
## Instructions
1. On the top of the page, select the *View* or *Plan* tab.
2. Choose a filter, from the dropdowns or the search bar, or search for a course on the search bar. This should reflect and automatically update the course table accordingly. <br>
   <img width="800" alt="Screenshot 2025-04-19 at 1 26 11 PM" src="https://github.com/user-attachments/assets/d8530c57-59ba-4f0e-a948-d2c43397eb2d" />

- When the pre-req list is long, click on the *Show More/Less* button to toggle details.
- When on the *Summarized* or *Compact* view, the semester offerings list will also have a similar toggle. Click on the *Show More/Less* button to toggle details. <br><img width="200" alt="Screenshot 2025-04-19 at 1 29 18 PM" src="https://github.com/user-attachments/assets/7fcc0a0c-9f55-4c03-8cfe-030a13d26223" />

  <img width="200" alt="Screenshot 2025-04-19 at 1 30 20 PM" src="https://github.com/user-attachments/assets/72cee343-cf82-4a7b-ae73-54f9e0058d0c" />


---

## Props

| Prop Name                 | Type     | Required | Description |
|--------------------------|----------|----------|-------------|
| `courses`                | Array    | ✅       | List of course objects to display |
| `allRequirements`        | Object   | ✅       | Requirement options grouped by major |
| `selectedFilters`        | Object   | ✅       | Tracks currently selected requirement filters |
| `handleFilterChange`     | Function | ✅       | Updates selected filters |
| `clearFilters`           | Function | ✅       | Clears all filters for a given major |
| `offeredOptions`         | Array    | ✅       | List of semesters used in the offered column |
| `selectedOfferedSemesters` | Array | ✅       | List of semesters currently selected |
| `setSelectedOfferedSemesters` | Function | ✅   | Updates selected offered semesters |
| `coreOnly`               | Boolean  | ❌       | If true, show only Core requirements |
| `genedOnly`              | Boolean  | ❌       | If true, show only GenEd requirements |
| `allowRemove`            | Boolean  | ❌       | If true, shows a delete button per course |
| `handleRemoveCourse`     | Function | ❌       | Function to remove a course (only if `allowRemove`) |
| `noPrereqs`              | Boolean / null | ❌   | Controls Prerequisite dropdown state |
| `setNoPrereqs`           | Function | ❌       | Updates prerequisite filter setting |
| `compactViewMode`        | String   | ❌       | If `"last1"` or `"last2"`, trims long requirement labels |
| `hideDropdowns`          | Boolean  | ❌       | If true, hides filter dropdowns in headers |
| `isPlanTab`              | Boolean  | ❌       | If true, adjusts empty state message for Plan tab |

---

## State & Logic

- `isPopupOpen`, `popupType`, `popupContent`: control the popup modal
- `fetchCourseDetails`: fetches full details of a course on click
- `filterRequirementObjects`: filters requirements based on `coreOnly` and `genedOnly`
- `compactViewMode`: trims requirement text in cells (`last1` or `last2`)
- `OfferedCell` and `PrereqCell`: expandable cells with “Show more” toggles

---

## Example Usage

```jsx
<CourseTable
  courses={courses}
  allRequirements={requirements}
  selectedFilters={selectedFilters}
  handleFilterChange={handleFilterChange}
  clearFilters={clearFilters}
  offeredOptions={offeredOptions}
  selectedOfferedSemesters={selectedOfferedSemesters}
  setSelectedOfferedSemesters={setSelectedOfferedSemesters}
  coreOnly={true}
  genedOnly={false}
  allowRemove={true}
  handleRemoveCourse={handleRemoveCourse}
  compactViewMode={"last1"}
/>
```

---

## Related Tests

- `CourseTable.test.js` – rendering, dropdown filters, popup behavior, expand/collapse functionality.

---

## Related Components

- `<MultiSelectDropdown />`
- `<SingleSelectDropdown />`
- `<Popup />`

---

## Styling

- `remove-col`: column for delete button
- `header-offered`, `header-prereq`, `header-{major}`: table header styles
- `expand-toggle`: Show more / less toggle
- `cell-offered`, `cell-prereq`, `cell-{major}`: data cell styles

---

## Notes

- Requirements are dynamically filtered and formatted based on Core/GenEd flags.
- Popup supports both course and requirement views.
- Offered semesters are sorted chronologically (F/S/M + year).
- Handles both full view and compact display modes.
