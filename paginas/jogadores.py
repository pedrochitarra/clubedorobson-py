import pandas as pd
import streamlit as st

from src import data, ui

POSICOES_FAV = {"goalkeeper": "Goleiro", "defender": "Defensor", "midfielder": "Meio-campo", "forward": "Atacante"}
# Índices de proPos usados pela API da EA
POSICOES = ["GOL", "LIB", "ALD", "LD", "ZAD", "ZAG", "ZAE", "LE", "ALE", "VOD", "VOL", "VOE", "MD", "MCD", "MC",
            "MCE", "ME", "MAD", "MEI", "MAE", "SAD", "SA", "SAE", "PD", "ATD", "ATA", "ATE", "PE"]
# Ordem dos atributos em vproattr ("088|089|...")
ATRIBUTOS = ["aceleracao", "pique", "agilidade", "equilibrio", "impulsao", "folego", "forca", "reacao",
             "combatividade", "frieza", "interceptacao", "posAtaque", "visao", "chuteslonge", "forcachute",
             "conducao", "finalizacao", "cobrancafalta", "cabeceio", "lancamento", "passecurto", "nocaodefensiva",
             "cruzamento", "controlebola", "divididaempe", "carrinho", "voleio", "curva", "penaltis"]


def lista():
    membros = data.members()
    rob = data.robsoners()
    st.html('<p class="cdr-title">Elenco</p><p class="cdr-sub">Quem vestiu a camisa do Robson, por número de jogos</p>')

    for col, (_, m) in zip(st.columns(2) * len(membros), membros.iterrows()):
        foto = ui.photo(m["name"])
        img = f'<img src="{foto}">' if foto else f'<img class="ph-empty" src="{ui.DEFAULT_PHOTO}">'
        num = f'<span class="num">{int(m["number"])}</span>' if pd.notna(m["number"]) else ""
        html = f"""
<div class="card player">
  <div class="ph">{img}{num}</div>
  <div style="flex:1;min-width:0">
    <div style="display:flex;justify-content:space-between;gap:8px">
      <div><div class="nm">{m['displayName']}</div><div class="tag">{m['name']} · {POSICOES_FAV.get(m['favoritePosition'], '')}</div></div>
      <div class="ovr">{m['proOverall']:.0f}</div>
    </div>
    <div class="pstats">
      <div><b>{m['gamesPlayed']:.0f}</b><span>Jogos</span></div><div><b>{m['goals']:.0f}</b><span>Gols</span></div>
      <div><b>{m['assists']:.0f}</b><span>Assist.</span></div><div><b>{m['manOfTheMatch']:.0f}</b><span>Craque</span></div>
    </div>
    <div class="bar" style="height:6px"><div style="width:{m['winRate']}%;background:var(--win)"></div></div>
    <div class="tag" style="margin-top:4px">{m['winRate']:.0f}% de vitórias</div>
  </div>
</div>"""
        with col:
            ui.link(f"jog_{m['name']}", html, jogador=m["name"])

    fakes = rob[rob["isfake"] == 1].sort_values("number")
    st.html('<div class="cdr-section">Personagens do clube</div>'
            '<p class="cdr-sub">Os craques fictícios que completavam o time</p>')
    for col, (_, r) in zip(st.columns(4) * len(fakes), fakes.iterrows()):
        with col:
            ui.link(
                f"leg_{r['name']}",
                f'<div class="card legend"><img src="{ui.photo(r["name"]) or ui.DEFAULT_PHOTO}">'
                f'<div class="big gold" style="font-size:1.4rem;margin-top:6px">{r["number"]}</div>'
                f'<div style="font-weight:600">{r["proName"]}</div></div>',
                jogador=r["name"])


def detalhe(tag: str):
    membros = data.members().set_index("name", drop=False)
    rob = data.robsoners()
    m = membros.loc[tag] if tag in membros.index else None
    r = rob.loc[tag] if tag in rob.index else None
    if m is None and r is None:
        st.error("Jogador não encontrado.")
        return

    # Atributos: última partida registrada do jogador, ou o cadastro do personagem
    pm = data.table("PlayersMatches")
    pm = pm[pm["name"] == tag]
    vpro = pm["vproattr"].iloc[0] if len(pm) else (r["vproattr"] if r is not None else None)
    s = dict(zip(ATRIBUTOS, map(int, vpro.split("|")))) if vpro else None

    nome = r["proName"] if r is not None else m["proName"]
    pos_idx = m["proPos"] if m is not None else r["proPos"]
    posicao = POSICOES[int(float(pos_idx))] if pd.notna(pos_idx) and str(pos_idx).strip() not in ("", "None") else ""
    foto = ui.photo(tag)

    g = None
    if s:
        g = {
            "RIT": round(s["pique"] * .55 + s["aceleracao"] * .45),
            "FIN": round(s["finalizacao"] * .45 + s["chuteslonge"] * .2 + s["forcachute"] * .2 + s["posAtaque"] * .05 + s["penaltis"] * .05 + s["voleio"] * .05),
            "PAS": round(s["passecurto"] * .35 + s["visao"] * .2 + s["cruzamento"] * .2 + s["lancamento"] * .15 + s["curva"] * .05 + s["cobrancafalta"] * .05),
            "CON": round(s["conducao"] * .5 + s["controlebola"] * .35 + s["agilidade"] * .1 + s["equilibrio"] * .05),
            "DEF": round(s["nocaodefensiva"] * .3 + s["divididaempe"] * .3 + s["interceptacao"] * .2 + s["cabeceio"] * .1 + s["carrinho"] * .1),
            "FIS": round(s["forca"] * .5 + s["folego"] * .25 + s["combatividade"] * .2 + s["impulsao"] * .05),
        }
    overall = int(m["proOverall"]) if m is not None else (round(sum(g.values()) / 6) if g else "—")

    ui.back("Elenco")

    attrs = "".join(f"<div><b>{v}</b><span>{k}</span></div>" for k, v in (g or {}).items())
    img = f'<img class="photo" src="{foto}">' if foto else f'<img class="photo ph-empty" src="{ui.DEFAULT_PHOTO}">'
    fatos = [(int(m["proHeight"] if m is not None else r["proHeight"]), "Altura (cm)")]
    if r is not None and r["weight"]:
        fatos.append((r["weight"], "Peso (kg)"))
    if r is not None and r["birthdate"]:
        fatos.append((r["birthdate"], "Nascimento"))
    fatos_html = "".join(f'<div class="card"><div class="big" style="font-size:1.9rem">{v}</div><div class="lbl">{l}</div></div>'
                         for v, l in fatos)

    if m is not None:
        carreira = [("Jogos", m["gamesPlayed"]), ("Gols", m["goals"]), ("Assistências", m["assists"]),
                    ("Craque do jogo", m["manOfTheMatch"]), ("Vitórias", f"{m['winRate']:.0f}%"),
                    ("Precisão de passe", f"{m['passSuccessRate']:.0f}%"), ("Precisão de chute", f"{m['shotSuccessRate']:.0f}%"),
                    ("Cartões vermelhos", m["redCards"])]
        extra = '<div class="cdr-grid carreira" style="margin-top:14px">' + "".join(
            f'<div class="card"><div class="big" style="font-size:1.9rem">{v if isinstance(v, str) else int(v)}</div><div class="lbl">{l}</div></div>'
            for l, v in carreira) + "</div>"
    else:
        extra = '<p class="note" style="margin-top:14px">🤖 Personagem fictício do clube: tem atributos, mas não entra nas estatísticas da EA.</p>'

    camisa = f'<span class="shirt" title="Camisa">{r["number"]}</span>' if r is not None and r["number"] else ""
    selos = (f'<div class="tags">{camisa}<span class="tagchip">🎮 {tag}</span>'
             + (f'<span class="tagchip">{posicao}</span>' if posicao else "")
             + ('<span class="tagchip fake">Personagem</span>' if m is None else "") + "</div>")
    st.html(f"""
<div class="profile" style="margin-top:14px">
  <div class="fut">
    <div class="top"><div class="ov">{overall}</div><div class="ps">{posicao}</div><img src="app/static/crests/99150901.png"></div>
    {img}
    <div class="fn">{nome}</div>
    <div class="at">{attrs}</div>
  </div>
  <div style="flex:1;min-width:0;width:100%">
    <p class="cdr-title">{nome}</p>{selos}
    <div class="cdr-grid fatos" style="--n:{len(fatos)}">{fatos_html}</div>
    {extra}
  </div>
</div>""")

    if s:
        grupos = [
            ("Ritmo", "RIT", [("Aceleração", "aceleracao"), ("Pique", "pique")]),
            ("Finalização", "FIN", [("Finalização", "finalizacao"), ("Força do chute", "forcachute"), ("Chute de longe", "chuteslonge"),
                                    ("Posicionamento", "posAtaque"), ("Voleio", "voleio"), ("Pênaltis", "penaltis")]),
            ("Passe", "PAS", [("Passe curto", "passecurto"), ("Visão", "visao"), ("Cruzamento", "cruzamento"),
                              ("Lançamento", "lancamento"), ("Curva", "curva"), ("Cobrança de falta", "cobrancafalta")]),
            ("Condução", "CON", [("Condução", "conducao"), ("Controle de bola", "controlebola"), ("Agilidade", "agilidade"),
                                 ("Equilíbrio", "equilibrio"), ("Reação", "reacao"), ("Frieza", "frieza")]),
            ("Defesa", "DEF", [("Noção defensiva", "nocaodefensiva"), ("Dividida em pé", "divididaempe"),
                               ("Interceptação", "interceptacao"), ("Cabeceio", "cabeceio"), ("Carrinho", "carrinho")]),
            ("Físico", "FIS", [("Força", "forca"), ("Fôlego", "folego"), ("Combatividade", "combatividade"), ("Impulsão", "impulsao")]),
        ]
        blocos = []
        for titulo, sigla, itens in grupos:
            linhas = "".join(
                f'<div class="attr"><span>{rot}</span><div class="bar"><div style="width:{s[k]}%;background:{ui.attr_color(s[k])}"></div></div>'
                f'<b style="color:{ui.attr_color(s[k])}">{s[k]}</b></div>' for rot, k in itens)
            blocos.append(f'<div class="card"><div class="card-h">{titulo} <span style="float:right;color:{ui.attr_color(g[sigla])}">{g[sigla]}</span></div>{linhas}</div>')
        st.html(f'<div class="cdr-grid g3" style="margin-top:20px">{"".join(blocos)}</div>')


tag = st.query_params.get("jogador")
if tag:
    detalhe(tag)
else:
    lista()
