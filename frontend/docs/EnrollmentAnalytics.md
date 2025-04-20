# Component: `<EnrollmentAnalytics>`

## Purpose

Displays enrollment trends for CMU-Q courses. Combines two sub-components:
- **AggregatedEnrollmentAnalytics**: shows total enrollment across semesters for multiple selected courses.
- **ClassEnrollmentAnalytics**: displays enrollment per class year (Freshman, Sophomore, etc.) for a single course.

---
## Instructions
At the top of the site, select the *Analytics* tab and scroll down to access visual insights on past course enrollment trends.

### Enrollment Analytics Across Courses
Use this section to compare enrollment patterns across multiple courses over time.
1. Enter a course code (e.g., 15-112, 15-110) into the input field and click “Add Course.”
2. Each selected course will appear as a tag below the input, and its enrollment trend will be plotted on the graph.
3. The X-axis displays semesters (e.g., S20, F22, S25), and the Y-axis shows enrollment counts.
4. Hover over the graph points for exact enrollment values per course and semester.
5. To remove a course from the chart, click the × on its corresponding tag.
<br>
<img width="600" alt="Screenshot 2025-04-19 at 3 55 23 PM" src="https://github.com/user-attachments/assets/a6986a29-8cf7-48e6-82f5-02d62c34cf8a" />

### Enrollment Analytics Across Classes
Use this section to see how a single course is taken by different student groups over time.
1. Enter the course code (e.g., 67-262) into the input field and click “Load Course.”
2. The chart will display enrollment counts for each student class group (e.g., Sophomores, Juniors, Seniors) across recent semesters.
3. Each group is color-coded and appears in the graph legend.
Use this data to understand which year levels typically take the course and how that changes over time.
<br>
<img width="600" alt="Screenshot 2025-04-19 at 3 55 16 PM" src="https://github.com/user-attachments/assets/0833a068-2726-47f0-8282-518c6db314da" />

---

## Internal Components

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

## Example Usage

```jsx
<EnrollmentAnalytics />
```

Place this component inside the `Analytics` tab of your app to let users explore how course enrollments evolve across semesters and cohorts.

---

## Related Tests

- `EnrollmentAnalytics.test.js` — test coverage includes:
  - API calls for valid/invalid course codes
  - Chart rendering using mock Plotly data
  - UI for search, input, loading, and error handling

---

## Styling

| Class / Style     | Description |
|-------------------|-------------|
| `search-container` | Container for each analytics panel |
| `text-input`, `add-all-btn` | Input and action controls |
| `filter-tag` | Course chips with remove buttons |
| `loading-spinner` | Displayed while fetching data |
| Plot styling | Handled by `react-plotly.js` responsive config |

---

## Notes

- Requires backend support at:  
  `GET /analytics/enrollment-data?course_code=XX-XXX`
- Automatically deduplicates courses and applies semantic formatting (`15-122`)
- Enrollment traces use `lines+markers` for visual clarity
- Class-specific analytics excludes "Class 0" (unspecified or administrative entries)
