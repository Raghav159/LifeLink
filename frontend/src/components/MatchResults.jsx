import { useState } from "react";
import API from "../services/api";
import DonorDetailsModal from "./DonorDetailsModal";
import "./MatchResults.css";

export default function MatchResults() {
  const [requestId, setRequestId] = useState("");
  const [matches, setMatches] = useState([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [searched, setSearched] = useState(false);
  const [selectedDonor, setSelectedDonor] = useState(null);

  const handleSearch = async (e) => {
    e.preventDefault();
    setError("");
    setMatches([]);
    setLoading(true);
    setSearched(true);

    if (!requestId.trim()) {
      setError("Please enter a valid Request ID");
      setLoading(false);
      return;
    }

    try {
      const response = await API.get(`/match/${requestId}`);
      
      // The response is directly a list of matches
      const matchList = Array.isArray(response.data) ? response.data : response.data.matches || [];
      setMatches(matchList);
      
      if (matchList.length === 0) {
        setError("No matching donors found for this request.");
      }
    } catch (err) {
      setError(`❌ Error: ${err.response?.data?.detail || "Request not found"}`);
      setMatches([]);
    } finally {
      setLoading(false);
    }
  };

  const getScoreColor = (score) => {
    if (score >= 0.8) return "#28a745";
    if (score >= 0.6) return "#ffc107";
    return "#dc3545";
  };

  const getScoreBadge = (score) => {
    if (score >= 0.8) return "Excellent";
    if (score >= 0.6) return "Good";
    return "Fair";
  };

  return (
    <div className="match-container">
      <h1>Find Matching Donors</h1>

      <form onSubmit={handleSearch} className="search-form">
        <input
          type="text"
          value={requestId}
          onChange={(e) => setRequestId(e.target.value)}
          placeholder="Enter Request ID (e.g., 1)"
          className="search-input"
        />
        <button type="submit" className="btn btn-search" disabled={loading}>
          {loading ? "Searching..." : "Find Matches"}
        </button>
      </form>

      {error && <div className="alert alert-error">{error}</div>}

      {searched && matches.length > 0 && (
        <div className="results">
          <h2>✅ Found {matches.length} Matching Donor(s)</h2>
          
          <div className="matches-grid">
            {matches.map((match, idx) => (
              <div key={match.donor_id} className={`match-card ${idx < 3 ? 'top-match' : ''}`}>
                {idx < 3 && <span className="badge">🏆 Top {idx + 1}</span>}
                
                <div className="card-header">
                  <h3>{match.name || "Anonymous Donor"}</h3>
                  <div 
                    className="score-circle"
                    style={{ background: getScoreColor(match.ml_score) }}
                  >
                    {(match.ml_score * 100).toFixed(0)}%
                  </div>
                </div>

                <div className="card-body">
                  <div className="info-row">
                    <span className="label">Blood Type:</span>
                    <span className="value">{match.blood_group}</span>
                  </div>
                  <div className="info-row">
                    <span className="label">Distance:</span>
                    <span className="value">{match.distance_km.toFixed(2)} km</span>
                  </div>
                  <div className="info-row">
                    <span className="label">ML Score:</span>
                    <span className="value">{(match.ml_score * 100).toFixed(1)}%</span>
                  </div>
                  <div className="info-row">
                    <span className="label">Match Quality:</span>
                    <span className="value">{getScoreBadge(match.ml_score)}</span>
                  </div>
                </div>

                <div className="card-footer">
                  <button className="btn btn-contact" onClick={() => setSelectedDonor(match)}>
                    📞 Contact Donor
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {searched && matches.length === 0 && !error && (
        <div className="empty-state">
          <p>🔍 No donors found. Try adjusting your search criteria.</p>
        </div>
      )}

      <DonorDetailsModal 
        donor={selectedDonor} 
        onClose={() => setSelectedDonor(null)} 
      />
    </div>
  );
}
