import { BrowserRouter, Routes, Route } from "react-router-dom";
import { useEffect, useState } from "react";
import Navbar from "./components/Navbar";
import Home from "./pages/Home";
import DonorPage from "./pages/DonorPage";
import RequestPage from "./pages/RequestPage";
import MatchesTablePage from "./pages/MatchesTablePage";
import "./App.css";

function App() {
  const [theme, setTheme] = useState("light");

  useEffect(() => {
    const storedTheme = localStorage.getItem("lifelink-theme");
    if (storedTheme) {
      setTheme(storedTheme);
      return;
    }

    const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
    setTheme(prefersDark ? "dark" : "light");
  }, []);

  useEffect(() => {
    document.documentElement.setAttribute("data-theme", theme);
    localStorage.setItem("lifelink-theme", theme);
  }, [theme]);

  const toggleTheme = () => {
    setTheme((prev) => (prev === "light" ? "dark" : "light"));
  };

  return (
    <BrowserRouter>
      <div className="app">
        <div className="background-blobs" aria-hidden="true">
          <span className="blob blob-a" />
          <span className="blob blob-b" />
          <span className="blob blob-c" />
        </div>

        <Navbar theme={theme} onToggleTheme={toggleTheme} />

        <main className="page-shell">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/donor" element={<DonorPage />} />
            <Route path="/request" element={<RequestPage />} />
            <Route path="/matches" element={<MatchesTablePage />} />
          </Routes>
        </main>

        <footer className="footer">
          <p>
            &copy; 2026 LifeLink. Emergency-ready donor matching.
            <span className="footer-note">Built for saving lives, not just data.</span>
          </p>
        </footer>
      </div>
    </BrowserRouter>
  );
}

export default App;
