# Component: `<DataUpload>`

## Purpose

Provides a user interface to upload datasets for initializing or updating the backend database. Supports uploading course ZIPs, audit ZIPs, enrollment Excel files, and department CSV files. Performs client-side validation for structure and file type before uploading.

---
## Instructions
For instructions, please visit the dedicated upload URL.

---

## Internal State

| State Variable      | Description |
|---------------------|-------------|
| `courseZips`        | ZIP files containing course data |
| `auditZips`         | ZIP files containing audit requirement data |
| `enrollmentFile`    | Excel file with course enrollment data |
| `departmentCsv`     | CSV file with department information |
| `error` / `success` | Display messages for validation/upload outcomes |
| `loading`           | Upload process status |

---

## Example Usage

```jsx
<DataUpload />
```

This component can be rendered on an admin or setup page where the backend database needs to be initialized with data from structured files. Files must follow expected formats, and course data is required if audit or enrollment data is present.

---

## Related Tests

- `DataUpload.test.js` — verifies:
  - ZIP structure validation (audit vs. course)
  - File type checks for Excel/CSV
  - Successful form submissions
  - Error and success message handling
  - Disabled state of the "Upload" button

---

## Styling & UI Libraries

| Element       | Source |
|---------------|--------|
| UI Components | [MUI (Material UI)](https://mui.com) |
| File Parsing  | [JSZip](https://stuk.github.io/jszip/) |
| Feedback UI   | `<Alert />`, `<CircularProgress />` from MUI |
| Hidden Input  | Styled with `VisuallyHiddenInput` using `@mui/material/styles` |

---

## Notes

- Performs client-side file type and content validation before sending to the backend.
- Uses `FormData` to send multiple files with the same field key (e.g., multiple ZIPs).
- Backend endpoint expected: `POST /upload/init-db/`
- All validation and upload combinations are described in a detailed instructional UI inside the component.

