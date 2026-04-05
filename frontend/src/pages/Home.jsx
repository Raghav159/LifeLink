import { Link } from "react-router-dom";
import "./Pages.css";

export default function Home() {
  return (
    <div className="home">
      <section className="hero">
        <div className="hero-content">
          <h1>🩸 Welcome to LifeLink</h1>
          <p>AI-Powered Blood Donor Matching Platform</p>
          <p className="subtitle">
            Connect donors and recipients efficiently with machine learning-powered matching
          </p>
        </div>
      </section>

      <section className="features">
        <h2>How It Works</h2>
        <div className="feature-grid">
          <div className="feature-card">
            <h3>1. Register as Donor</h3>
            <p>Share your blood type, location, and availability to help those in need.</p>
            <Link to="/donor" className="link-btn">Register Now</Link>
          </div>

          <div className="feature-card">
            <h3>2. Create Request</h3>
            <p>Submit blood requests with urgency levels and specific requirements.</p>
            <Link to="/request" className="link-btn">Create Request</Link>
          </div>
        </div>
      </section>

      <section className="stats">
        <div className="stat-item">
          <h3>🌍 Coverage</h3>
          <p>Real-time matching across regions</p>
        </div>
        <div className="stat-item">
          <h3>🤖 Smart AI</h3>
          <p>ML-powered donor compatibility</p>
        </div>
        <div className="stat-item">
          <h3>⚡ Fast</h3>
          <p>Instant donor suggestions</p>
        </div>
        <div className="stat-item">
          <h3>🔒 Secure</h3>
          <p>Privacy-first approach</p>
        </div>
      </section>

      <section className="cta">
        <h2>Ready to Save Lives?</h2>
        <div className="cta-buttons">
          <Link to="/donor" className="btn btn-primary">Become a Donor</Link>
          <Link to="/request" className="btn btn-secondary">Request Blood</Link>
        </div>
      </section>
    </div>
  );
}
