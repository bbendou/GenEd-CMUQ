# Component: `<AnalyticsPage>`

## Purpose

Serves as the main analytics dashboard in the GenEd platform. Displays visual insights on:
- **Requirement Category Coverage** for a selected major
- **Enrollment Trends** across semesters and student classes

---

## Instructions
1. On the tab located on the top of the page, click on the *Analytics* tab.
<img width="800" alt="Screenshot 2025-04-19 at 1 08 46 PM" src="https://github.com/user-attachments/assets/77952f5d-91e2-494a-8a4b-6d71a7b4d80a" />

---

## Internal State

| State Variable   | Description |
|------------------|-------------|
| `selectedMajor`  | Currently selected major code (e.g., `"cs"`, `"bio"`) — saved in `localStorage` |

---

## Logic Overview

- Renders two major analytics sections:
  - `<CategoryCoverage>`: shows how many courses fulfill each requirement category
  - `<EnrollmentAnalytics>`: visualizes overall enrollment and enrollment by class year
- Uses localStorage to persist the selected major across page reloads

---

## Example Usage

```jsx
<AnalyticsPage />
```

Used in the **Analytics** tab of the GenEd app. This component provides an overview of course coverage and participation trends per major.

---

## Related Components

- `<CategoryCoverage />` — Major/semester-wise requirement category chart
- `<EnrollmentAnalytics />` — Enrollment comparison charts

---

## Related Tests

- `AnalyticsPage.test.js` — covers:
  - LocalStorage persistence of `selectedMajor`
  - Rendering both child components
  - UI behavior when switching majors

---

## Styling

| Class | Description |
|-------|-------------|
| `analytics-container` | Main page layout |
| `title`, `subtitle`   | Page header styles |
| `<hr />`              | Section separator |

---

## Notes

- Majors are hardcoded in the component for display purposes, but can be dynamically sourced if backend supports it.
- The selected major is passed to both analytics views for synchronized filtering.

