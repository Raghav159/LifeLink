import { useState } from "react";
import API from "../services/api";
import MapPicker from "./MapPicker";
import "./Form.css";

export default function DonorForm() {
  const [formData, setFormData] = useState({
    name: "",
    blood_group: "",
    age: "",
    latitude: "",
    longitude: "",
    contact_number: "",
    last_donation_date: "",
  });

  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [loading, setLoading] = useState(false);

  const requiredFields = [
    formData.name,
    formData.blood_group,
    formData.age,
    formData.latitude,
    formData.longitude,
    formData.contact_number,
    formData.last_donation_date,
  ];
  const completion = Math.round((requiredFields.filter(Boolean).length / requiredFields.length) * 100);

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
    if (!formData.name || !formData.blood_group || !formData.age ||
        formData.latitude === "" || formData.longitude === "" || 
        !formData.contact_number || !formData.last_donation_date) {
      setError("Please fill all fields and select a location on the map");
      setLoading(false);
      return;
    }

    try {
      const response = await API.post("/donors/", {
        name: formData.name,
        blood_group: formData.blood_group,
        age: parseInt(formData.age),
        latitude: parseFloat(formData.latitude),
        longitude: parseFloat(formData.longitude),
        contact_number: formData.contact_number,
        last_donation_date: formData.last_donation_date,
      });

      setSuccess(`✅ Donor registered successfully! ID: ${response.data.id}`);
      setFormData({
        name: "",
        blood_group: "",
        age: "",
        latitude: "",
        longitude: "",
        contact_number: "",
        last_donation_date: "",
      });
      setTimeout(() => setSuccess(""), 5000);
    } catch (err) {
      setError(`❌ Error: ${err.response?.data?.detail || err.message}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="form-container">
      <h1>Register as Donor</h1>

      <div className="form-layout">
        <div>
          {error && <div className="alert alert-error">{error}</div>}
          {success && <div className="alert alert-success">{success}</div>}

          <form onSubmit={handleSubmit} className="form">
            <section className="form-block glass surface-card">
              <h2>Personal Info</h2>
              <div className="form-group">
                <label>Full Name *</label>
                <input
                  type="text"
                  name="name"
                  value={formData.name}
                  onChange={handleChange}
                  placeholder="e.g., Riya Sharma"
                  required
                />
              </div>

              <div className="form-group">
                <label>Contact Number *</label>
                <input
                  type="tel"
                  name="contact_number"
                  value={formData.contact_number}
                  onChange={handleChange}
                  placeholder="e.g., +91 98xxxxxx21"
                  required
                />
                <small className="field-hint">Used only for urgent contact during active requests.</small>
              </div>

              <div className="form-group">
                <label>Age *</label>
                <input
                  type="number"
                  name="age"
                  value={formData.age}
                  onChange={handleChange}
                  placeholder="18 to 65"
                  min="18"
                  max="65"
                  required
                />
              </div>
            </section>

            <section className="form-block glass surface-card">
              <h2>Medical Info</h2>
              <div className="form-group">
                <label>Blood Type *</label>
                <select
                  name="blood_group"
                  value={formData.blood_group}
                  onChange={handleChange}
                  required
                >
                  <option value="">Select blood type</option>
                  <option value="O+">O+</option>
                  <option value="O-">O- (Universal Donor)</option>
                  <option value="A+">A+</option>
                  <option value="A-">A-</option>
                  <option value="B+">B+</option>
                  <option value="B-">B-</option>
                  <option value="AB+">AB+</option>
                  <option value="AB-">AB-</option>
                </select>
              </div>

              <div className="form-group">
                <label>Last Donation Date *</label>
                <input
                  type="date"
                  name="last_donation_date"
                  value={formData.last_donation_date}
                  onChange={handleChange}
                  required
                />
              </div>
            </section>

            <section className="form-block glass surface-card">
              <h2>Location</h2>
              <MapPicker
                setLat={(lat) => setFormData((prev) => ({ ...prev, latitude: lat }))}
                setLng={(lng) => setFormData((prev) => ({ ...prev, longitude: lng }))}
                label="Pin your location to improve nearest-match ranking"
              />
            </section>

            <button type="submit" className="btn btn-primary" disabled={loading}>
              {loading ? "Registering donor..." : "Register as Donor"}
            </button>
          </form>
        </div>

        <aside className="form-summary glass surface-card">
          <h3>Live Summary</h3>
          <p>Profile completeness</p>
          <div className="summary-progress">
            <span style={{ width: `${completion}%` }} />
          </div>
          <p className="summary-value">{completion}% complete</p>
          <div className="summary-row">
            <span>Blood Group</span>
            <strong>{formData.blood_group || "Pending"}</strong>
          </div>
          <div className="summary-row">
            <span>Age</span>
            <strong>{formData.age || "--"}</strong>
          </div>
          <div className="summary-row">
            <span>Location</span>
            <span className={`chip ${formData.latitude && formData.longitude ? "chip-success" : "chip-warning"}`}>
              {formData.latitude && formData.longitude ? "Pinned" : "Pending"}
            </span>
          </div>
        </aside>
      </div>
    </div>
  );
}
