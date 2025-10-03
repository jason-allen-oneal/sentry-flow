"use client";
import { useState } from "react";
import { createIndicator } from "../../lib/api";

export default function SubmitPage() {
  const [value, setValue] = useState("");
  const [type, setType] = useState("ip");
  const [tags, setTags] = useState("");
  const [resp, setResp] = useState<any>(null);

  const handleSubmit = async () => {
    const res = await createIndicator({ type, value, tags: tags.split(",") });
    setResp(res);
  };

  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Submit IOC</h1>
      <div className="space-y-4">
        <input
          className="bg-slate-800 p-2 rounded w-full"
          placeholder="Indicator value (e.g. 8.8.8.8)"
          value={value}
          onChange={(e) => setValue(e.target.value)}
        />
        <select
          className="bg-slate-800 p-2 rounded"
          value={type}
          onChange={(e) => setType(e.target.value)}
        >
          <option value="ip">IP</option>
          <option value="domain">Domain</option>
          <option value="url">URL</option>
          <option value="hash_sha256">SHA256</option>
        </select>
        <input
          className="bg-slate-800 p-2 rounded w-full"
          placeholder="Tags (comma-separated)"
          value={tags}
          onChange={(e) => setTags(e.target.value)}
        />
        <button
          className="bg-cyan-600 px-4 py-2 rounded hover:bg-cyan-500"
          onClick={handleSubmit}
        >
          Submit
        </button>
      </div>
      {resp && (
        <pre className="mt-6 bg-slate-900 p-4 rounded text-sm">
          {JSON.stringify(resp, null, 2)}
        </pre>
      )}
    </div>
  );
}
