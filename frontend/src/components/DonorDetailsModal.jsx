import React from "react";
import "./DonorDetailsModal.css";

export default function DonorDetailsModal({ donor, onClose }) {
  if (!donor) return null;

  const formatDate = (dateStr) => {
    try {
      return new Date(dateStr).toLocaleDateString("en-US", {
        year: "numeric",
        month: "long",
        day: "numeric",
      });
    } catch {
      return "N/A";
    }
  };

  const getScoreColor = (score) => {
    if (score >= 0.8) return "var(--success)";
    if (score >= 0.6) return "var(--warning)";
    return "var(--danger)";
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content glass surface-card" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2>Donor Details</h2>
          <button className="btn-close" onClick={onClose}>&times;</button>
        </div>
        
        <div className="modal-body">
          <div className="donor-profile">
            <div className="profile-header">
              <div className="donor-avatar">
                {donor.name ? donor.name.charAt(0) : "D"}
              </div>
              <div className="donor-info-main">
                <h3>{donor.name}</h3>
                <div className="donor-status">
                  <span className={`chip ${donor.health_eligible ? "chip-success" : "chip-danger"}`}>
                    {donor.health_eligible ? "Eligible" : "Ineligible"}
                  </span>
                  <span className="chip chip-info">{donor.blood_group}</span>
                </div>
              </div>
            </div>

            <div className="info-grid">
              <div className="info-item">
                <span className="info-label">Age</span>
                <span className="info-value">{donor.age} years</span>
              </div>
              <div className="info-item">
                <span className="info-label">Match Score</span>
                <span className="info-value" style={{ color: getScoreColor(donor.ml_score) }}>
                  {(donor.ml_score * 100).toFixed(0)}% Match
                </span>
              </div>
              <div className="info-item">
                <span className="info-label">Distance</span>
                <span className="info-value">{donor.distance_km?.toFixed(2)} km away</span>
              </div>
              <div className="info-item">
                <span className="info-label">Last Donation</span>
                <span className="info-value">{formatDate(donor.last_donation_date)}</span>
              </div>
              <div className="info-item">
                <span className="info-label">Contact Number</span>
                <span className="info-value">{donor.contact_number}</span>
              </div>
              <div className="info-item">
                <span className="info-label">Health Status</span>
                <span className="info-value">{donor.health_eligible ? "Healthy & Eligible" : "Currently Ineligible"}</span>
              </div>
            </div>

            <div className="stats-section">
              <div className="stats-grid">
                <div className="stat-item">
                  <span className="stat-value">{donor.donation_frequency_6m || 0}</span>
                  <span className="stat-label">Donations (6m)</span>
                </div>
                <div className="stat-item">
                  <span className="stat-value">{donor.successful_previous_matches || 0}</span>
                  <span className="stat-label">Successful Matches</span>
                </div>
                <div className="stat-item">
                  <span className="stat-value">{donor.has_adverse_reactions ? "Yes" : "None"}</span>
                  <span className="stat-label">Adverse Reactions</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className="modal-footer">
          <button className="btn btn-secondary" onClick={onClose}>Close</button>
          <a className="btn btn-primary" href={`tel:${donor.contact_number}`}>
            📞 Call Donor
          </a>
        </div>
      </div>
    </div>
  );
}
