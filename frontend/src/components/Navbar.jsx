import { Link } from "react-router-dom";
import "./Navbar.css";

export default function Navbar() {
  return (
    <nav className="navbar">
      <div className="navbar-container">
        <Link to="/" className="logo">
          🩸 LifeLink
        </Link>
        <ul className="nav-menu">
          <li>
            <Link to="/" className="nav-link">
              Home
            </Link>
          </li>
          <li>
            <Link to="/donor" className="nav-link">
              Register Donor
            </Link>
          </li>
          <li>
            <Link to="/request" className="nav-link">
              Create Request
            </Link>
          </li>
        </ul>
      </div>
    </nav>
  );
}
