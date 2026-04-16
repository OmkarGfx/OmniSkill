const SCRIPT_BASE = "https://raw.githubusercontent.com/kilospark/webact/main";

export default async function handler(req, res) {
  if (req.method !== "GET") return res.status(405).end();

  const name = req.query.name;
  if (name !== "install" && name !== "uninstall") {
    return res.status(404).json({ error: "Not found" });
  }

  try {
    const resp = await fetch(`${SCRIPT_BASE}/${name}.sh`);
    if (!resp.ok) return res.status(502).send(`Failed to fetch ${name}.sh`);
    res.setHeader("Content-Type", "text/plain; charset=utf-8");
    res.setHeader("Cache-Control", "public, max-age=300");
    res.send(await resp.text());
  } catch (e) {
    res.status(502).send(`Failed to fetch ${name}.sh: ${e.message}`);
  }
}
