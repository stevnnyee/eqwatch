import { useEffect, useState } from "react";

const API = "http://localhost:8000";

export default function Users() {
  const [users, setUsers] = useState([]);
  const [form, setForm] = useState({ first_name: "", last_name: "", email: "", password: "" });
  const [error, setError] = useState("");

  function loadUsers() {
    fetch(`${API}/users`)
      .then((r) => r.json())
      .then(setUsers);
  }

  useEffect(() => { loadUsers(); }, []);

  function handleSubmit(e) {
    e.preventDefault();
    setError("");
    fetch(`${API}/users`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(form),
    })
      .then((r) => {
        if (!r.ok) throw new Error("Failed to create user");
        return r.json();
      })
      .then(() => {
        setForm({ first_name: "", last_name: "", email: "", password: "" });
        loadUsers();
      })
      .catch((err) => setError(err.message));
  }

  function handleDelete(id) {
    fetch(`${API}/users/${id}`, { method: "DELETE" }).then(loadUsers);
  }

  return (
    <div>
      <h2 className="text-xl font-semibold mb-4">Users</h2>

      <form onSubmit={handleSubmit} className="mb-6 grid grid-cols-2 gap-3 max-w-lg">
        {["first_name", "last_name", "email", "password"].map((field) => (
          <input
            key={field}
            className="border rounded px-3 py-2 text-sm"
            placeholder={field.replace("_", " ")}
            type={field === "password" ? "password" : "text"}
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
          Add User
        </button>
      </form>

      <table className="min-w-full text-sm border border-gray-200 rounded">
        <thead className="bg-gray-100">
          <tr>
            <th className="px-4 py-2 text-left">ID</th>
            <th className="px-4 py-2 text-left">First Name</th>
            <th className="px-4 py-2 text-left">Last Name</th>
            <th className="px-4 py-2 text-left">Email</th>
            <th className="px-4 py-2 text-left">Created At</th>
            <th className="px-4 py-2"></th>
          </tr>
        </thead>
        <tbody>
          {users.map((u) => (
            <tr key={u.user_id} className="border-t border-gray-100 hover:bg-gray-50">
              <td className="px-4 py-2">{u.user_id}</td>
              <td className="px-4 py-2">{u.first_name}</td>
              <td className="px-4 py-2">{u.last_name}</td>
              <td className="px-4 py-2">{u.email}</td>
              <td className="px-4 py-2">{new Date(u.created_at).toLocaleString()}</td>
              <td className="px-4 py-2">
                <button
                  onClick={() => handleDelete(u.user_id)}
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
