import { useEffect, useState } from "react";

const API = "http://localhost:8000";

export default function Regions() {
  const [regions, setRegions] = useState([]);
  const [form, setForm] = useState({ name: "", min_lat: "", max_lat: "", min_lon: "", max_lon: "" });
  const [error, setError] = useState("");

  function loadRegions() {
    fetch(`${API}/regions`)
      .then((r) => r.json())
      .then(setRegions);
  }

  useEffect(() => { loadRegions(); }, []);

  function handleSubmit(e) {
    e.preventDefault();
    setError("");
    fetch(`${API}/regions`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        name: form.name,
        min_lat: parseFloat(form.min_lat),
        max_lat: parseFloat(form.max_lat),
        min_lon: parseFloat(form.min_lon),
        max_lon: parseFloat(form.max_lon),
      }),
    })
      .then((r) => {
        if (!r.ok) throw new Error("Failed to create region");
        return r.json();
      })
      .then(() => {
        setForm({ name: "", min_lat: "", max_lat: "", min_lon: "", max_lon: "" });
        loadRegions();
      })
      .catch((err) => setError(err.message));
  }

  function handleDelete(id) {
    fetch(`${API}/regions/${id}`, { method: "DELETE" }).then(loadRegions);
  }

  return (
    <div>
      <h2 className="text-xl font-semibold mb-4">Regions</h2>

      <form onSubmit={handleSubmit} className="mb-6 grid grid-cols-2 gap-3 max-w-lg">
        <input
          className="col-span-2 border rounded px-3 py-2 text-sm"
          placeholder="Region name"
          value={form.name}
          onChange={(e) => setForm({ ...form, name: e.target.value })}
          required
        />
        {["min_lat", "max_lat", "min_lon", "max_lon"].map((field) => (
          <input
            key={field}
            className="border rounded px-3 py-2 text-sm"
            placeholder={field}
            value={form[field]}
            onChange={(e) => setForm({ ...form, [field]: e.target.value })}
            required
          />
        ))}
        {error && <p className="col-span-2 text-red-500 text-sm">{error}</p>}
        <button
          type="submit"
          className="col-span-2 bg-blue-600 text-white rounded px-4 py-2 text-sm hover:bg-blue-700"
        >
          Add Region
        </button>
      </form>

      <table className="min-w-full text-sm border border-gray-200 rounded">
        <thead className="bg-gray-100">
          <tr>
            <th className="px-4 py-2 text-left">ID</th>
            <th className="px-4 py-2 text-left">Name</th>
            <th className="px-4 py-2 text-left">Min Lat</th>
            <th className="px-4 py-2 text-left">Max Lat</th>
            <th className="px-4 py-2 text-left">Min Lon</th>
            <th className="px-4 py-2 text-left">Max Lon</th>
            <th className="px-4 py-2"></th>
          </tr>
        </thead>
        <tbody>
          {regions.map((r) => (
            <tr key={r.region_id} className="border-t border-gray-100 hover:bg-gray-50">
              <td className="px-4 py-2">{r.region_id}</td>
              <td className="px-4 py-2">{r.name}</td>
              <td className="px-4 py-2">{r.min_lat}</td>
              <td className="px-4 py-2">{r.max_lat}</td>
              <td className="px-4 py-2">{r.min_lon}</td>
              <td className="px-4 py-2">{r.max_lon}</td>
              <td className="px-4 py-2">
                <button
                  onClick={() => handleDelete(r.region_id)}
                  className="text-red-500 hover:underline text-xs"
                >
                  Delete
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
