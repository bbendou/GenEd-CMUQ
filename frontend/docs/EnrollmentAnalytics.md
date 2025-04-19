# Component: `<EnrollmentAnalytics>`

## 📌 Purpose

Displays enrollment trends for CMU-Q courses. Combines two sub-components:
- **AggregatedEnrollmentAnalytics**: shows total enrollment across semesters for multiple selected courses.
- **ClassEnrollmentAnalytics**: displays enrollment per class year (Freshman, Sophomore, etc.) for a single course.

---

## 🔧 Internal Components

### 1. `<AggregatedEnrollmentAnalytics />`

| Feature         | Description |
|-----------------|-------------|
| Input           | Course code text box (`15122` or `15-122`) |
| Output          | Line chart of enrollment count over semesters |
| Logic           | Fetches enrollment totals for each course from `/analytics/enrollment-data` |
| UI              | Adds/removes course chips, shows loading/error states |

### 2. `<ClassEnrollmentAnalytics />`

| Feature         | Description |
|-----------------|-------------|
| Input           | Single course code |
| Output          | Line chart per class (1st year – 4th year) |
| Logic           | Filters enrollment by `class_` field and aggregates data |
| UI              | Allows toggling of view based on selected course code |

---

## 📤 Example Usage

```jsx
<EnrollmentAnalytics />
```

Place this component inside the `Analytics` tab of your app to let users explore how course enrollments evolve across semesters and cohorts.

---

## 🧪 Related Tests

- `EnrollmentAnalytics.test.js` — test coverage includes:
  - API calls for valid/invalid course codes
  - Chart rendering using mock Plotly data
  - UI for search, input, loading, and error handling

---

## 🎨 Styling

| Class / Style     | Description |
|-------------------|-------------|
| `search-container` | Container for each analytics panel |
| `text-input`, `add-all-btn` | Input and action controls |
| `filter-tag` | Course chips with remove buttons |
| `loading-spinner` | Displayed while fetching data |
| Plot styling | Handled by `react-plotly.js` responsive config |

---

## 🚨 Notes

- Requires backend support at:  
  `GET /analytics/enrollment-data?course_code=XX-XXX`
- Automatically deduplicates courses and applies semantic formatting (`15-122`)
- Enrollment traces use `lines+markers` for visual clarity
- Class-specific analytics excludes "Class 0" (unspecified or administrative entries)
