import React, { useState, useEffect, useCallback } from "react";
import "../styles.css";
import SearchBar from "./SearchBar";
import CourseTable from "./CourseTable";
import SelectedFilters from "./SelectedFilters";

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL;

const CourseTablePage = () => {
  // States for department and course search input
  const [selectedDepartment, setSelectedDepartment] = useState("");
  const [searchQuery, setSearchQuery] = useState("");
  // States for offered-location checkboxes
  const [offeredQatar, setOfferedQatar] = useState(null);
  const [offeredPitts, setOfferedPitts] = useState(null);
  // "No Prerequisites" flag: when true, fetch courses with no prerequisites
  const [noPrereqs, setNoPrereqs] = useState(null);
  // Requirement filters (for BA, BS, CS, IS)
  const [selectedFilters, setSelectedFilters] = useState({ BA: [], BS: [], CS: [], IS: [] });
  // Offered semester filter (selected via a dropdown in the table header)
  const [selectedOfferedSemesters, setSelectedOfferedSemesters] = useState([]);
  // Courses and requirements from API
  const [courses, setCourses] = useState([]);
  const [requirements, setRequirements] = useState({ BA: [], BS: [], CS: [], IS: [] });
  // All available offered semester options (fetched from the dedicated endpoint)
  const [offeredOptions, setOfferedOptions] = useState([]);

  // New state for requirement type filtering
  const [coreOnly, setCoreOnly] = useState(null);
  const [genedOnly, setGenedOnly] = useState(null);

  // Fetch departments from API
  useEffect(() => {
    const fetchDepartments = async () => {
      try {
        const response = await fetch(`${API_BASE_URL}/departments`);
        if (!response.ok) throw new Error("Failed to fetch departments");
        const data = await response.json();
        console.log("Fetched departments:", data);
      } catch (error) {
        console.error("Error fetching departments:", error);
      }
    };
    fetchDepartments();
  }, []);

  // Fetch requirements from API
  useEffect(() => {
    const fetchRequirements = async () => {
      try {
        const response = await fetch(`${API_BASE_URL}/requirements`);
        if (!response.ok) throw new Error("Failed to fetch requirements");
        const data = await response.json();
        console.log("Requirements fetched:", data);
        const transformedRequirements = { BA: [], BS: [], CS: [], IS: [] };
        data.requirements.forEach(({ requirement, type, major }) => {
          const majorKey = { cs: "CS", is: "IS", ba: "BA", bio: "BS" }[major];
          if (majorKey && transformedRequirements[majorKey]) {
            transformedRequirements[majorKey].push({ requirement, type: !!type, major: majorKey });
          }
        });

        setRequirements(transformedRequirements);
      } catch (error) {
        console.error("Error fetching requirements:", error);
      }
    };
    fetchRequirements();
  }, []);

  // Memoize the helper function so it only changes when coreOnly or genedOnly change.
  const courseMatchesRequirementFilter = useCallback((course) => {
    // If neither filter is active, include all courses.
    if (coreOnly === null && genedOnly === null) return true;

    // Check if the course has ANY requirements at all.
    const majors = Object.keys(course.requirements || {});
    const hasAnyReq = majors.some(
      (major) => (course.requirements[major] || []).length > 0
    );
    // If a course has no requirement data, include it.
    if (!hasAnyReq) return true;

    // For each major, filter the requirement objects.
    for (let major of majors) {
      const reqObjs = course.requirements[major] || [];
      const filtered = reqObjs.filter((reqObj) => {
        if (coreOnly && !genedOnly) {
          return reqObj.type === false; // Only Core requirements.
        } else if (genedOnly && !coreOnly) {
          return reqObj.type === true;  // Only GenEd requirements.
        }
        return true; // If both filters are inactive or both active, include all.
      });
      if (filtered.length > 0) return true;
    }
    return false;
  }, [coreOnly, genedOnly]);

  // Fetch courses using combined filters from backend
  useEffect(() => {
    const fetchCourses = async () => {
      try {
        const params = new URLSearchParams();
        if (selectedDepartment) params.append("department", selectedDepartment);
        if (searchQuery) params.append("searchQuery", searchQuery);
        if (selectedOfferedSemesters.length > 0)
          params.append("semester", selectedOfferedSemesters.join(","));
        if (noPrereqs === false) params.append("has_prereqs", false);
        if (offeredQatar !== null) params.append("offered_qatar", offeredQatar);
        if (offeredPitts !== null) params.append("offered_pitts", offeredPitts);
        if (selectedFilters.CS.length > 0)
          params.append("cs_requirement", selectedFilters.CS.join(","));
        if (selectedFilters.IS.length > 0)
          params.append("is_requirement", selectedFilters.IS.join(","));
        if (selectedFilters.BA.length > 0)
          params.append("ba_requirement", selectedFilters.BA.join(","));
        if (selectedFilters.BS.length > 0)
          params.append("bs_requirement", selectedFilters.BS.join(","));

        const response = await fetch(`${API_BASE_URL}/courses/search?${params.toString()}`);
        if (!response.ok) throw new Error("Failed to fetch courses");
        const data = await response.json();
        const filteredCourses = data.courses.filter(courseMatchesRequirementFilter);
        setCourses(filteredCourses);
      } catch (error) {
        console.error("Error fetching courses:", error);
      }
    };

    fetchCourses();
  }, [
    selectedDepartment,
    searchQuery,
    selectedOfferedSemesters,
    noPrereqs,
    offeredQatar,
    offeredPitts,
    selectedFilters.BA,
    selectedFilters.BS,
    selectedFilters.CS,
    selectedFilters.IS,
    coreOnly,
    genedOnly,
    courseMatchesRequirementFilter
  ]);

  // Fetch all semesters from the dedicated endpoint
  useEffect(() => {
    const fetchSemesters = async () => {
      try {
        const response = await fetch(`${API_BASE_URL}/courses/semesters`);
        if (!response.ok) throw new Error("Failed to fetch semesters");
        const data = await response.json();
        setOfferedOptions(data.semesters);
      } catch (error) {
        console.error("Error fetching semesters:", error);
      }
    };
    fetchSemesters();
  }, []);

  const handleFilterChange = (major, newSelection) => {
    setSelectedFilters((prev) => ({
      ...prev,
      [major]: Array.isArray(newSelection)
        ? newSelection
        : prev[major].filter((filter) => filter !== newSelection),
    }));
  };

  const clearFilters = (major) => {
    setSelectedFilters((prev) => ({ ...prev, [major]: [] }));
  };

  const removeOfferedSemester = (semester) => {
    setSelectedOfferedSemesters((prev) => prev.filter((s) => s !== semester));
  };

  return (
    <div className="table-container">
      <h1 className="title">CMU-Q General Education</h1>
      <SearchBar
        selectedDepartment={selectedDepartment}
        setSelectedDepartment={setSelectedDepartment}
        searchQuery={searchQuery}
        setSearchQuery={setSearchQuery}
        noPrereqs={noPrereqs}
        setNoPrereqs={setNoPrereqs}
        offeredQatar={offeredQatar}
        setOfferedQatar={setOfferedQatar}
        offeredPitts={offeredPitts}
        setOfferedPitts={setOfferedPitts}
        coreOnly={coreOnly}
        setCoreOnly={setCoreOnly}
        genedOnly={genedOnly}
        setGenedOnly={setGenedOnly}
      />
      <SelectedFilters
        selectedFilters={selectedFilters}
        handleFilterChange={handleFilterChange}
        selectedOfferedSemesters={selectedOfferedSemesters}
        removeOfferedSemester={removeOfferedSemester}
      />
      <div className="course-count">Showing {courses.length} courses</div>
      <CourseTable
        courses={courses}
        allRequirements={requirements}
        selectedFilters={selectedFilters}
        handleFilterChange={handleFilterChange}
        clearFilters={clearFilters}
        offeredOptions={offeredOptions}
        selectedOfferedSemesters={selectedOfferedSemesters}
        setSelectedOfferedSemesters={setSelectedOfferedSemesters}
        coreOnly={coreOnly}
        genedOnly={genedOnly}
      />
    </div>
  );
};

export default CourseTablePage;
