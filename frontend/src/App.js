// import CourseTableMock from "./components/courseTableMock/courseTableMock.js";
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import CourseTablePage from './components/CourseTablePage';
import DataUpload from './components/DataUpload';
import AnalyticsPage from './components/Analytics';
import "./styles.css";

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<CourseTablePage />} />
        <Route path="/upload" element={<DataUpload />} />
        <Route path="/analytics" element={<AnalyticsPage />} />
      </Routes>
    </Router>
  );
};

export default App;
