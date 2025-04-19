# Component: `<MainTabs>`

## 📌 Purpose

Serves as the entry-point navigation for the GenEd planning interface. Manages the three main tabs: **View**, **Plan**, and **Analytics**, and renders their associated components. Uses `localStorage` to persist the user’s last selected tab.

---

## 🔧 Internal State

| State Variable | Description |
|----------------|-------------|
| `activeTab`    | Stores the currently selected tab: `"general"`, `"plan"`, or `"analytics"` |

---

## 🧠 Logic Overview

- `useEffect` stores the selected tab in `localStorage` to persist tab selection across page reloads
- Renders one of the three tab components conditionally:
  - `"general"` → `<CourseTablePage />`
  - `"plan"` → `<PlanCourseTab />`
  - `"analytics"` → `<AnalyticsPage />`
- Applies the `"active"` class to the selected tab for styling

---

## 📤 Example Usage

```jsx
<MainTabs />
```

Used as the main controller in the app’s homepage or dashboard to switch between course viewing, planning, and analytics.

---

## 🧱 Related Components

- `<CourseTablePage>` — Tab for searching and filtering courses
- `<PlanCourseTab>` — Tab for managing a planned list of courses
- `<AnalyticsPage>` — Tab for displaying data visualizations on course metrics

---

## 🧪 Related Tests

- `MainTabs.test.js` — test coverage includes:
  - Tab switching
  - Persistence using localStorage
  - Conditional rendering of child components

---

## 🎨 Styling

| Class | Description |
|-------|-------------|
| `tab-bar` | Container for the tab toggle buttons |
| `tab`     | Style for inactive tabs |
| `tab.active` | Highlighted tab styling |
| `tab-content` | Content area under the tab bar |

---

## 🚨 Notes

- `key` props are applied to each tab render to ensure full reset of internal state when switching.
- You can extend this component to accept custom tab content or dynamically load tabs from configuration.
