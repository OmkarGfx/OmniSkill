const GITHUB_REPO = process.env.GITHUB_REPO || "kilospark/webact";
const CACHE_TTL_MS = 5 * 60 * 1000;

let cached = null;
let cachedAt = 0;

async function fetchLatestVersion() {
  const now = Date.now();
  if (cached && now - cachedAt < CACHE_TTL_MS) return cached;

  const res = await fetch(
    `https://api.github.com/repos/${GITHUB_REPO}/releases/latest`,
    { headers: { Accept: "application/vnd.github+json" } }
  );
  if (!res.ok) throw new Error(`GitHub API ${res.status}`);
  const data = await res.json();
  const version = data.tag_name.replace(/^v/, "");
  cached = { latest: version, download_url: data.html_url };
  cachedAt = now;
  return cached;
}

export default async function handler(req, res) {
  if (req.method !== "GET") return res.status(405).end();
  try {
    const info = await fetchLatestVersion();
    const current = req.query.current || "";
    res.json({
      latest: info.latest,
      current_is_latest: current === info.latest,
      download_url: info.download_url,
    });
  } catch {
    res.status(502).json({ error: "Failed to check version" });
  }
}
