import { BrowserRouter, Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import Home from "./pages/Home";
import DonorPage from "./pages/DonorPage";
import RequestPage from "./pages/RequestPage";
import MatchesTablePage from "./pages/MatchesTablePage";
import "./App.css";

function App() {
  return (
    <BrowserRouter>
      <div className="app">
        <Navbar />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/donor" element={<DonorPage />} />
          <Route path="/request" element={<RequestPage />} />
          <Route path="/matches" element={<MatchesTablePage />} />
        </Routes>
        <footer className="footer">
          <p>&copy; 2026 LifeLink. Saving lives through technology. 🩸</p>
        </footer>
      </div>
    </BrowserRouter>
  );
}

export default App;
