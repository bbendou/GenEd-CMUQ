# Component: `<PlanCourseTab>`

## 📌 Purpose

Provides an interactive tab where users can search for courses by code, add them to a personal plan, and view them in a dedicated table. Utilizes localStorage for persistence across sessions.

---

## 🔧 Internal State

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

## 🧠 Logic Overview

- Uses `localStorage` to persist added courses
- Fetches requirement data from backend to support table rendering
- Enables searching by formatted course code (e.g., `15122` or `15-122`)
- Displays toast messages when adding duplicate or new courses
- Filters out already added courses from re-adding
- Supports compact requirement views (`full`, `last2`, `last1`)
- Provides a search dropdown UI that collapses on outside click

---

## 📤 Example Usage

```jsx
<PlanCourseTab />
```

Used as a standalone tab or page in the GenEd planning interface. Requires the backend to expose:
- `/courses/search`
- `/courses/{course_code}`
- `/requirements`

---

## 🧱 Related Components

- `<CourseTable>` — reused to render planned courses
- Toast/snackbar
- Animated search results dropdown

---

## 🧪 Related Tests

- `PlanCourseTab.test.js` — test coverage includes:
  - Adding/removing courses
  - Search result rendering
  - Toast messages
  - Persistence with localStorage
  - UI toggle for compact views

---

## 🎨 Styling

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

## 🚨 Notes

- Integrates with `CourseTable`, so format consistency and filtering logic are shared.
- Can be easily extended to allow editing/removal or viewing course details.
- This component only adds courses via search; it does not support filtering by requirements or location.
