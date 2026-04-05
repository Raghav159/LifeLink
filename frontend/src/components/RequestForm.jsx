import { useState } from "react";
import { useNavigate } from "react-router-dom";
import API from "../services/api";
import MapPicker from "./MapPicker";
import "./Form.css";

export default function RequestForm() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    patient_name: "",
    blood_group_required: "",
    urgency_level: "MEDIUM",
    quantity: "450",
    latitude: "",
    longitude: "",
    patient_age: "",
  });

  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setSuccess("");
    setLoading(true);

    // Validate form
    if (!formData.patient_name || !formData.blood_group_required ||
        formData.latitude === "" || formData.longitude === "" || 
        !formData.patient_age) {
      setError("Please fill all fields and select a location on the map");
      setLoading(false);
      return;
    }

    try {
      // Get current hour automatically
      const currentHour = new Date().getHours();

      // Create request
      const response = await API.post("/requests/", {
        blood_group_required: formData.blood_group_required,
        urgency_level: formData.urgency_level,
        quantity: parseInt(formData.quantity),
        latitude: parseFloat(formData.latitude),
        longitude: parseFloat(formData.longitude),
        patient_age: parseInt(formData.patient_age),
        request_hour: currentHour,
      });

      const newRequestId = response.data.id;
      setSuccess(`✅ Request created! Fetching matching donors...`);
      
      // Automatically fetch matches
      try {
        const matchResponse = await API.get(`/match/${newRequestId}`);
        const matchList = Array.isArray(matchResponse.data) ? matchResponse.data : [];
        
        if (matchList.length === 0) {
          setError("No matching donors found at this moment.");
        }
        
        // Navigate to matches page with data
        navigate("/matches", { 
          state: { 
            matches: matchList, 
            requestId: newRequestId,
            requestData: formData
          } 
        });
      } catch (matchErr) {
        console.error("Error fetching matches:", matchErr);
        setError(`Request created, but could not fetch matches: ${matchErr.response?.data?.detail || matchErr.message}`);
      }

      // Reset form
      setFormData({
        patient_name: "",
        blood_group_required: "",
        urgency_level: "MEDIUM",
        quantity: "450",
        latitude: "",
        longitude: "",
        patient_age: "",
      });
    } catch (err) {
      setError(`❌ Error: ${err.response?.data?.detail || err.message}`);
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
    if (score >= 0.8) return "🟢 Excellent";
    if (score >= 0.6) return "🟡 Good";
    return "🔴 Fair";
  };

  return (
    <div className="form-container">
      <h1>Create Blood Request</h1>

      {error && <div className="alert alert-error">{error}</div>}
      {success && (
        <div className="alert alert-success">
          {success}
        </div>
      )}

      <form onSubmit={handleSubmit} className="form">
        <div className="form-group">
          <label>Patient Name (Optional)</label>
          <input
            type="text"
            name="patient_name"
            value={formData.patient_name}
            onChange={handleChange}
            placeholder="Enter patient name (optional)"
          />
        </div>

        <div className="form-group">
          <label>Blood Type Needed *</label>
          <select
            name="blood_group_required"
            value={formData.blood_group_required}
            onChange={handleChange}
            required
          >
            <option value="">Select Blood Type</option>
            <option value="O+">O+</option>
            <option value="O-">O-</option>
            <option value="A+">A+</option>
            <option value="A-">A-</option>
            <option value="B+">B+</option>
            <option value="B-">B-</option>
            <option value="AB+">AB+</option>
            <option value="AB-">AB-</option>
          </select>
        </div>

        <div className="form-group">
          <label>Urgency Level *</label>
          <select
            name="urgency_level"
            value={formData.urgency_level}
            onChange={handleChange}
          >
            <option value="LOW">Low</option>
            <option value="MEDIUM">Medium</option>
            <option value="HIGH">High</option>
          </select>
        </div>

        <div className="form-group">
          <label>Quantity (ML) *</label>
          <input
            type="number"
            name="quantity"
            value={formData.quantity}
            onChange={handleChange}
            placeholder="Enter quantity in ML"
            min="300"
            max="600"
            required
          />
        </div>

        <div className="form-group">
          <label>Patient Age *</label>
          <input
            type="number"
            name="patient_age"
            value={formData.patient_age}
            onChange={handleChange}
            placeholder="Enter patient age"
            min="1"
            max="120"
            required
          />
        </div>

        <MapPicker 
          setLat={(lat) => setFormData((prev) => ({ ...prev, latitude: lat }))}
          setLng={(lng) => setFormData((prev) => ({ ...prev, longitude: lng }))}
          label="Select Hospital/Location"
        />

        <button type="submit" className="btn btn-primary" disabled={loading}>
          {loading ? "Creating Request & Finding Matches..." : "Create Request"}
        </button>
      </form>
    </div>
  );
}
