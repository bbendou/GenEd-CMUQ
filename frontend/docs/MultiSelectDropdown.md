# Component: `<MultiSelectDropdown>`

## Purpose

A reusable dropdown component supporting single or grouped multiselect behavior. Used for filtering by requirements, departments, course types, locations, and semesters in the GenEd UI.

---

## Instructions
The dropdowns under each major (BA, BS, CS, IS) and the Offered column allow you to filter courses based on specific requirements or semester offerings. Selecting a requirement will filter all the course results to show only those that fulfill chosen requirments.

1. Open the dropdown by clicking the “Select Requirements ▼” button.
2. Scroll through available options. These represent requirement paths (e.g., GenEd → Science and Engineering → Lab Requirement).
3. Check the boxes to select one or multiple filters. Click on *Apply Filters* when you're done choosing to update the table. This *Apply* button is disabled (gray) if there are no filters selected.
     - To select all options, click the “SELECT ALL” button. This will dynamically update the table.
     - To clear all selections, click the “CLEAR ALL” button. This will dynamically update the table. This button is disabled (gray) if there are no active filters for the major.
4. Selected filters will appear as colored tags above the table.
5. To remove requirement/offering filters:
   - Click on the 'x' button on its respective filter tags.
   - Open the dropdown again and scroll to the respective requirement/option, click on it again to deselect it. Then, click on *Apply Filters* to update the table.
<img width="262" alt="Screenshot 2025-04-19 at 1 41 36 PM" src="https://github.com/user-attachments/assets/d519a6ce-23d5-4261-9926-40c99dbf63c3" />

The department, location, and course type dropdowns in the search bar also use this component. Instructions on how to use them are located in SearchBar.md.

---

## Props

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

## Logic Overview

- Internally manages dropdown state (`isOpen`, `tempSelection`, `expandedGroups`)
- Uses `buildNestedGroups()` to structure Core/GenEd requirements into collapsible groups
- Dynamically renders:
  - Flat checkbox lists for `department`, `location`, etc.
  - Collapsible nested groups for requirement filtering
- Tracks temporary selection before applying via “Apply Filters” button
- Includes built-in toggles for “Select All”, “Clear All”, and group-specific selection

---

## Example Usage

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

## Related Tests

- `MultiSelectDropdown.test.js` — tests include:
  - Dropdown open/close behavior
  - Select/deselect logic
  - Nested group toggle and “Select All in group”
  - Apply filter validation

---

## Styling

| Class | Description |
|-------|-------------|
| `dropdown`, `dropdown-content`, `dropdown-btn` | Container and toggle styles |
| `dropdown-group`, `dropdown-subgroup` | Indent groups visually |
| `select-buttons-row`, `drop-apply-btn` | Action buttons within dropdown |
| `dropdown-item`, `checkbox-right` | Styles for checkbox labels |
| `dropdown-offered` | Specialized style for semester filters |

---

## Notes

- Avoid using dropdowns with hundreds of items — group hierarchies can grow deep.
- Dropdown closes on outside click (via `useRef` and `mousedown` event).
- Make sure `handleFilterChange()` handles both string and array inputs depending on context.
