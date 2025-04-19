# Component: `<MultiSelectDropdown>`

## 📌 Purpose

A reusable dropdown component supporting single or grouped multiselect behavior. Used for filtering by requirements, departments, course types, locations, and semesters in the GenEd UI.

---

## 🔧 Props

| Prop Name             | Type     | Required | Description |
|-----------------------|----------|----------|-------------|
| `major`               | String   | ✅       | Identifies the type of filter this dropdown manages |
| `allRequirements`     | Array    | ✅       | List of available options (can be flat or nested objects) |
| `selectedFilters`     | Object   | ✅       | Current selected filter values |
| `handleFilterChange`  | Function | ✅       | Callback to apply new filter selections |
| `clearFilters`        | Function | ✅       | Callback to clear all filters for this major |
| `showSelectedInButton` | Boolean | ❌       | If true, displays current selections in the button label |
| `hideSelectButtons`   | Boolean  | ❌       | Hides "Select All" and "Clear All" buttons if true |
| `wrapperClassName`    | String   | ❌       | Optional class name for styling the container |

---

## 🧠 Logic Overview

- Internally manages dropdown state (`isOpen`, `tempSelection`, `expandedGroups`)
- Uses `buildNestedGroups()` to structure Core/GenEd requirements into collapsible groups
- Dynamically renders:
  - Flat checkbox lists for `department`, `location`, etc.
  - Collapsible nested groups for requirement filtering
- Tracks temporary selection before applying via “Apply Filters” button
- Includes built-in toggles for “Select All”, “Clear All”, and group-specific selection

---

## 📤 Example Usage

```jsx
<MultiSelectDropdown
  major="CS"
  allRequirements={requirements.CS}
  selectedFilters={selectedFilters}
  handleFilterChange={handleFilterChange}
  clearFilters={clearFilters}
/>
```

You can reuse this for filtering by `department`, `offered`, `location`, `courseType`, or any requirement type. For non-requirement filters, it renders a simple list; for requirement filters, it renders a hierarchical group.

---

## 🧪 Related Tests

- `MultiSelectDropdown.test.js` — tests include:
  - Dropdown open/close behavior
  - Select/deselect logic
  - Nested group toggle and “Select All in group”
  - Apply filter validation

---

## 🎨 Styling

| Class | Description |
|-------|-------------|
| `dropdown`, `dropdown-content`, `dropdown-btn` | Container and toggle styles |
| `dropdown-group`, `dropdown-subgroup` | Indent groups visually |
| `select-buttons-row`, `drop-apply-btn` | Action buttons within dropdown |
| `dropdown-item`, `checkbox-right` | Styles for checkbox labels |
| `dropdown-offered` | Specialized style for semester filters |

---

## 🚨 Notes

- Avoid using dropdowns with hundreds of items — group hierarchies can grow deep.
- Dropdown closes on outside click (via `useRef` and `mousedown` event).
- Make sure `handleFilterChange()` handles both string and array inputs depending on context.
