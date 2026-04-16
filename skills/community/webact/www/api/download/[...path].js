const GITHUB_REPO = process.env.GITHUB_REPO || "kilospark/webact";
const VALID_ASSETS = [
  "webact-darwin-arm64",
  "webact-darwin-x64",
  "webact-linux-x64",
  "webact-linux-arm64",
];

export default async function handler(req, res) {
  if (req.method !== "GET") return res.status(405).end();

  const parts = req.query.path || [];
  let version, assetRaw;

  if (parts.length === 2) {
    version = parts[0];
    assetRaw = parts[1];
  } else if (parts.length === 1) {
    assetRaw = parts[0];
    version = req.query.v;
  } else {
    return res.status(404).json({ error: "Not found" });
  }

  const asset = assetRaw.replace(/\.tar\.gz$/, "");
  if (!VALID_ASSETS.includes(asset)) {
    return res.status(404).json({ error: "Unknown asset" });
  }

  try {
    let tag;
    if (version) {
      tag = version.startsWith("v") ? version : `v${version}`;
    } else {
      const apiRes = await fetch(
        `https://api.github.com/repos/${GITHUB_REPO}/releases/latest`,
        { headers: { Accept: "application/vnd.github+json" } }
      );
      if (!apiRes.ok) throw new Error(`GitHub API ${apiRes.status}`);
      const data = await apiRes.json();
      tag = data.tag_name;
    }

    const url = `https://github.com/${GITHUB_REPO}/releases/download/${tag}/${asset}.tar.gz`;
    const upstream = await fetch(url, { redirect: "follow" });
    if (!upstream.ok) {
      return res.status(upstream.status).json({ error: `Upstream ${upstream.status}` });
    }

    res.setHeader("Content-Type", "application/gzip");
    res.setHeader("Content-Disposition", `attachment; filename="${asset}.tar.gz"`);
    const cl = upstream.headers.get("content-length");
    if (cl) res.setHeader("Content-Length", cl);

    const reader = upstream.body.getReader();
    while (true) {
      const { done, value } = await reader.read();
      if (done) { res.end(); return; }
      if (!res.write(value)) {
        await new Promise((resolve) => res.once("drain", resolve));
      }
    }
  } catch {
    if (!res.headersSent) {
      res.status(502).json({ error: "Failed to fetch binary" });
    }
  }
}
