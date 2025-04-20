# Component: `<PopUp>`

## Purpose

Displays a modal overlay containing detailed information about either a course or a requirement. Dynamically switches between `course` and `requirement` view modes. Used in the CourseTable to provide interactive, in-depth exploration.

---
## Instructions
The popup appears when a course code or requirement cell is clicked in the course table. It provides detailed information without navigating away from the main view.

### Course Popups
Clicking on a course code opens a popup displaying detailed course information, including the course code, title, unit count, description, prerequisites, semester offerings, and the requirements it fulfills across majors. You can scroll through the list of fulfilled requirements, organized by major. <br>
<img width="300" alt="Screenshot 2025-04-19 at 12 36 51 PM" src="https://github.com/user-attachments/assets/24caac5a-c7f4-4213-ade7-42efedbfab2b" />

### Requirement Popups
Clicking on a requirement cell opens a popup showing all the courses that fulfill that specific requirement. The requirement name is shown at the top, and the list of matching courses appears below. Each course name is clickable and will open a course details popup when selected. <br>
<img width="300" alt="Screenshot 2025-04-19 at 12 36 59 PM" src="https://github.com/user-attachments/assets/ebf6abbd-155f-42a8-8691-224d498d5c67" />


### Closing the Popup
Click the ✖ icon in the top-right corner of the popup panel to close it and return to the main view.

---
## Props

| Prop Name   | Type     | Required | Description |
|-------------|----------|----------|-------------|
| `isOpen`    | Boolean  | ✅       | Controls visibility of the popup |
| `onClose`   | Function | ✅       | Callback for closing the popup |
| `type`      | String   | ✅       | "course" or "requirement" – controls rendering logic |
| `content`   | Object   | ✅       | Course or requirement data to display |
| `openPopup` | Function | ✅       | Used for opening nested popups (e.g., clicking a requirement course link) |

---

## Logic Overview

- `formatRequirement()`: Helper function to clean and format raw requirement strings (especially for GenEd).
  - Handles variations like "General Education" or "University Core Requirements".
  - Converts `---` separators into arrows (`→`).
- Requirements and courses are grouped and displayed per major.
- Deduplicates and sorts semesters using `sortSemesters()`.

---

## Example UI

### Course View

Displays:
- Course code, name, units, description
- Prerequisites (cleaned)
- Semesters offered
- Requirements it fulfills (grouped by major)

### Requirement View

Displays:
- Formatted requirement name
- List of courses that fulfill it
- Each course is clickable and opens its popup view

---


---

## Example Usage

```jsx
<Popup
  isOpen={isPopupOpen}
  onClose={() => setIsPopupOpen(false)}
  type="course"
  content={selectedCourse}
  openPopup={(type, content) => {
    setPopupType(type);
    setPopupContent(content);
    setIsPopupOpen(true);
  }}
/>
```

You can trigger this component on row clicks or requirement clicks within `<CourseTable>`. The `type` can be `"course"` or `"requirement"` depending on the context, and the `content` prop should contain either full course data or a requirement object with a list of courses.


## Related Tests

- `Popup.test.js` – test visibility toggling, correct formatting of requirements, rendering of course list

---

## Styling

| Class | Description |
|-------|-------------|
| `popup-overlay` | Full-screen dimmed background |
| `popup-panel` | Main content container |
| `popup-close-btn` | Closes the popup |
| `popup-title` | Header text |
| `requirement-group`, `requirement-list` | Styling for grouped content |
| `course-link` | Clickable course item within requirement view |

---

## Notes

- Popup is conditionally rendered – returns `null` if `isOpen` is false.
- Uses `Set` and custom sorting to handle semester display cleanly.
- Uses nested click handlers to allow opening another popup from within a requirement popup.

