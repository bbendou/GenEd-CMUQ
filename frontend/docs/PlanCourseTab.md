# Component: `<PlanCourseTab>`

## Purpose

Provides an interactive tab where users can search for courses by code, add them to a personal plan, and view them in a dedicated table. Utilizes localStorage for persistence across sessions.

---
## Instructions
### Adding Courses
Use the search functionality at the top of the Plan tab to find existing courses by code or department. Once located, click the “Add” button next to a course to add it to your personal course plan. <br>
<img width="517" alt="Screenshot 2025-04-19 at 3 35 48 PM" src="https://github.com/user-attachments/assets/bd783fca-986e-4cea-b319-44355d4f24fa" />


### Planned Course Table
Courses you’ve added will appear in a table that mirrors the main course table structure. Each row represents a course, and each column shows which requirements that course fulfills per major. You can hover or click on the requirement cells to view more details in a popup.

### Removing Courses
To remove a course from your plan, click the ✖ icon in the first column of the row. The table will update immediately to reflect the change. <br>
<img width="272" alt="Screenshot 2025-04-19 at 3 51 29 PM" src="https://github.com/user-attachments/assets/075a3a36-7f81-4c44-a04d-143cb084e9ce" />

### Clear All Courses
Click the “Clear All” button, then "OK" on the popup message, to remove all courses from your current plan and reset the planning table. 
<img width="479" alt="Screenshot 2025-04-19 at 3 36 07 PM" src="https://github.com/user-attachments/assets/e2830b8f-36bd-41c7-bf66-4e517e247b43" />


---

## Internal State

| State Variable      | Description |
|---------------------|-------------|
| `searchQuery`       | Input for searching course code |
| `searchResults`     | Results returned from course search |
| `addedCourses`      | Courses added to the plan (stored in localStorage) |
| `requirements`      | Requirements used for formatting the course table |
| `toast`             | Snackbar message state for success/warnings |
| `showSearchResults` | Toggles visibility of search result panel |
| `compactViewMode`   | Controls how requirement paths are displayed |
| `loading`           | Whether requirement data is being fetched |

---

## Logic Overview

- Uses `localStorage` to persist added courses
- Fetches requirement data from backend to support table rendering
- Enables searching by formatted course code (e.g., `15122` or `15-122`)
- Displays toast messages when adding duplicate or new courses
- Filters out already added courses from re-adding
- Supports compact requirement views (`full`, `last2`, `last1`)
- Provides a search dropdown UI that collapses on outside click

---

## Example Usage

```jsx
<PlanCourseTab />
```

Used as a standalone tab or page in the GenEd planning interface. Requires the backend to expose:
- `/courses/search`
- `/courses/{course_code}`
- `/requirements`

---

## Related Components

- `<CourseTable>` — reused to render planned courses
- Toast/snackbar
- Animated search results dropdown

---

## Related Tests

- `PlanCourseTab.test.js` — test coverage includes:
  - Adding/removing courses
  - Search result rendering
  - Toast messages
  - Persistence with localStorage
  - UI toggle for compact views

---

## Styling

| Class | Description |
|-------|-------------|
| `plan-tab-container` | Main wrapper layout |
| `search-bar-container`, `search-bar-enhanced` | Custom search bar layout |
| `scrollable-results` | Floating container for search matches |
| `course-result-item` | Each item in the result list |
| `toast-snackbar` | Feedback messages |
| `loading-spinner` | Loading indicator |
| `view-toggle`, `clear-all-btn` | Utility controls for view and clearing plan |

---

## Notes

- Integrates with `CourseTable`, so format consistency and filtering logic are shared.
- Can be easily extended to allow editing/removal or viewing course details.
- This component only adds courses via search; it does not support filtering by requirements or location.
