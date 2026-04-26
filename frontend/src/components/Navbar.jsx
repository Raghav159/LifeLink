import { NavLink } from "react-router-dom";
import "./Navbar.css";

export default function Navbar({ theme, onToggleTheme }) {
  const navClass = ({ isActive }) => (isActive ? "nav-link active" : "nav-link");

  return (
    <nav className="navbar">
      <div className="navbar-container glass">
        <NavLink to="/" className="logo">
          <span className="logo-mark">LL</span>
          <span>LifeLink</span>
        </NavLink>

        <ul className="nav-menu">
          <li>
            <NavLink to="/" className={navClass}>
              Home
            </NavLink>
          </li>
          <li>
            <NavLink to="/donor" className={navClass}>
              Register Donor
            </NavLink>
          </li>
          <li>
            <NavLink to="/request" className={navClass}>
              Create Request
            </NavLink>
          </li>
          <li>
            <NavLink to="/matches" className={navClass}>
              Matches
            </NavLink>
          </li>
        </ul>

        <div className="navbar-actions">
          <button
            className={`theme-toggle ${theme === "dark" ? "theme-toggle-dark" : "theme-toggle-light"}`}
            type="button"
            onClick={onToggleTheme}
            aria-label="Toggle between light and dark theme"
            aria-pressed={theme === "dark"}
          >
            <span className="theme-toggle-track" aria-hidden="true">
              <svg className="theme-toggle-icon theme-toggle-icon-sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
                <circle cx="12" cy="12" r="4" />
                <path d="M12 2v2" />
                <path d="M12 20v2" />
                <path d="M4.93 4.93l1.41 1.41" />
                <path d="M17.66 17.66l1.41 1.41" />
                <path d="M2 12h2" />
                <path d="M20 12h2" />
                <path d="M4.93 19.07l1.41-1.41" />
                <path d="M17.66 6.34l1.41-1.41" />
              </svg>
              <svg className="theme-toggle-icon theme-toggle-icon-moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
                <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z" />
              </svg>
              <span className="theme-toggle-thumb">
                {theme === "dark" ? (
                  <svg className="theme-thumb-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z" />
                  </svg>
                ) : (
                  <svg className="theme-thumb-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <circle cx="12" cy="12" r="4" />
                    <path d="M12 2v2" />
                    <path d="M12 20v2" />
                    <path d="M4.93 4.93l1.41 1.41" />
                    <path d="M17.66 17.66l1.41 1.41" />
                    <path d="M2 12h2" />
                    <path d="M20 12h2" />
                    <path d="M4.93 19.07l1.41-1.41" />
                    <path d="M17.66 6.34l1.41-1.41" />
                  </svg>
                )}
              </span>
            </span>
          </button>
          <NavLink to="/request" className="btn btn-primary emergency-btn">
            Emergency Request
          </NavLink>
        </div>
      </div>
    </nav>
  );
}
