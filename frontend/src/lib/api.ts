const BASE = "http://127.0.0.1:8000";

function headers() {
  return {
    "Content-Type": "application/json",
    "X-API-Key": localStorage.getItem("apiKey") || "",
  };
}

export async function createIndicator(ind: { type: string; value: string; tags: string[] }) {
  const res = await fetch(`${BASE}/indicators/`, {
    method: "POST",
    headers: headers(),
    body: JSON.stringify(ind),
  });
  return res.json();
}

export async function getIndicators() {
    const res = await fetch(`${BASE}/feeds?min_score=0`, { headers: headers() });
    if (!res.ok) {
      throw new Error(`API error: ${res.status}`);
    }
    return res.json();
}
  

export async function getPackages() {
  const res = await fetch(`${BASE}/packages`, {
    headers: headers(),
  });
  return res.json();
}

export async function createApiKey(owner: string) {
  const res = await fetch(`${BASE}/apikeys/create?owner=${owner}`, {
    method: "POST",
    headers: headers(),
  });
  return res.json();
}

export async function createAlert(alert: { tag: string; minScore: number; channel: string; target: string }) {
  const res = await fetch(`${BASE}/alerts`, {
    method: "POST",
    headers: headers(),
    body: JSON.stringify(alert),
  });
  return res.json();
}
