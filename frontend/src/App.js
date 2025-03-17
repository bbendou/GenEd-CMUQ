import React, { useState } from "react";
import CourseTablePage from "./components/CourseTablePage";
import AnalyticsPage from "./components/Analytics";
import "./styles.css";

const App = () => {
  const [currentPage, setCurrentPage] = useState("table");

  return (
    <div>
      <nav style={{ padding: "10px", backgroundColor: "#eee", marginBottom: "20px" }}>
        <button onClick={() => setCurrentPage("table")}>Main Page</button>
        <button onClick={() => setCurrentPage("analytics")} style={{ marginLeft: "10px" }}>
          Analytics Page
        </button>
      </nav>
      {currentPage === "table" ? <CourseTablePage /> : <AnalyticsPage />}
    </div>
  );
};

export default App;
