import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Login from "./components/Login/Login";
import Register from "./components/Register/Register";
import "./App.css";
import MonitoringPage from "./pages/MonitoringPage";

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/" element={<Login />} />
          <Route path="/monitoring" element={<MonitoringPage />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
