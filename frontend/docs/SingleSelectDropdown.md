# Component: `<SingleSelectDropdown>`

## Purpose

Provides a simple dropdown component for selecting a single value from a list of options. Used in the GenEd interface to filter by pre-requisite availability.

---
## Instructions
This is used exclusively in the Pre-req column of the course table. It allows you to filter courses based on whether or not they have prerequisites.

Clicking the dropdown will reveal three options:
- All course - Shows all courses (default)
- Has Pre-reqs – Displays only courses that list prerequisites.
- No Pre-reqs – Displays only courses that do not require any prerequisites.

Once selected, the course table updates automatically to reflect your choice. Only one option can be selected at a time.
<img width="150" alt="Screenshot 2025-04-19 at 12 37 36 PM" src="https://github.com/user-attachments/assets/6f2225fc-5e2e-4a4b-8c2f-37b1c8446c79" />


### Clearing the Filter
To remove the filter, click the dropdown again and select *All Courses*. The full list of courses will reappear. Or, you can also press the X button on the respective filter tag that appears on top of the course table.

---

## Props

| Prop Name   | Type     | Required | Description |
|-------------|----------|----------|-------------|
| `options`   | Array    | ✅       | List of options to display in the dropdown |
| `selected`  | String   | ✅       | Currently selected value |
| `onChange`  | Function | ✅       | Callback triggered when a new value is selected |
| `major`     | String   | ❌       | Optional identifier used for styling contextually (e.g., for prereq dropdown) |

---

## Logic Overview

- Internal state tracks whether the dropdown is open
- Uses `useRef` and a `mousedown` listener to close the dropdown when clicking outside
- Renders options with a radio-button-like checkbox UI (only one item can be selected at a time)

---

## Example Usage

```jsx
<SingleSelectDropdown
  options={["all", "with", "without"]}
  selected={"with"}
  onChange={(value) => setNoPrereqs(value === "with" ? true : value === "without" ? false : null)}
  major="prereq"
/>
```

Used in the “Prerequisites” column of `<CourseTable>` to toggle between showing:
- All courses
- Only those with prerequisites
- Only those without prerequisites

---

## Related Tests

- `SingleSelectDropdown.test.js` – tests for:
  - Opening and closing the dropdown
  - Selecting an item triggers `onChange`
  - Only one item can be selected at a time

---

## Styling

| Class | Description |
|-------|-------------|
| `dropdown`, `dropdown-btn`, `dropdown-content` | General dropdown styles |
| `dropdown-prereq` | Applied when `major="prereq"` to style differently |
| `dropdown-item` | Individual option style |

---

## Notes

- The dropdown is not a native `<select>` element for styling flexibility.
- Can be extended to support other single-choice filters if needed.
