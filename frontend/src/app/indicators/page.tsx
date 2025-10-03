"use client";
import { useEffect, useState } from "react";
import { getIndicators } from "../../lib/api";

export default function IndicatorsPage() {
  const [data, setData] = useState<any[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    getIndicators()
      .then((res) => {
        if (Array.isArray(res)) {
          setData(res);
        } else {
          setError(JSON.stringify(res));
        }
      })
      .catch((err) => setError(err.message));
  }, []);

  if (error) {
    return (
      <div className="text-red-400">
        Failed to load indicators: {error}
      </div>
    );
  }

  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Indicators</h1>
      <table className="w-full text-left border-collapse">
        <thead className="bg-slate-800">
          <tr>
            <th className="p-2">Type</th>
            <th className="p-2">Value</th>
            <th className="p-2">Score</th>
            <th className="p-2">Tags</th>
            <th className="p-2">Country</th>
          </tr>
        </thead>
        <tbody>
          {data.map((ind) => (
            <tr key={ind.id} className="border-b border-slate-800">
              <td className="p-2">{ind.type}</td>
              <td className="p-2">{ind.canonical_value}</td>
              <td className="p-2">{ind.score}</td>
              <td className="p-2">{ind.tags.join(", ")}</td>
              <td className="p-2">{ind.country}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
