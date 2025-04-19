# Component: `<SingleSelectDropdown>`

## Purpose

Provides a simple dropdown component for selecting a single value from a list of options. Used in the GenEd interface to filter by pre-requisite availability.

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
