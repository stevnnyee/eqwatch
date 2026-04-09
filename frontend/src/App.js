import { useState } from "react";
import Earthquakes from "./pages/Earthquakes";
import Regions from "./pages/Regions";
import Alerts from "./pages/Alerts";
import Users from "./pages/Users";

const TABS = ["Earthquakes", "Users", "Regions", "Alerts"];

export default function App() {
  const [active, setActive] = useState("Earthquakes");

  const page = {
    Earthquakes: <Earthquakes />,
    Users: <Users />,
    Regions: <Regions />,
    Alerts: <Alerts />,
  }[active];

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white border-b border-gray-200 px-6 py-4 flex items-center gap-6">
        <span className="font-bold text-lg tracking-tight">EQWatch</span>
        <div className="flex gap-4">
          {TABS.map((tab) => (
            <button
              key={tab}
              onClick={() => setActive(tab)}
              className={`text-sm px-3 py-1 rounded ${
                active === tab
                  ? "bg-blue-600 text-white"
                  : "text-gray-600 hover:text-gray-900"
              }`}
            >
              {tab}
            </button>
          ))}
        </div>
      </nav>
      <main className="p-6">{page}</main>
    </div>
  );
}
