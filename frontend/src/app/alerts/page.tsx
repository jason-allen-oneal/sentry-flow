"use client";
import { useState } from "react";
import { createAlert } from "@/lib/api";

export default function AlertsPage() {
  const [tag, setTag] = useState("");
  const [minScore, setMinScore] = useState(70);
  const [channel, setChannel] = useState("webhook");
  const [target, setTarget] = useState("");
  const [resp, setResp] = useState<any>(null);

  const handleCreate = async () => {
    const res = await createAlert({ tag, minScore, channel, target });
    setResp(res);
  };

  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Alerts</h1>
      <div className="space-y-4">
        <input
          className="bg-slate-800 p-2 rounded w-full"
          placeholder="Tag filter (optional)"
          value={tag}
          onChange={(e) => setTag(e.target.value)}
        />
        <input
          type="number"
          className="bg-slate-800 p-2 rounded w-full"
          placeholder="Minimum score"
          value={minScore}
          onChange={(e) => setMinScore(Number(e.target.value))}
        />
        <select
          className="bg-slate-800 p-2 rounded"
          value={channel}
          onChange={(e) => setChannel(e.target.value)}
        >
          <option value="webhook">Webhook</option>
          <option value="email">Email</option>
          <option value="discord">Discord</option>
        </select>
        <input
          className="bg-slate-800 p-2 rounded w-full"
          placeholder="Target URL or email"
          value={target}
          onChange={(e) => setTarget(e.target.value)}
        />
        <button
          onClick={handleCreate}
          className="bg-cyan-600 px-4 py-2 rounded hover:bg-cyan-500"
        >
          Create Alert
        </button>
        {resp && (
          <pre className="mt-6 bg-slate-900 p-4 rounded text-sm">
            {JSON.stringify(resp, null, 2)}
          </pre>
        )}
      </div>
    </div>
  );
}
