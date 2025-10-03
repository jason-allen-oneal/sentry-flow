export default function Dashboard() {
  return (
    <div>
      <h1 className="text-3xl font-bold mb-4">SentryFlow Dashboard</h1>
      <p className="text-slate-400">
        Welcome to SentryFlow — your threat intel sharing platform.
      </p>
      <ul className="mt-6 space-y-2">
        <li>🚀 Submit Indicators</li>
        <li>🔍 Browse/Search IOC database</li>
        <li>📦 Group into Intel Packages</li>
        <li>📡 Export JSON/STIX feeds</li>
        <li>🔑 Manage API keys</li>
        <li>⚡ Setup alerts</li>
      </ul>
    </div>
  );
}
