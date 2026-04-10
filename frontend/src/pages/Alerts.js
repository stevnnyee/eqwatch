import { useEffect, useState } from "react";

const API = "http://localhost:8000";

export default function Alerts() {
  const [alerts, setAlerts] = useState([]);
  const [form, setForm] = useState({ user_id: "", eq_id: "" });
  const [error, setError] = useState("");

  function loadAlerts() {
    fetch(`${API}/alerts`)
      .then((r) => r.json())
      .then(setAlerts);
  }

  useEffect(() => { loadAlerts(); }, []);

  function handleSubmit(e) {
    e.preventDefault();
    setError("");
    fetch(`${API}/alerts`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        user_id: parseInt(form.user_id),
        eq_id: parseInt(form.eq_id),
      }),
    })
      .then((r) => {
        if (!r.ok) throw new Error("Failed to create alert");
        return r.json();
      })
      .then(() => {
        setForm({ user_id: "", eq_id: "" });
        loadAlerts();
      })
      .catch((err) => setError(err.message));
  }

  function handleDelete(id) {
    fetch(`${API}/alerts/${id}`, { method: "DELETE" }).then(loadAlerts);
  }

  return (
    <div>
      <h2 className="text-xl font-semibold mb-4">Alerts</h2>

      <form onSubmit={handleSubmit} className="mb-6 flex gap-3 items-end max-w-lg">
        <div className="flex flex-col gap-1">
          <label className="text-xs text-gray-500">User ID</label>
          <input
            className="border rounded px-3 py-2 text-sm w-28"
            placeholder="1"
            value={form.user_id}
            onChange={(e) => setForm({ ...form, user_id: e.target.value })}
            required
          />
        </div>
        <div className="flex flex-col gap-1">
          <label className="text-xs text-gray-500">Earthquake ID</label>
          <input
            className="border rounded px-3 py-2 text-sm w-28"
            placeholder="1"
            value={form.eq_id}
            onChange={(e) => setForm({ ...form, eq_id: e.target.value })}
            required
          />
        </div>
        <button
          type="submit"
          className="bg-blue-600 text-white rounded px-4 py-2 text-sm hover:bg-blue-700"
        >
          Create Alert
        </button>
        {error && <p className="text-red-500 text-sm">{error}</p>}
      </form>

      <table className="min-w-full text-sm border border-gray-200 rounded">
        <thead className="bg-gray-100">
          <tr>
            <th className="px-4 py-2 text-left">Alert ID</th>
            <th className="px-4 py-2 text-left">User ID</th>
            <th className="px-4 py-2 text-left">Earthquake ID</th>
            <th className="px-4 py-2 text-left">Sent At</th>
            <th className="px-4 py-2"></th>
          </tr>
        </thead>
        <tbody>
          {alerts.map((a) => (
            <tr key={a.alert_id} className="border-t border-gray-100 hover:bg-gray-50">
              <td className="px-4 py-2">{a.alert_id}</td>
              <td className="px-4 py-2">{a.user_id}</td>
              <td className="px-4 py-2">{a.eq_id}</td>
              <td className="px-4 py-2">{new Date(a.sent_at + "Z").toLocaleString()}</td>
              <td className="px-4 py-2">
                <button
                  onClick={() => handleDelete(a.alert_id)}
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
