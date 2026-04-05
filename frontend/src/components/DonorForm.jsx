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
      
      {error && <div className="alert alert-error">{error}</div>}
      {success && <div className="alert alert-success">{success}</div>}

      <form onSubmit={handleSubmit} className="form">
        <div className="form-group">
          <label>Full Name *</label>
          <input
            type="text"
            name="name"
            value={formData.name}
            onChange={handleChange}
            placeholder="Enter your full name"
            required
          />
        </div>

        <div className="form-group">
          <label>Blood Type *</label>
          <select
            name="blood_group"
            value={formData.blood_group}
            onChange={handleChange}
            required
          >
            <option value="">Select Blood Type</option>
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
          <label>Age *</label>
          <input
            type="number"
            name="age"
            value={formData.age}
            onChange={handleChange}
            placeholder="Enter your age"
            min="18"
            max="65"
            required
          />
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

        <div className="form-group">
          <label>Contact Number *</label>
          <input
            type="tel"
            name="contact_number"
            value={formData.contact_number}
            onChange={handleChange}
            placeholder="Enter your contact number"
            required
          />
        </div>

        <MapPicker 
          setLat={(lat) => setFormData((prev) => ({ ...prev, latitude: lat }))}
          setLng={(lng) => setFormData((prev) => ({ ...prev, longitude: lng }))}
          label="Select Your Location"
        />

        <button type="submit" className="btn btn-primary" disabled={loading}>
          {loading ? "Registering..." : "Register as Donor"}
        </button>
      </form>
    </div>
  );
}
