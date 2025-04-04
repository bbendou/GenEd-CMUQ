import React, { useState, useEffect } from "react";
import CourseTable from "./CourseTable";
import { formatCourseCode } from './utils/courseCodeFormatter';
import "../styles.css";

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL;

const PlanCourseTab = () => {
  const [searchQuery, setSearchQuery] = useState("");
  const [searchResults, setSearchResults] = useState([]);

  // Use localStorage to persist added courses
  const [addedCourses, setAddedCourses] = useState(() => {
    const savedCourses = localStorage.getItem("plannedCourses");
    return savedCourses ? JSON.parse(savedCourses) : [];
  });

  const [requirements, setRequirements] = useState({ BA: [], BS: [], CS: [], IS: [] });

  // Save added courses to localStorage whenever they change
  useEffect(() => {
    localStorage.setItem("plannedCourses", JSON.stringify(addedCourses));
  }, [addedCourses]);

  useEffect(() => {
    const fetchRequirements = async () => {
      try {
        const response = await fetch(`${API_BASE_URL}/requirements`);
        const data = await response.json();
        const grouped = { BA: [], BS: [], CS: [], IS: [] };
        data.requirements.forEach(({ requirement, type, major }) => {
          const majorKey = {
            cs: "CS",
            is: "IS",
            ba: "BA",
            bio: "BS",
          }[major];
          if (majorKey) grouped[majorKey].push({ requirement, type: !!type, major: majorKey });
        });
        setRequirements(grouped);
      } catch (err) {
        console.error("Failed to fetch requirements:", err);
      }
    };
    fetchRequirements();
  }, []);

  const handleSearch = async () => {
    try {
      const formattedQuery = formatCourseCode(searchQuery);
      const response = await fetch(`${API_BASE_URL}/courses/search?searchQuery=${formattedQuery}`);
      const data = await response.json();
      setSearchResults(data.courses || []);
    } catch (err) {
      console.error("Search error:", err);
    }
  };

  const addCourse = async (course) => {
    if (addedCourses.some((c) => c.course_code === course.course_code)) return;
    try {
      const res = await fetch(`${API_BASE_URL}/courses/${course.course_code}`);
      const fullCourse = await res.json();
      setAddedCourses((prev) => [...prev, fullCourse]);
      setSearchQuery("");
      setSearchResults([]);
    } catch (err) {
      console.error("Error adding course:", err);
    }
  };

  const removeCourse = (code) => {
    setAddedCourses((prev) => prev.filter((c) => c.course_code !== code));
  };

  const clearAllCourses = () => {
    if (window.confirm("Are you sure you want to clear all planned courses?")) {
      setAddedCourses([]);
    }
  };

  return (
    <div className="plan-tab">
      <h1 className="title">Plan Courses</h1>

      <div className="search-bar">
        <input
          className="search-input"
          type="text"
          placeholder="Search by course code (e.g. 15122 or 15-122)"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
        />
        <button className="search-btn" onClick={handleSearch}>🔍</button>
      </div>

      {searchResults.length > 0 && (
        <div className="search-results">
          <ul className="search-result-list">
            {searchResults.map((course) => (
              <li key={course.course_code} className="search-result-item">
                <span
                  className="course-link"
                  onClick={() => addCourse(course)}
                  title="Click to add"
                >
                  {course.course_code} – {course.course_name}
                </span>
                <button className="add-btn" onClick={() => addCourse(course)}>Add</button>
              </li>
            ))}
          </ul>
        </div>
      )}

      {addedCourses.length > 0 && (
        <div className="planned-courses-header">
          <h3>Selected Courses ({addedCourses.length})</h3>
          <button className="clear-all-btn" onClick={clearAllCourses}>Clear All</button>
        </div>
      )}

      <CourseTable
        courses={addedCourses}
        allRequirements={requirements}
        selectedFilters={{ BA: [], BS: [], CS: [], IS: [] }}
        handleFilterChange={() => {}}
        clearFilters={() => {}}
        offeredOptions={[]}
        selectedOfferedSemesters={[]}
        setSelectedOfferedSemesters={() => {}}
        coreOnly={false}
        genedOnly={false}
        allowRemove={true}
        handleRemoveCourse={removeCourse}
      />
    </div>
  );
};

export default PlanCourseTab;
