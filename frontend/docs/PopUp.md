# Component: `<PopUp>`

## Purpose

Displays a modal overlay containing detailed information about either a course or a requirement. Dynamically switches between `course` and `requirement` view modes. Used in the CourseTable to provide interactive, in-depth exploration.

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

