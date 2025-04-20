# Component: `<CourseTablePage>`

## Purpose

Acts as the main page controller for the CMU-Q GenEd frontend. Manages the UI state, filter logic, search behavior, course retrieval, and rendering of child components such as the search bar, table, and popups.

---
## Instructions
### View
Choosing a view from the view dropdown will update the length of the displayed requirements accordingly. This dropdown is located above the table, to the left of the Clear Filters button. 
- Full Requirements View: Contains the full requirements string. Ex: *Biological Sciences → Biological Sciences Electives → Biological Sciences Electives → Departmental Electives Group*
- Summarized Requirements View: Contains the last 2 groups of the requirements string. Ex: *Biological Sciences Electives → Departmental Electives Group*
- Compact Requirements View: Contains the last group of the requirements string. Ex: *Departmental Electives Group*
<img width="350" alt="Screenshot 2025-04-19 at 1 27 03 PM" src="https://github.com/user-attachments/assets/2bfcf15f-a6c5-4c80-a8c5-3d564840b7fe" /> <img width="800" alt="Screenshot 2025-04-19 at 1 37 28 PM" src="https://github.com/user-attachments/assets/d15b66ad-a19b-4faf-ae12-45d98cffff4c" />

When opening the website for the first time, the default view is the Full Requirements View.

### Clear Button
To reset all the chosen dropdown filters, search bar filter, or search queries, click on the *Clear All Filters* button. This is located above the table, next to the Requirements View dropdown select.
- A popup message should appear. Click on the *Clear All Filters* option. <br><img width="707" alt="Screenshot 2025-04-19 at 1 40 00 PM" src="https://github.com/user-attachments/assets/fc14d0b8-d2f5-4081-9d12-e27cd8f0879f" />

### Add to Plan Button
To add all the courses which are currently on your view tab to the planning tab, click on *Add All To Plan* button. This is located above the table, next to the Clear All Filters button.
- If there are more than 20 courses in view, a popup message should appear. Click on the *Yes, Add All* to confirm your decision. <br><img width="473" alt="Screenshot 2025-04-19 at 1 40 08 PM" src="https://github.com/user-attachments/assets/9efd5227-44b6-4442-a900-2ef363ad13c0" /> <br>
These courses are now successfully added to the plan tab. Open the plan tab to view your courses.
- This button will be disabled if all the courses in the view are already added to the plan tab.

### Sort Button
You can sort the table results by their course code or by the number of requirements met (with highest being priority).
- To change the sorting order, click on the *Sort by __* button. This is located above the table, next to the Add to Plan button.
- This will dynamically change based on the current sorting order. <br>
<img width="236" height="70" alt="Screenshot 2025-04-19 at 1 40 32 PM" src="https://github.com/user-attachments/assets/923794b3-58ee-4246-ba14-59c7b8f707ab" /> <img width="267" height="70" alt="Screenshot 2025-04-19 at 1 40 23 PM" src="https://github.com/user-attachments/assets/ae30b2a3-dd5b-47c9-bf42-bc3a97213a91" />

### Pagination Controls and Display
You can change the number of courses being displayed on the current page by selecting your desired number on the pagination controls.
- Scroll down to the bottom of the page until you reach the end of the current results.
- Click on the right-most dropdown, which controls how many courses are being displayed per page. <br>
<img width="303" alt="Screenshot 2025-04-19 at 1 40 57 PM" src="https://github.com/user-attachments/assets/b4f16778-090f-49c6-a908-dfc540f6fee4" />
<br>
Your chosen option, along with the total number of courses, is displayed on the top left of the table.
<br><img width="150" alt="Screenshot 2025-04-19 at 2 04 26 PM" src="https://github.com/user-attachments/assets/bf792041-2806-47de-ac74-d6c40bf4791f" />

</br>
You can also go to the previous or next page using these controls. Simply use the left and right arrows or click on a page number to go to your desired page. <br>
<img width="200" alt="Screenshot 2025-04-19 at 1 40 49 PM" src="https://github.com/user-attachments/assets/a231bed6-0db1-4631-b770-1dc16551a8b0" />

### Dropdowns
Instructions on the dropdowns are located in the following files: [SearchBar]([url](https://github.com/bbendou/GenEd-CMUQ/blob/frontend_documentation/frontend/docs/SearchBar.md)), [MultiSelectDropdown]([url](https://github.com/bbendou/GenEd-CMUQ/blob/frontend_documentation/frontend/docs/MultiSelectDropdown.md)), and [SingleSelectDropdown]([url](https://github.com/bbendou/GenEd-CMUQ/blob/frontend_documentation/frontend/docs/SingleSelectDropdown.md)).

---

## Internal State

- `selectedDepartments`, `searchQuery`, `noPrereqs`, `coreOnly`, `genedOnly`, etc.: Manage user-selected filters
- `courses`, `requirements`: Store data fetched from backend
- `offeredOptions`: Populates semester dropdowns
- `sortMode`: Toggles between sorting by course code or requirements
- `compactViewMode`: Controls the display format of requirement text
- `toast`, `loading`, `showConfirmPopup`, `showClearPopup`: UI feedback and modals

---

## API Calls

- `/departments`: Fetch list of departments for dropdown
- `/requirements`: Fetch course requirement data
- `/courses/search`: Fetch filtered list of courses
- `/courses/semesters`: Get available semesters

All filters and search values are sent as query parameters.

---

## Lifecycle Effects

- `useEffect` saves user preferences to `localStorage` for persistence
- Search query is debounced using a `setTimeout` (350ms delay)
- Courses and requirements are re-fetched when filters change
- Paginated display updates when data length or page changes

---

## Handlers

| Handler | Purpose |
|---------|---------|
| `handleFilterChange` | Updates selected filters by major |
| `clearFilters` | Clears all filters for a major |
| `removeOfferedSemester` | Removes a selected semester |
| `removePrereqFilter` | Resets the pre-req filter to null |
| `handleRemoveCourse` | Removes a course from the local course list |
| `addCoursesToPlan` | Saves selected courses to localStorage |
| `toggleSortByReqs` | Toggles between sorting modes |
| `clearAllFilters` | Resets all filters to their defaults |

---

## Child Components

- `<SearchBar />`
- `<SelectedFilters />`
- `<CourseTable />`
- Toast and popup components for UI interaction

---

## Related Tests

- `CourseTablePage.test.js` – covers filter state logic, fetch behavior, and UI interaction
- Mocks localStorage and API calls for isolation

---

## Styling

| Class | Description |
|-------|-------------|
| `table-container` | Main container layout |
| `view-toolbar` | Toolbar with filters, sort and plan buttons |
| `toast-snackbar` | Small floating message box |
| `popup-overlay-2`, `popup-box` | Modal styles for confirmation dialogs |
| `no-results-msg` | Display when no matching courses |

---

## Notes

- Uses `AbortController` to cancel pending API fetches and avoid race conditions.
- Stores filter state in `localStorage` for persistence across page reloads.
- Modular design supports adding new filters or sorting methods with minimal refactoring.
