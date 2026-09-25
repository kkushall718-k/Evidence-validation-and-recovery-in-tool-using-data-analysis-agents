"""Self-contained read-only notebook preview from saved outputs, no execution."""

from pathlib import Path
import html, json, re

ROOT = Path(__file__).resolve().parents[1]
p = ROOT / "notebooks/Thesis_Experiment_Reproduction.ipynb"
nb = json.loads(p.read_text())
parts = [
    '<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Thesis experiment reproduction</title><style>body{max-width:1060px;margin:45px auto;padding:0 24px;color:#182933;font:17px/1.6 system-ui}h1{line-height:1.2}h2{margin-top:42px}pre{white-space:pre-wrap;background:#f3f5f7;padding:16px;font:13px/1.5 monospace;overflow-wrap:anywhere}img{max-width:100%;height:auto}table{border-collapse:collapse;font-size:13px;display:block;overflow:auto}td,th{border:1px solid #ccd5dc;padding:7px;text-align:left}summary{cursor:pointer;color:#17638a;margin:14px 0}.output{overflow:auto}code{background:#f3f5f7}a{color:#17638a}</style><body>'
]


def md(src):
    out = []
    for block in src.split("\n\n"):
        level = len(block) - len(block.lstrip("#"))
        s = html.escape(block[level:].strip() if level else block)
        s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
        s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
        out.append(
            f"<h{min(level,6)}>{s}</h{min(level,6)}>" if level else f"<p>{s}</p>"
        )
    return "\n".join(out)


for c in nb["cells"]:
    src = "".join(c["source"])
    if c["cell_type"] == "markdown":
        parts.append(md(src))
        continue
    parts.append(
        "<details><summary>Python cell "
        + str(c.get("execution_count", ""))
        + "</summary><pre>"
        + html.escape(src)
        + "</pre></details>"
    )
    for o in c.get("outputs", []):
        data = o.get("data", {})
        if "image/png" in data:
            parts.append(
                '<img alt="Saved experimental result figure" src="data:image/png;base64,'
                + "".join(data["image/png"]).replace("\n", "")
                + '">'
            )
        elif "text/html" in data:
            parts.append('<div class="output">' + "".join(data["text/html"]) + "</div>")
        elif "text/plain" in data:
            parts.append("<pre>" + html.escape("".join(data["text/plain"])) + "</pre>")
        elif "text" in o:
            parts.append("<pre>" + html.escape("".join(o["text"])) + "</pre>")
parts.append("</body></html>")
p.with_suffix(".html").write_text("\n".join(parts))
print("Saved self-contained HTML preview without executing any code.")
