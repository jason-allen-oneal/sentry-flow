"use client";
import { useState } from "react";

export default function FeedsPage() {
  const [tag, setTag] = useState("");
  const [minScore, setMinScore] = useState(50);

  const jsonUrl = `http://127.0.0.1:8000/feeds?min_score=${minScore}${
    tag ? `&tag=${tag}` : ""
  }`;
  const stixUrl = `http://127.0.0.1:8000/feeds/stix?min_score=${minScore}${
    tag ? `&tag=${tag}` : ""
  }`;

  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Feeds</h1>
      <div className="space-y-4">
        <input
          className="bg-slate-800 p-2 rounded w-full"
          placeholder="Filter by tag (optional)"
          value={tag}
          onChange={(e) => setTag(e.target.value)}
        />
        <input
          type="number"
          className="bg-slate-800 p-2 rounded w-full"
          value={minScore}
          onChange={(e) => setMinScore(Number(e.target.value))}
        />
        <div className="mt-4 space-y-2">
          <p>JSON Feed:</p>
          <code className="block bg-slate-900 p-2 rounded">{jsonUrl}</code>
          <p>STIX Feed:</p>
          <code className="block bg-slate-900 p-2 rounded">{stixUrl}</code>
        </div>
      </div>
    </div>
  );
}
