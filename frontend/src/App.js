import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import MainTabs from "./components/MainTabs";
import DataUpload from './components/DataUpload';
import "./styles.css";

const App = () => {
  // Read the upload path from environment variable, with a fallback
  const uploadPath = process.env.REACT_APP_UPLOAD_PATH || '/configure-data'; // Fallback path

  return (
    <Router>
      <Routes>
        <Route path="/" element={<MainTabs />} />
        {/* Use the environment variable for the path */}
        <Route path={uploadPath} element={<DataUpload />} />
      </Routes>
    </Router>
  );
};

export default App;
