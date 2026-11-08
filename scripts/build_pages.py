"""Monta _site/ para o GitHub Pages: o app roda no navegador com stlite (Streamlit + Pyodide).

- index.html carrega o stlite e monta o app com os arquivos listados em ARQUIVOS
- os arquivos do app e o banco vão junto como estáticos (o stlite baixa cada um)
- static/ é copiado para app/static/, o mesmo caminho que o Streamlit normal serve
- 404.html é uma cópia do index.html, para que /clube, /jogadores etc. abram o app

Uso: python scripts/build_pages.py   (depois: python -m http.server -d _site)
"""
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "_site"
STLITE = "1.12.0"

ARQUIVOS = [
    "app.py",
    *sorted(str(p.relative_to(ROOT)).replace("\\", "/") for p in (ROOT / "paginas").glob("*.py")),
    "src/data.py",
    "src/ui.py",
    "data/raw/clubedorobson.db",
    "static/crests/99150901.png",  # st.logo e page_icon leem do sistema de arquivos
    "static_index.json",  # gerado no build: lista de static/ para o ui.py
]

# Mesmo tema do .streamlit/config.toml (o stlite recebe a config pelo mount)
CONFIG = {
    "theme.base": "dark",
    "theme.primaryColor": "#f5c518",
    "theme.backgroundColor": "#120c1c",
    "theme.secondaryBackgroundColor": "#1c1329",
    "theme.textColor": "#f3eefb",
    "client.toolbarMode": "viewer",
}

INDEX = """<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#120c1c">
  <title>Clube do Robson</title>
  <link rel="icon" href="app/static/crests/99150901.png">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@stlite/browser@__STLITE__/build/stlite.css">
  <style>
    html, body { margin: 0; background: #120c1c; color: #f3eefb; font-family: system-ui, sans-serif; }
    #carregando { position: fixed; inset: 0; display: grid; place-items: center; text-align: center; }
    #carregando img { width: 96px; height: 96px; animation: pulsa 1.6s ease-in-out infinite; }
    #carregando p { color: #a99cc0; margin-top: 12px; }
    @keyframes pulsa { 50% { transform: scale(1.08); opacity: .7; } }
  </style>
</head>
<body>
  <div id="carregando"><div><img src="app/static/crests/99150901.png" alt=""><p>Carregando o Clube do Robson…</p></div></div>
  <div id="root"></div>
  <script type="module">
    import { mount } from "https://cdn.jsdelivr.net/npm/@stlite/browser@__STLITE__/build/stlite.js";
    // Base do site (ex.: /clubedorobson-py/), para baixar os arquivos de qualquer rota
    const base = new URL(document.querySelector('link[rel=icon]').href, location.href).pathname.replace(/app\\/static\\/crests\\/99150901\\.png$/, '');
    const arquivos = __ARQUIVOS__;
    const files = Object.fromEntries(arquivos.map((f) => [f, { url: base + f }]));
    mount({
      requirements: ["pandas"],
      entrypoint: "app.py",
      files,
      streamlitConfig: __CONFIG__,
    }, document.getElementById("root"));
    new MutationObserver((_, obs) => {
      if (document.querySelector('[data-testid="stApp"]')) { document.getElementById('carregando').remove(); obs.disconnect(); }
    }).observe(document.getElementById('root'), { childList: true, subtree: true });
  </script>
</body>
</html>
"""


def main():
    if SITE.exists():
        shutil.rmtree(SITE)
    SITE.mkdir()
    indice = sorted(p.relative_to(ROOT / 'static').as_posix() for p in (ROOT / 'static').rglob('*') if p.is_file())
    (ROOT / 'static_index.json').write_text(json.dumps(indice), encoding='utf-8')
    for f in ARQUIVOS:
        (SITE / f).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / f, SITE / f)
    shutil.copytree(ROOT / "static", SITE / "app" / "static")
    html = (INDEX.replace("__STLITE__", STLITE)
            .replace("__ARQUIVOS__", json.dumps(ARQUIVOS))
            .replace("__CONFIG__", json.dumps(CONFIG)))
    (SITE / "index.html").write_text(html, encoding="utf-8")
    (SITE / "404.html").write_text(html, encoding="utf-8")
    (SITE / ".nojekyll").write_text("")
    total = sum(p.stat().st_size for p in SITE.rglob("*") if p.is_file())
    print(f"{len(ARQUIVOS)} arquivos do app, {total / 1e6:.1f} MB em {SITE}")


if __name__ == "__main__":
    main()
