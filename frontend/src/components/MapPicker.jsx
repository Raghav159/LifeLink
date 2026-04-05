import { MapContainer, TileLayer, Marker, useMapEvents, Popup, useMap } from "react-leaflet";
import { useState, useEffect } from "react";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import "./MapPicker.css";

// Fix default marker icon
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png",
  iconUrl: "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png",
  shadowUrl: "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png",
});

function LocationMarker({ setPosition, position }) {
  useMapEvents({
    click(e) {
      // Capture exact click coordinates
      const newPos = {
        lat: parseFloat(e.latlng.lat.toFixed(6)),
        lng: parseFloat(e.latlng.lng.toFixed(6))
      };
      setPosition(newPos);
    },
  });

  return position ? (
    <Marker 
      position={[parseFloat(position.lat), parseFloat(position.lng)]}
      title={`${position.lat.toFixed(6)}, ${position.lng.toFixed(6)}`}
    >
      <Popup>
        <strong>Selected Location</strong><br/>
        Lat: {parseFloat(position.lat).toFixed(6)}<br/>
        Lng: {parseFloat(position.lng).toFixed(6)}
      </Popup>
    </Marker>
  ) : null;
}

function MapUpdater({ position }) {
  const map = useMap();

  useEffect(() => {
    if (position) {
      // Fly to the position with animation
      map.flyTo([position.lat, position.lng], 15, {
        duration: 1.5
      });
      // Invalidate size to ensure map renders correctly
      map.invalidateSize();
    }
  }, [position, map]);

  return null;
}

function GeolocationButton({ onLocationFound }) {
  const [loading, setLoading] = useState(false);
  
  const getMyLocation = (e) => {
    console.log("🔵 Get My Location clicked");
    
    if (!navigator.geolocation) {
      console.error("❌ Geolocation not supported");
      alert("❌ Geolocation is not supported by your browser");
      return;
    }
    
    console.log("🟢 Requesting HIGH-ACCURACY GPS (30 second wait for satellite lock)...");
    setLoading(true);
    
    if (e && e.target) {
      e.target.disabled = true;
      e.target.textContent = "📍 Acquiring GPS... (this takes 10-30s)";
    }
    
    // Start fresh - clear any cached position by small delay
    setTimeout(() => {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          console.log("✅ GPS position received:", position);
          const { latitude, longitude, accuracy } = position.coords;
          
          // Log accuracy for debugging
          if (accuracy) {
            console.log(`✅ GPS Accuracy: ${Math.round(accuracy)}m`);
            if (accuracy > 100) {
              console.warn("⚠️ Warning: Accuracy is poor (>100m). This might be WiFi/IP triangulation, not GPS.");
            } else if (accuracy <= 10) {
              console.log("🟢 Excellent GPS accuracy!");
            }
          }
          
          const latlng = { 
            lat: parseFloat(latitude.toFixed(6)), 
            lng: parseFloat(longitude.toFixed(6)) 
          };
          
          console.log("🎯 Location found:", latlng, "Accuracy:", Math.round(accuracy), "m");
          onLocationFound(latlng);
          setLoading(false);
          
          if (e && e.target) {
            e.target.disabled = false;
            e.target.textContent = `✅ Location Found! (${Math.round(accuracy)}m accuracy)`;
            setTimeout(() => {
              if (e.target) {
                e.target.textContent = "📍 Get My Location";
              }
            }, 3000);
          }
        },
        (error) => {
          console.error("❌ GPS Error:", error);
          let errorMsg = error.message;
          switch(error.code) {
            case error.PERMISSION_DENIED:
              errorMsg = "Location permission denied. Enable in browser settings.";
              break;
            case error.POSITION_UNAVAILABLE:
              errorMsg = "Location service unavailable. Try clicking on the map instead.";
              break;
            case error.TIMEOUT:
              errorMsg = "GPS timeout (took >30s). Try clicking on the map for manual location.";
              break;
            default:
              errorMsg = "Could not get location.";
          }
          console.error("Error details:", errorMsg);
          alert("❌ " + errorMsg);
          setLoading(false);
          
          if (e && e.target) {
            e.target.disabled = false;
            e.target.textContent = "📍 Get My Location";
          }
        },
        {
          enableHighAccuracy: true,  // ✅ FORCE GPS - reject WiFi/IP triangulation
          timeout: 30000,            // ✅ Wait up to 30 seconds for satellite lock
          maximumAge: 0              // ✅ Don't use cached location - always fresh
        }
      );
    }, 100);
  };

  return (
    <button 
      type="button" 
      className="btn-geolocation"
      onClick={getMyLocation}
      disabled={loading}
      title="Get your current location with high accuracy GPS"
    >
      📍 Get My Location
    </button>
  );
}

export default function MapPicker({ setLat, setLng, label = "Select Location on Map", initialLat = null, initialLng = null }) {
  const [position, setPosition] = useState(
    initialLat && initialLng ? { lat: initialLat, lng: initialLng } : null
  );

  const handlePositionChange = (pos) => {
    const precisePos = {
      lat: parseFloat(pos.lat),
      lng: parseFloat(pos.lng)
    };
    setPosition(precisePos);
    setLat(precisePos.lat);
    setLng(precisePos.lng);
  };

  const handleLocationFound = (latlng) => {
    handlePositionChange(latlng);
  };

  return (
    <div className="map-picker">
      <div className="map-header">
        <label className="map-label">{label}</label>
        <div className="map-wrapper">
          <MapContainer center={position ? [position.lat, position.lng] : [12.97, 77.59]} zoom={13} className="map-container">
            <TileLayer
              url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
              attribution='&copy; OpenStreetMap contributors'
            />
            <LocationMarker setPosition={handlePositionChange} position={position} />
            <MapUpdater position={position} />
          </MapContainer>
          <GeolocationButton onLocationFound={handleLocationFound} />
        </div>
      </div>
      {position && (
        <div className="map-info">
          <p>📍 Latitude: {parseFloat(position.lat).toFixed(6)}</p>
          <p>📍 Longitude: {parseFloat(position.lng).toFixed(6)}</p>
        </div>
      )}
    </div>
  );
}
