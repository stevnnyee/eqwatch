import { useEffect, useState } from "react";

const API = "http://localhost:8000";

export default function Earthquakes() {
  const [earthquakes, setEarthquakes] = useState([]);

  useEffect(() => {
    fetch(`${API}/earthquakes`)
      .then((r) => r.json())
      .then(setEarthquakes);
  }, []);

  return (
    <div>
      <h2 className="text-xl font-semibold mb-4">Earthquakes ({earthquakes.length})</h2>
      <div className="overflow-auto max-h-[70vh] rounded border border-gray-200">
        <table className="min-w-full text-sm">
          <thead className="bg-gray-100 sticky top-0">
            <tr>
              <th className="px-4 py-2 text-left">ID</th>
              <th className="px-4 py-2 text-left">Magnitude</th>
              <th className="px-4 py-2 text-left">Depth (km)</th>
              <th className="px-4 py-2 text-left">Latitude</th>
              <th className="px-4 py-2 text-left">Longitude</th>
              <th className="px-4 py-2 text-left">Location</th>
              <th className="px-4 py-2 text-left">Occurred At</th>
            </tr>
          </thead>
          <tbody>
            {earthquakes.map((eq) => (
              <tr key={eq.eq_id} className="border-t border-gray-100 hover:bg-gray-50">
                <td className="px-4 py-2">{eq.eq_id}</td>
                <td className="px-4 py-2">{eq.magnitude}</td>
                <td className="px-4 py-2">{eq.depth}</td>
                <td className="px-4 py-2">{eq.latitude}</td>
                <td className="px-4 py-2">{eq.longitude}</td>
                <td className="px-4 py-2">{eq.location_name}</td>
                <td className="px-4 py-2">{new Date(eq.occurred_at + "Z").toLocaleString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
