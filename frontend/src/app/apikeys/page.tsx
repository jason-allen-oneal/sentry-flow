"use client";
import { useState, useEffect } from "react";
import { createApiKey } from "@/lib/api";

export default function ApiKeysPage() {
  const [owner, setOwner] = useState("me");
  const [key, setKey] = useState<any>(null);

  const handleCreate = async () => {
    const res = await createApiKey(owner);
    setKey(res);
    if (res.key) {
      localStorage.setItem("apiKey", res.key);
    }
  };

  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">API Keys</h1>
      <div className="space-y-4">
        <input
          className="bg-slate-800 p-2 rounded"
          placeholder="Owner name"
          value={owner}
          onChange={(e) => setOwner(e.target.value)}
        />
        <button
          onClick={handleCreate}
          className="bg-cyan-600 px-4 py-2 rounded hover:bg-cyan-500"
        >
          Generate API Key
        </button>
        {key && (
          <pre className="mt-4 bg-slate-900 p-4 rounded text-sm">
            {JSON.stringify(key, null, 2)}
          </pre>
        )}
      </div>
    </div>
  );
}
