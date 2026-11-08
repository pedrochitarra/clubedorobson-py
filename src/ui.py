"""Visual compartilhado: CSS (mesmo tema da versão Vue) e helpers de HTML/imagens."""
import base64
import json
import math
from pathlib import Path

import streamlit as st

STATIC = Path(__file__).resolve().parent.parent / "static"
RESULT_LABEL = {"w": "V", "d": "E", "l": "D"}
RESULT_NAME = {"w": "Vitória", "d": "Empate", "l": "Derrota"}

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600;700;800&family=Inter:wght@400;500;600;700&display=swap');
:root {
  --bg: #120c1c; --surface: #1c1329; --surface-2: #261a37; --surface-3: #312246;
  --border: rgba(255,255,255,.08); --text: #f3eefb; --muted: #a99cc0;
  --brand: #a77bf0; --gold: #f5c518; --win: #3ecf8e; --draw: #9aa0b4; --loss: #ef5d6b;
  --display: 'Barlow Condensed', 'Inter', sans-serif;
}
/* Só no texto: aplicar em [class*="st-"] troca também a fonte dos ícones Material e eles viram texto */
body, .stApp, .stMarkdown, .stHtml, button p { font-family: 'Inter', system-ui, sans-serif; }
.stApp { background: radial-gradient(1200px 500px at 50% -200px, rgba(124,77,206,.35), transparent 70%), var(--bg); }
.block-container { max-width: 1120px; padding-top: 2.5rem; }
h1, h2, h3 { font-family: var(--display) !important; text-transform: uppercase; letter-spacing: .03em; }
a, a:visited { color: inherit; text-decoration: none; }

.cdr-title { font-family: var(--display) !important; font-weight: 700; font-size: 2.2rem !important; text-transform: uppercase; margin: 0; line-height: 1.1; }
.cdr-sub { color: var(--muted); margin: 2px 0 18px; }
.cdr-section { font-family: var(--display); font-weight: 700; font-size: 1.5rem; text-transform: uppercase; margin: 28px 0 12px; }
.cdr-grid { display: grid; gap: 14px; }
.g2 { grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); }
.g3 { grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); }
.g4 { grid-template-columns: repeat(auto-fit, minmax(170px, 1fr)); }
.card { background: linear-gradient(180deg, var(--surface-2), var(--surface)); border: 1px solid var(--border);
        border-radius: 16px; padding: 18px; color: var(--text); }
a.card { display: block; transition: transform .15s, border-color .15s; }
a.card.match { display: grid; } a.card.player { display: flex; }
a.card:hover { transform: translateY(-2px); border-color: rgba(167,123,240,.5); }
.card-h { font-family: var(--display); font-weight: 700; letter-spacing: .08em; text-transform: uppercase; color: var(--muted); margin-bottom: 10px; }
.big { font-family: var(--display); font-weight: 800; font-size: 2.6rem; line-height: 1; }
.lbl { color: var(--muted); font-size: .78rem; text-transform: uppercase; letter-spacing: .06em; margin-top: 4px; }
.kv { display: flex; justify-content: space-between; padding: 7px 0; border-bottom: 1px solid var(--border); }
.kv:last-child { border-bottom: 0; }
.kv span:first-child { color: var(--muted); }
.kv span:last-child { font-family: var(--display); font-weight: 700; font-size: 1.15rem; }
.w { color: var(--win); } .d { color: var(--draw); } .l { color: var(--loss); } .gold { color: var(--gold); }
.bar { display: flex; height: 10px; border-radius: 99px; overflow: hidden; background: var(--surface-3); }
.bar > div { height: 100%; }
.badge { display: inline-flex; align-items: center; justify-content: center; width: 26px; height: 26px; border-radius: 8px;
         font-family: var(--display); font-weight: 800; color: #120c1c; }
.badge.w { background: var(--win); } .badge.d { background: var(--draw); } .badge.l { background: var(--loss); }

/* Clube */
.hero { display: flex; gap: 32px; align-items: center; padding: 30px;
        background: radial-gradient(600px 300px at 0% 0%, rgba(167,123,240,.25), transparent 70%), linear-gradient(180deg, var(--surface-2), var(--surface)); }
.hero img { width: 160px; height: 160px; object-fit: contain; filter: drop-shadow(0 12px 30px rgba(124,77,206,.5)); }
.hero-rec { display: flex; gap: 32px; margin: 16px 0; }
.trophy { text-align: center; } .trophy img { height: 140px; object-fit: contain; }
.trophy .big { color: var(--gold); font-size: 2.2rem; } .trophy.zero img { filter: grayscale(1) opacity(.35); } .trophy.zero .big { color: var(--muted); }

/* Jogadores */
.player { display: flex; gap: 16px; align-items: center; }
.player .ph { position: relative; width: 104px; height: 104px; flex-shrink: 0; border-radius: 14px; overflow: hidden;
              background: radial-gradient(circle at 50% 30%, var(--surface-3), var(--surface)); }
.player .ph img { width: 100%; height: 100%; object-fit: cover; object-position: top; }
.player .ph img.ph-empty { object-fit: contain; padding: 24px; opacity: .25; }
.player .num { position: absolute; left: 6px; bottom: 2px; font-family: var(--display); font-weight: 800; font-size: 1.5rem; color: var(--gold); text-shadow: 0 2px 6px #000a; }
.player .nm { font-family: var(--display); font-weight: 700; font-size: 1.45rem; line-height: 1.1; }
.player .tag { color: var(--muted); font-size: .8rem; }
.ovr { font-family: var(--display); font-weight: 800; font-size: 1.3rem; color: #120c1c; background: var(--gold); border-radius: 10px; padding: 1px 10px; height: fit-content; }
.pstats { display: grid; grid-template-columns: repeat(4, 1fr); gap: 6px; margin: 8px 0; }
.pstats b { display: block; font-family: var(--display); font-size: 1.25rem; line-height: 1; }
.pstats span { color: var(--muted); font-size: .7rem; text-transform: uppercase; }
.legend { text-align: center; } .legend img { width: 100%; height: 140px; object-fit: cover; object-position: top; border-radius: 12px; }

/* Partidas */
.match { display: grid; grid-template-columns: 64px 1fr auto 1fr 32px; align-items: center; gap: 14px; padding: 12px 16px;
         border-left: 4px solid transparent; margin-bottom: 10px; }
.match.w { border-left-color: var(--win); } .match.d { border-left-color: var(--draw); } .match.l { border-left-color: var(--loss); }
.match .dt { font-family: var(--display); font-weight: 700; text-transform: uppercase; line-height: 1.1; color: var(--text); }
.match .dt small { display: block; color: var(--muted); font-weight: 500; }
.team { display: flex; align-items: center; gap: 10px; min-width: 0; color: var(--text); font-weight: 600; }
.team img { width: 40px; height: 40px; object-fit: contain; }
.team.home { justify-content: flex-end; text-align: right; }
.team.us { color: var(--gold); }
.score { font-family: var(--display); font-weight: 800; font-size: 1.8rem; background: var(--bg); border-radius: 10px; padding: 2px 14px; color: var(--text); }

.board { display: grid; grid-template-columns: 1fr auto 1fr; align-items: center; text-align: center; gap: 16px; }
.board img { width: 110px; height: 110px; object-fit: contain; }
.board .cn { font-family: var(--display); font-weight: 700; font-size: 1.4rem; }
.board .goals { font-family: var(--display); font-weight: 800; font-size: 4.2rem; line-height: 1; }
.pill { display: inline-block; margin-top: 8px; padding: 2px 14px; border-radius: 99px; font-family: var(--display); font-weight: 700; text-transform: uppercase; color: #120c1c; }
.pill.w { background: var(--win); } .pill.d { background: var(--draw); } .pill.l { background: var(--loss); }
.meta { color: var(--muted); font-size: .85rem; text-align: center; margin-bottom: 14px; }
.cmp { padding: 8px 0; border-bottom: 1px solid var(--border); }
.cmp:last-child { border-bottom: 0; }
.cmp .vals { display: flex; justify-content: space-between; font-family: var(--display); font-weight: 700; font-size: 1.15rem; }
.cmp .vals span:nth-child(2) { font-family: 'Inter'; font-weight: 500; font-size: .78rem; color: var(--muted); text-transform: uppercase; }
.cmp .bars { display: flex; gap: 6px; margin-top: 4px; }
.cmp .bars .bar { flex: 1; height: 8px; }
.cmp .home { justify-content: flex-end; } .cmp .home > div { background: var(--brand); } .cmp .away > div { background: var(--gold); }

/* Jogador */
.fut { width: 250px; padding: 18px; border-radius: 22px; position: relative; text-align: center; flex-shrink: 0;
       background: radial-gradient(260px 200px at 50% 20%, rgba(245,197,24,.35), transparent 70%), linear-gradient(160deg, #3a2758, #1c1329 70%);
       border: 1px solid rgba(245,197,24,.4); box-shadow: 0 20px 50px #0007; }
.fut .top { position: absolute; top: 18px; left: 20px; font-family: var(--display); line-height: 1; text-align: center; }
.fut .ov { font-weight: 800; font-size: 3rem; color: var(--gold); } .fut .ps { font-weight: 700; font-size: 1.2rem; }
.fut .top img { width: 30px; margin-top: 6px; }
.fut .photo { width: 180px; height: 180px; object-fit: cover; object-position: top; margin-left: 30px; }
.fut .photo.ph-empty { object-fit: contain; padding: 30px; opacity: .3; }
.fut .fn { font-family: var(--display); font-weight: 800; font-size: 1.6rem; text-transform: uppercase; border-top: 1px solid #f5c51866; border-bottom: 1px solid #f5c51866; margin: 4px 0 10px; }
.fut .at { display: grid; grid-template-columns: repeat(3, 1fr); gap: 4px 8px; font-family: var(--display); }
.fut .at b { font-size: 1.3rem; } .fut .at span { color: var(--muted); font-weight: 600; margin-left: 4px; }
.profile { display: flex; gap: 26px; align-items: flex-start; }
.attr { display: grid; grid-template-columns: minmax(0,1fr) 64px 26px; gap: 10px; align-items: center; padding: 4px 0; font-size: .86rem; }
.attr span { color: var(--muted); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.attr b { font-family: var(--display); font-size: 1.05rem; text-align: right; }
.attr .bar { height: 6px; }
.cdr-grid.fatos { grid-template-columns: repeat(var(--n), minmax(0, 1fr)); }
.cdr-grid.carreira { grid-template-columns: repeat(4, minmax(0, 1fr)); }
.cdr-grid.fatos .card, .cdr-grid.carreira .card { padding: 14px 16px; min-width: 0; }
@media (max-width: 700px) { .cdr-grid.carreira { grid-template-columns: repeat(2, minmax(0, 1fr)); } }
.habilidades { display: grid; grid-template-columns: minmax(260px, 340px) minmax(0, 1fr); gap: 14px; margin-top: 20px; align-items: start; }
.habilidades .grupos { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 14px; }
.radar-card { position: sticky; top: 70px; text-align: center; }
@media (max-width: 860px) { .habilidades { grid-template-columns: 1fr; } .radar-card { position: static; } }
@media (max-width: 560px) { .habilidades .grupos { grid-template-columns: 1fr; } }
.tags { display: flex; align-items: center; flex-wrap: wrap; gap: 8px; margin: 8px 0 18px; }
.shirt { display: inline-grid; place-items: center; min-width: 52px; height: 52px; padding: 0 8px; border-radius: 12px 12px 18px 18px;
         background: linear-gradient(180deg, #ff4fa0, #d81b72); color: #fff; font-family: var(--display); font-weight: 800; font-size: 1.7rem;
         box-shadow: inset 0 -4px 0 rgba(0,0,0,.18); }
.tagchip { display: inline-flex; align-items: center; gap: 6px; padding: 5px 12px; border-radius: 99px; background: var(--surface-3);
           border: 1px solid var(--border); color: var(--text); font-weight: 600; font-size: .85rem; }
.tagchip.fake { color: var(--gold); border-color: rgba(245,197,24,.35); }
.note { color: var(--muted); border: 1px dashed var(--border); border-radius: 12px; padding: 12px 14px; }
@media (max-width: 700px) {
  .hero, .profile { flex-direction: column; text-align: center; }
  .match { grid-template-columns: 1fr auto 1fr; } .match .dt, .match .badge { display: none; }
  .team, .team.home { flex-direction: column; justify-content: center; text-align: center; font-size: .8rem; }
}
</style>
"""


def inject_css() -> None:
    st.html(CSS + LINK_CSS)


# Cards clicáveis sem <a href>: no stlite (Python no navegador) recarregar a página
# reinicia o Python inteiro. Um botão transparente por cima do card só reexecuta o script.
LINK_CSS = """
<style>
div[class*="st-key-lnk_"] { position: relative; gap: 0 !important; }
div[class*="st-key-lnk_"] div[data-testid="stElementContainer"]:has(.stButton) {
  position: absolute !important; inset: 0; z-index: 3; margin: 0 !important; width: 100% !important; }
div[class*="st-key-lnk_"] .stButton, div[class*="st-key-lnk_"] .stButton button { width: 100%; height: 100%; }
div[class*="st-key-lnk_"] .stButton button { opacity: 0; cursor: pointer; }
div[class*="st-key-lnk_"]:hover .card { transform: translateY(-2px); border-color: rgba(167,123,240,.5); }
div[class*="st-key-lnk_"]:hover .match { transform: translateX(3px); }
div[class*="st-key-lnk_"] .card { transition: transform .15s, border-color .15s; }
div.st-key-voltar button { background: none !important; border: 0 !important; color: var(--muted) !important;
  padding: 0 !important; min-height: 0 !important; font-weight: 600; }
div.st-key-voltar button:hover { color: var(--text) !important; }
</style>
"""


def link(key: str, html: str, page: str | None = None, **params) -> None:
    """Desenha `html` e torna o bloco inteiro clicável: abre `page` (ou a página atual) com `params` na URL."""
    with st.container(key=f"lnk_{key}"):
        st.html(html)
        if st.button("Abrir", key=f"btn_{key}"):
            if page:
                st.switch_page(page, query_params=params)
            st.query_params.from_dict(params)
            st.rerun()


def back(label: str) -> None:
    """Botão "voltar" com cara de link: limpa os parâmetros da URL e volta para a lista."""
    if st.button(f"← {label}", key="voltar"):
        st.query_params.clear()
        st.rerun()


@st.cache_data
def _static_files() -> frozenset:
    """Arquivos em static/ ("crests/123.png"...). No stlite a pasta não está no sistema de
    arquivos do Python (o GitHub Pages serve as imagens), então vale o índice gerado no build."""
    indice = STATIC.parent / "static_index.json"
    if indice.exists():
        return frozenset(json.loads(indice.read_text(encoding="utf-8")))
    return frozenset(p.relative_to(STATIC).as_posix() for p in STATIC.rglob("*") if p.is_file())


def crest(club_row) -> str:
    """URL do escudo local. Clube customizado usa customcrestid; licenciado usa teamId."""
    cid = club_row["customcrestid"] if club_row["iscustomteam"] == 1 else club_row["teamId"]
    return f"app/static/crests/{cid}.png" if f"crests/{cid}.png" in _static_files() else "app/static/crests/99150901.png"


def photo(gamertag: str):
    """URL da foto local do jogador, ou None quando não existe."""
    return f"app/static/players/{gamertag}.png" if f"players/{gamertag}.png" in _static_files() else None


DEFAULT_PHOTO = "app/static/players/_default.png"


def attr_color(v: float) -> str:
    return "var(--win)" if v >= 85 else "var(--gold)" if v >= 70 else "#f59f4a" if v >= 50 else "var(--loss)"


def _cor_literal(v: float) -> str:
    return "#3ecf8e" if v >= 85 else "#f5c518" if v >= 70 else "#f59f4a" if v >= 50 else "#ef5d6b"


def radar(valores: dict, tamanho: int = 300) -> str:
    """Hexágono de habilidades: um eixo por atributo (0–99), grade em 25/50/75/99.
    Vai como <img> com SVG em base64, porque o st.html remove <svg> embutido; por isso as cores são literais."""
    nomes = list(valores)
    c, r = tamanho / 2, tamanho / 2 - 46
    ang = [-math.pi / 2 + i * 2 * math.pi / len(nomes) for i in range(len(nomes))]

    def ponto(a, f):
        return c + r * f * math.cos(a), c + r * f * math.sin(a)

    def poly(fs):
        return " ".join(f"{x:.1f},{y:.1f}" for x, y in (ponto(a, f) for a, f in zip(ang, fs)))

    grade = "".join(f'<polygon points="{poly([f] * len(nomes))}" fill="none" stroke="rgba(255,255,255,{.06 + .04 * i:.2f})"/>'
                    for i, f in enumerate((.25, .5, .75, 1)))
    eixos = "".join(f'<line x1="{c}" y1="{c}" x2="{ponto(a, 1)[0]:.1f}" y2="{ponto(a, 1)[1]:.1f}" stroke="rgba(255,255,255,.08)"/>' for a in ang)
    fs = [valores[n] / 99 for n in nomes]
    pontos = "".join(f'<circle cx="{ponto(a, f)[0]:.1f}" cy="{ponto(a, f)[1]:.1f}" r="3.5" fill="#f5c518"/>' for a, f in zip(ang, fs))
    rotulos = ""
    for a, n in zip(ang, nomes):
        x, y = ponto(a, 1.25)
        rotulos += (f'<text x="{x:.1f}" y="{y - 5:.1f}" text-anchor="middle" fill="#a99cc0" '
                    f'font-family="Barlow Condensed, sans-serif" font-weight="700" font-size="13">{n}</text>'
                    f'<text x="{x:.1f}" y="{y + 13:.1f}" text-anchor="middle" fill="{_cor_literal(valores[n])}" '
                    f'font-family="Barlow Condensed, sans-serif" font-weight="800" font-size="19">{valores[n]}</text>')
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {tamanho} {tamanho}">{grade}{eixos}'
           f'<polygon points="{poly(fs)}" fill="rgba(245,197,24,.22)" stroke="#f5c518" stroke-width="2" stroke-linejoin="round"/>'
           f'{pontos}{rotulos}</svg>')
    src = "data:image/svg+xml;base64," + base64.b64encode(svg.encode("utf-8")).decode()
    return f'<img src="{src}" alt="Hexágono de habilidades" style="width:100%;max-width:{tamanho}px;display:block;margin:auto">'


def fmt_int(v) -> str:
    return f"{int(v):,}".replace(",", ".")
