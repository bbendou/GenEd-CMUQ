# GenEd Frontend

This directory contains the React.js frontend application for the CMU-Q General Education course planning platform. It provides a searchable, filterable UI to explore and plan general education and core requirements across different majors.

---

## Getting Started

### Prerequisites

* Node.js (v16+ recommended)
* npm (comes with Node.js)

### Setup

1. **Navigate to the frontend directory:**
   ```bash
   cd path/to/GenEd-CMUQ/frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Run the development server:**
   ```bash
   npm start
   ```

The app will be accessible at `http://localhost:3000`.

> ⚠️ Make sure the backend is running and available at the correct API base URL. You can configure this in `.env`:
> ```env
> REACT_APP_API_BASE_URL=http://127.0.0.1:8000
> ```

---

## Features

- 🔍 Search for courses by department and course number.
- ✅ Filter by campus offering, prerequisites, GenEd/Core types, and requirement fulfillment.
- 📚 View courses fulfilling specific requirements.
- 📊 Paginated results for easy navigation.
- 🧩 Modular components with popup detail views.

---

## Components Overview

| Component | Purpose |
|----------|---------|
| `CourseTablePage.js` | Top-level controller for state and layout. Combines filters, search bar, and table. |
| `SearchBar.js` | Handles department selection, search input, and checkbox filters. |
| `CourseTable.js` | Renders the course data in a table format with dynamic requirement columns. |
| `MultiSelectDropdown.js` | Generic dropdown for selecting multiple filters (e.g. requirements, semesters). |
| `MultiSelectDepartment.js` | Specialized dropdown for department filtering. |
| `SelectedFilters.js` | Shows active filters with remove buttons. |
| `PopUp.js` | Modal that shows detailed course or requirement information. |

---

## File Structure

```
frontend/
│
├── public/                # Static files
│   ├── index.html
│   ├── manifest.json      # PWA settings
│   └── icons              # App icons 
│
├── docs/                # Documentation on all components
│
├── src/
│   ├── components/        # React components
│   │   ├── CourseTablePage.js
│   │   ├── CourseTable.js
│   │   ├── SearchBar.js
│   │   ├── PopUp.js
│   │   ├── MultiSelectDropdown.js
│   │   ├── MultiSelectDepartment.js
│   │   └── SelectedFilters.js
│   ├── styles.css         # App styling
│   ├── planTabStyles.css  # App styling for planning tab
│   └── index.js           # Entry point
│   └── App.js           
│
├── .env                   # API base URL config
├── package.json           # Project metadata & dependencies
└── README.md              # This file
```

---

## Running Tests

The frontend uses **Jest** and **React Testing Library** for testing. Make sure you are in the frontend folder before running tests.

### Running All Tests
```bash
npm test
```

### Running a Specific Test File
```bash
npm test CourseTable.test.js
```

### Example Test Files
Tests are located in the `frontend/tests/` directory and include:

```
tests/
├── CourseTable.test.js
├── SearchBar.test.js
├── CourseTablePage.test.js
├── MultiSelectDropdown.test.js
└── ...
```

Tests cover component rendering, user interactions, and prop handling. Each test simulates real user behavior using `@testing-library/react`.

> Make sure all required props are mocked correctly in your tests to avoid runtime errors.

---

## Development Notes

- Data is fetched dynamically via REST API endpoints from the FastAPI backend.
- API errors are handled in `useEffect` hooks with simple `console.error()` logs—consider improving with user notifications.
- The UI is responsive and works across modern browsers.

---

## Progressive Web App (PWA)

The frontend includes a `manifest.json` file to support installation as a PWA. Icons and colors can be customized in `public/manifest.json`.

---

## Authors

This project was developed by CMU-Q Students, Boushra, Jullia, and Yousuf, for the **67-373 Information Systems Consulting Project**.
