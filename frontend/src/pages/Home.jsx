import { Link } from "react-router-dom";
import BlurText from "../components/BlurText";
import CountUp from "../components/CountUp";
import "./Pages.css";

export default function Home() {
  const trustStats = [
    { to: 24, suffix: "k+", label: "Active donors", duration: 1.8 },
    { to: 4.8, suffix: " min", label: "Average match time", duration: 1.5 },
    { to: 112, suffix: "", label: "Coverage zones", duration: 1.9 },
    { to: 97, suffix: "%", label: "Fulfillment reliability", duration: 1.7 },
  ];

  return (
    <div className="home">
      <section className="hero glass surface-card">
        <div className="hero-copy">
          <BlurText
            text="Emergency-ready donor network"
            delay={85}
            animateBy="words"
            direction="top"
            className="hero-kicker hero-kicker-animated"
            as="p"
          />
          <BlurText
            text="Find Blood Donors in Minutes, Not Hours"
            delay={140}
            animateBy="words"
            direction="top"
            className="hero-title"
            as="h1"
          />
          <BlurText
            text="Intelligent ranking + location-aware matching designed for hospitals and emergency teams. Built to reduce response time when every minute matters."
            delay={42}
            animateBy="words"
            direction="top"
            className="hero-subcopy"
            as="p"
          />
          <div className="hero-actions">
            <Link to="/donor" className="btn btn-secondary">Become Donor</Link>
            <Link to="/request" className="btn btn-primary">Find Donors</Link>
          </div>
        </div>

        <div className="hero-floating">
          <article className="floating-card card-one glass surface-card">
            <p>Live Match</p>
            <h3>O- request</h3>
            <span>92% compatibility</span>
          </article>
          <article className="floating-card card-two glass surface-card">
            <p>Nearest Donor</p>
            <h3>2.4 km</h3>
            <span>Health eligible</span>
          </article>
          <article className="floating-card card-three glass surface-card">
            <p>Avg Match Time</p>
            <h3>4.8 min</h3>
            <span>Across 112 zones</span>
          </article>
        </div>
      </section>

      <section className="trust-strip glass surface-card">
        {trustStats.map((stat, index) => (
          <article key={stat.label}>
            <h3 className="trust-value">
              <CountUp
                from={0}
                to={stat.to}
                separator=","
                direction="up"
                duration={stat.duration}
                delay={0.1 * index}
                className="count-up-text"
              />
              {stat.suffix}
            </h3>
            <p className="trust-label">{stat.label}</p>
          </article>
        ))}
      </section>

      <section className="features">
        <h2>How It Works</h2>
        <div className="feature-grid">
          <div className="feature-card glass surface-card">
            <h3>1. Create Request</h3>
            <p>Set blood group, urgency, units, and location in a guided flow.</p>
          </div>

          <div className="feature-card glass surface-card">
            <h3>2. AI Matching</h3>
            <p>Compatibility, distance, and health factors are ranked instantly.</p>
            <span className="chip chip-info">Smart Priority Engine</span>
          </div>

          <div className="feature-card glass surface-card">
            <h3>3. Connect Fast</h3>
            <p>Contact best donors with clear actions and coordinated outreach.</p>
          </div>
        </div>
      </section>

      <section className="cta glass surface-card">
        <h2>Your one action can save a life.</h2>
        <p>Join as donor or create a request from the navigation above when you need to act.</p>
      </section>
    </div>
  );
}
