import { useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import "./MatchesTablePage.css";

export default function MatchesTablePage() {
  const location = useLocation();
  const navigate = useNavigate();
  const { matches = [], requestId = "", requestData = {} } = location.state || {};
  const [sortConfig, setSortConfig] = useState({ key: null, direction: "asc" });

  if (!matches || matches.length === 0) {
    return (
      <div className="matches-page">
        <div className="no-matches">
          <h2>No Data Available</h2>
          <p>No matching donors were found or the data expired.</p>
          <button className="btn btn-primary" onClick={() => navigate("/request")}>
            Create New Request
          </button>
        </div>
      </div>
    );
  }

  const handleSort = (key) => {
    let direction = "asc";
    if (sortConfig.key === key && sortConfig.direction === "asc") {
      direction = "desc";
    }
    setSortConfig({ key, direction });
  };

  const getSortedMatches = () => {
    let sorted = [...matches];
    if (!sortConfig.key) return sorted;

    sorted.sort((a, b) => {
      let aVal, bVal;

      switch (sortConfig.key) {
        case "name":
          aVal = a.name || "";
          bVal = b.name || "";
          break;
        case "distance":
          aVal = a.distance_km || 0;
          bVal = b.distance_km || 0;
          break;
        case "score":
          aVal = a.ml_score || 0;
          bVal = b.ml_score || 0;
          break;
        default:
          return 0;
      }

      if (typeof aVal === "string") {
        aVal = aVal.toLowerCase();
        bVal = bVal.toLowerCase();
      }

      if (aVal < bVal) return sortConfig.direction === "asc" ? -1 : 1;
      if (aVal > bVal) return sortConfig.direction === "asc" ? 1 : -1;
      return 0;
    });

    return sorted;
  };

  const getScoreBadge = (score) => {
    if (score >= 0.8) return "🟢 Excellent";
    if (score >= 0.6) return "🟡 Good";
    return "🔴 Fair";
  };

  const getScoreColor = (score) => {
    if (score >= 0.8) return "#28a745";
    if (score >= 0.6) return "#ffc107";
    return "#dc3545";
  };

  const formatDate = (dateStr) => {
    try {
      return new Date(dateStr).toLocaleDateString();
    } catch {
      return "N/A";
    }
  };

  const sortedMatches = getSortedMatches();
  const SortIcon = ({ column }) => {
    if (sortConfig.key !== column) return "";
    return sortConfig.direction === "asc" ? " ↑" : " ↓";
  };

  return (
    <div className="matches-page">
      <div className="matches-header">
        <div className="header-content">
          <h1>🩸 Donor Matches ({matches.length})</h1>
          <p className="request-info">
            Request: <strong>{requestData.blood_group_required}</strong> | 
            ID: <code>{requestId.substring(0, 8)}...</code>
          </p>
        </div>
      </div>

      <div className="table-wrapper">
        <table className="matches-table">
          <thead>
            <tr>
              <th style={{ textAlign: "center", width: "60px" }}>Rank</th>
              <th onClick={() => handleSort("name")} style={{ cursor: "pointer" }}>
                Donor Name<SortIcon column="name" />
              </th>
              <th style={{ textAlign: "center" }}>Age</th>
              <th style={{ textAlign: "center" }}>Blood</th>
              <th 
                onClick={() => handleSort("distance")} 
                style={{ textAlign: "right", paddingRight: "20px", cursor: "pointer" }}
              >
                Distance<SortIcon column="distance" />
              </th>
              <th 
                onClick={() => handleSort("score")} 
                style={{ textAlign: "center", cursor: "pointer" }}
              >
                Score<SortIcon column="score" />
              </th>
              <th style={{ textAlign: "center" }}>Quality</th>
              <th style={{ textAlign: "center" }}>Contact</th>
              <th style={{ textAlign: "center" }}>Health</th>
              <th style={{ textAlign: "center" }}>Last Donation</th>
            </tr>
          </thead>
          <tbody>
            {sortedMatches.map((match, idx) => (
              <tr key={match.donor_id} className={idx < 2 ? "top-match" : ""}>
                <td style={{ textAlign: "center" }}>
                  <span className={`rank-badge ${idx < 2 ? "top" : ""}`}>
                    {idx < 2 ? `🏆 #${idx + 1}` : `#${idx + 1}`}
                  </span>
                </td>
                <td className="name-cell">{match.name}</td>
                <td style={{ textAlign: "center" }}>{match.age}</td>
                <td style={{ textAlign: "center", fontWeight: "600", color: "#c41e3a" }}>
                  {match.blood_group}
                </td>
                <td style={{ textAlign: "right", paddingRight: "20px" }}>
                  {match.distance_km.toFixed(2)} km
                </td>
                <td style={{ textAlign: "center" }}>
                  <span 
                    className="score-pill"
                    style={{ background: getScoreColor(match.ml_score) }}
                  >
                    {(match.ml_score * 100).toFixed(0)}%
                  </span>
                </td>
                <td style={{ textAlign: "center" }}>{getScoreBadge(match.ml_score)}</td>
                <td style={{ textAlign: "center" }}>
                  <button 
                    className="btn-contact-donor"
                    onClick={() => alert(`Contacting: ${match.name}\nPhone: ${match.contact_number}`)}
                    title={match.contact_number}
                  >
                    📞
                  </button>
                </td>
                <td style={{ textAlign: "center" }}>
                  {match.health_eligible ? (
                    <span className="status-eligible">✅ Yes</span>
                  ) : (
                    <span className="status-ineligible">❌ No</span>
                  )}
                </td>
                <td style={{ textAlign: "center", fontSize: "0.85rem" }}>
                  {formatDate(match.last_donation_date)}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="footer-actions">
        <button className="btn btn-secondary" onClick={() => navigate("/request")}>
          Create New Request
        </button>
      </div>
    </div>
  );
}
