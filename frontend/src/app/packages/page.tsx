"use client";
import { useEffect, useState } from "react";
import { getPackages } from "../../lib/api";

export default function PackagesPage() {
  const [packages, setPackages] = useState<any[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    getPackages()
      .then((res) => {
        if (Array.isArray(res)) setPackages(res);
        else setError(JSON.stringify(res));
      })
      .catch((err) => setError(err.message));
  }, []);

  if (error) {
    return <div className="text-red-400">Error: {error}</div>;
  }

  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Intel Packages</h1>
      {packages.length === 0 && (
        <p className="text-slate-400">No intel packages yet.</p>
      )}
      <div className="grid gap-4">
        {packages.map((pkg) => (
          <div key={pkg.id} className="bg-slate-900 p-4 rounded shadow">
            <h2 className="text-xl font-semibold">{pkg.title}</h2>
            <p className="text-slate-400">{pkg.summary}</p>
            <p className="mt-2 text-sm">
              Techniques: {pkg.techniques.join(", ") || "None"}
            </p>
            <p className="text-sm">Indicators: {pkg.indicators.length}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
