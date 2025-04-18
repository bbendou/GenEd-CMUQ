import React, { useEffect, useState } from "react";
import MultiSelectDropdown from "./MultiSelectDropdown";
import { formatCourseCode } from './utils/courseCodeFormatter';

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL;

const SearchBar = ({
  selectedDepartments,
  setSelectedDepartments,
  searchQuery,
  setSearchQuery,
  noPrereqs,
  setNoPrereqs,
  offeredQatar,
  setOfferedQatar,
  offeredPitts,
  setOfferedPitts,
  coreOnly,       // new prop for Core checkbox
  setCoreOnly,    // setter for Core checkbox
  genedOnly,      // new prop for GenEd checkbox
  setGenedOnly    // setter for GenEd checkbox
}) => {
  const [departments, setDepartments] = useState([]);

  // Set default values on component mount if not already set
  useEffect(() => {
    // Default location to Qatar if not already set
    // if (offeredQatar === null) {
    //   setOfferedQatar(true); // Removed: This prevents unchecking Qatar
    // }

    // Default course type to both Core and GenEd if not already set
    if (coreOnly === null && genedOnly === null) {
      setCoreOnly(true);
      setGenedOnly(true);
    }
  }, [coreOnly, genedOnly, setCoreOnly, setGenedOnly]);

  // Fetch departments from API
  useEffect(() => {
    const fetchDepartments = async () => {
      try {
        const response = await fetch(`${API_BASE_URL}/departments`);
        if (!response.ok) throw new Error("Failed to fetch departments");
        const data = await response.json();
        console.log("Fetched departments:", data);
        setDepartments(data.departments || []);
      } catch (error) {
        console.error("Error fetching departments:", error);
      }
    };

    fetchDepartments();
  }, []);

  // Function to get department name based on selected dep_code
  const getDepartmentName = (depCode) => {
    const dept = departments.find((dept) => dept.dep_code === depCode);
    return dept ? `${dept.dep_code} - ${dept.name}` : depCode;
  };

  // Modify the search input handler
  const handleSearchChange = (e) => {
    const formattedCode = formatCourseCode(e.target.value);
    setSearchQuery(formattedCode);
  };

  // Handle Enter key press in the search input
  const handleKeyDown = (event) => {
    if (event.key === 'Enter') {
      // Prevent default form submission if this were part of a form
      event.preventDefault();
      // Optionally blur the input to signify search completion
      event.target.blur();
      // The actual search is triggered by the state change via onChange
      // and the useEffect hook in the parent component.
      // No explicit search function call needed here.
    }
  };

  return (
    <div className="search-container">
      {/* Header Row for Labels */}
      <div className="search-header-row">
        {/* Wrap labels to control flex sizing */}
        <div className="search-label-wrapper">
          <label className="search-label">SEARCH</label>
        </div>
        <div className="filter-label-wrapper">
          <label className="filter-section-label">FILTER</label>
        </div>
      </div>

      {/* Content Row for Input and Filters */}
      <div className="search-content-row">
        {/* Wrapper for Search Input */}
        <div className="search-input-wrapper">
          <input
            type="text"
            placeholder="Search by course code (e.g. 15122 or 15-122)"
            value={searchQuery}
            onChange={handleSearchChange}
            onKeyDown={handleKeyDown}
            className="text-input"
          />
        </div>

        {/* Wrapper for Filter Groups */}
        <div className="search-filters-wrapper">
          {/* Department Dropdown */}
          <div className="filter-group">
            <label className="filter-label">Departments</label>
            <MultiSelectDropdown
              major="department"
              showSelectedInButton={false}
              wrapperClassName="department-dropdown-wrapper"
              allRequirements={departments.map((d) => ({
                value: d.dep_code,
                label: `${d.dep_code} - ${d.name}`,
              }))}
              selectedFilters={{ department: selectedDepartments }}
              handleFilterChange={(major, selected) => setSelectedDepartments(selected)}
              clearFilters={() => setSelectedDepartments([])}
            />
          </div>

          {/* Location Dropdown */}
          <div className="filter-group">
            <label className="filter-label">Location</label>
            <MultiSelectDropdown
              major="location"
              wrapperClassName="location-dropdown-wrapper"
              showSelectedInButton={true}
              hideSelectButtons={true}
              allRequirements={["qatar", "pitts"]}
              selectedFilters={{ location: [
                ...(offeredQatar ? ["qatar"] : []),
                ...(offeredPitts ? ["pitts"] : [])
              ] }}
              handleFilterChange={(major, selected) => {
                setOfferedQatar(selected.includes("qatar") ? true : null);
                setOfferedPitts(selected.includes("pitts") ? true : null);
              }}
              clearFilters={() => {
                setOfferedQatar(null);
                setOfferedPitts(null);
              }}
            />
          </div>

          {/* Course Type Dropdown */}
          <div className="filter-group">
            <label className="filter-label">Course Type</label>
            <MultiSelectDropdown
              major="courseType"
              wrapperClassName="course-type-dropdown-wrapper"
              showSelectedInButton={true}
              hideSelectButtons={true}
              allRequirements={["core", "gened"]}
              selectedFilters={{ courseType: [
                ...(coreOnly ? ["core"] : []),
                ...(genedOnly ? ["gened"] : [])
              ] }}
              handleFilterChange={(major, selected) => {
                setCoreOnly(selected.includes("core") ? true : null);
                setGenedOnly(selected.includes("gened") ? true : null);
              }}
              clearFilters={() => {
                setCoreOnly(null);
                setGenedOnly(null);
              }}
            />
          </div>
        </div> { /* End search-filters-wrapper */ }
      </div> { /* End search-content-row */ }

      {/*Display Selected Filters*/}
      {(selectedDepartments.length > 0 || searchQuery) && (
        <div className="selected-filters">
          {selectedDepartments.map((depCode) => (
            <span key={depCode} className="filter-tag">
              <button
                onClick={() =>
                  setSelectedDepartments((prev) =>
                    prev.filter((code) => code !== depCode)
                  )
                }
              >
                <span style={{ fontWeight: "bold", marginRight: "4px" }}>×</span>
              </button>
              {getDepartmentName(depCode)}
            </span>
          ))}

          {searchQuery && (
            <span className="filter-tag">
              <button onClick={() => setSearchQuery("")}>
                <span style={{ fontWeight: "bold", marginRight: "4px" }}>×</span>
              </button>
              {searchQuery}
            </span>
          )}
        </div>
      )}
    </div>
  );
};

export default SearchBar;
