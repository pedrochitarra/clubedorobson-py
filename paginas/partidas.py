import random

import streamlit as st

from src import data, ui

MESES = ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"]


def lista():
    partidas = data.matches()
    clubs = data.clubs()
    st.html('<p class="cdr-title">Partidas</p><p class="cdr-sub">Jogos registrados por temporada</p>')

    temporadas = sorted(partidas["season"].dropna().astype(int).unique(), reverse=True)
    temporada = st.pills("Temporada", temporadas, default=temporadas[0], format_func=lambda t: f"Temporada {t}",
                         label_visibility="collapsed")
    if temporada is None:
        return
    jogos = partidas[partidas["season"] == temporada]

    r = jogos["result"].value_counts()
    st.html(f"""
<div class="cdr-grid g4" style="margin:6px 0 18px">
  <div class="card" style="text-align:center"><div class="big">{len(jogos)}</div><div class="lbl">Jogos</div></div>
  <div class="card" style="text-align:center"><div class="big w">{r.get('w', 0)}</div><div class="lbl">Vitórias</div></div>
  <div class="card" style="text-align:center"><div class="big d">{r.get('d', 0)}</div><div class="lbl">Empates</div></div>
  <div class="card" style="text-align:center"><div class="big l">{r.get('l', 0)}</div><div class="lbl">Derrotas</div></div>
</div>""")

    for _, m in jogos.iterrows():
        h, a = clubs.loc[m["homeClub"]], clubs.loc[m["awayClub"]]
        d = m["date"]
        ui.link(f"par_{m['matchId']}", f"""
<div class="card match {m['result']}">
  <div class="dt">{d.day:02d} {MESES[d.month - 1]}<small>{d:%H:%M}</small></div>
  <div class="team home {'us' if h['clubId'] == data.CLUB_ID else ''}"><span>{h['name']}</span><img src="{ui.crest(h)}"></div>
  <div class="score">{m['homeGoals']:.0f} – {m['awayGoals']:.0f}</div>
  <div class="team {'us' if a['clubId'] == data.CLUB_ID else ''}"><img src="{ui.crest(a)}"><span>{a['name']}</span></div>
  <span class="badge {m['result']}">{ui.RESULT_LABEL[m['result']]}</span>
</div>""", partida=m["matchId"])


def detalhe(match_id: str):
    m = data.match(match_id)
    clubs = data.clubs()
    h, a = clubs.loc[m["homeClub"]], clubs.loc[m["awayClub"]]
    stats = data.club_match_stats(match_id)
    sh, sa = stats.loc[m["homeClub"]], stats.loc[m["awayClub"]]

    # Público simulado: 80–100% da capacidade (a Arena Robson Oliveira usa o Emirates como referência)
    estadio = "Emirates Stadium" if h["stadname"] == "Arena Robson Oliveira" else h["stadname"]
    cap = data.stadium_capacity(estadio)
    publico = f" · 👥 {ui.fmt_int(cap * random.Random(match_id).uniform(.8, 1))}" if cap else ""
    d = m["date"]

    ui.back("Partidas")
    st.html(f"""
<div class="card" style="margin-top:12px;padding:24px;background:radial-gradient(500px 220px at 50% 0%, rgba(167,123,240,.28), transparent 70%), linear-gradient(180deg,var(--surface-2),var(--surface))">
  <div class="meta">📅 {d.day:02d} {MESES[d.month - 1]} {d.year} · 🕐 {d:%H:%M} · 🏟️ {h['stadname']}{publico}</div>
  <div class="board">
    <div><img src="{ui.crest(h)}"><div class="cn {'gold' if h['clubId'] == data.CLUB_ID else ''}">{h['name']}</div><div class="lbl">Casa</div></div>
    <div><div class="goals">{m['homeGoals']:.0f} – {m['awayGoals']:.0f}</div><span class="pill {m['result']}">{ui.RESULT_NAME[m['result']]}</span></div>
    <div><img src="{ui.crest(a)}"><div class="cn {'gold' if a['clubId'] == data.CLUB_ID else ''}">{a['name']}</div><div class="lbl">Fora</div></div>
  </div>
</div>""")

    def prec(s):
        return s["passesmade"] / s["passattempts"] * 100 if s["passattempts"] else 0

    posse_h = sh["passesmade"] / ((sh["passesmade"] + sa["passesmade"]) or 1) * 100
    comparacoes = [
        ("Passes", sh["passesmade"], sa["passesmade"], "{:.0f}"),
        ("Precisão no passe", prec(sh), prec(sa), "{:.1f}%"),
        ("Posse de bola", posse_h, 100 - posse_h, "{:.1f}%"),
        ("Chutes", sh["shots"], sa["shots"], "{:.0f}"),
        ("Divididas", sh["tacklesmade"], sa["tacklesmade"], "{:.0f}"),
    ]
    linhas = []
    for rot, vh, va, fmt in comparacoes:
        tot = (vh + va) or 1
        linhas.append(
            f'<div class="cmp"><div class="vals"><span class="{"gold" if vh > va else ""}">{fmt.format(vh)}</span>'
            f'<span>{rot}</span><span class="{"gold" if va > vh else ""}">{fmt.format(va)}</span></div>'
            f'<div class="bars"><div class="bar home"><div style="width:{vh / tot * 100}%"></div></div>'
            f'<div class="bar away"><div style="width:{va / tot * 100}%"></div></div></div></div>')
    st.html(f'<div class="card" style="margin-top:16px"><div class="card-h">Estatísticas</div>{"".join(linhas)}</div>')

    # Escalações
    jogadores = data.player_match_stats(match_id)
    nomes = data.members().set_index("name")["displayName"]
    st.html('<div class="cdr-section">Escalações</div>')
    for col, clube in zip(st.columns(2), (h, a)):
        with col:
            st.html(f'<div class="card-h" style="text-align:center">{clube["name"]}</div>')
            js = jogadores[jogadores["clubid"] == clube["clubId"]].copy()
            js["Jogador"] = [nomes.get(n, n) for n in js["name"]]
            js["Craque"] = js["mom"].map({1: "⭐"}).fillna("")
            st.dataframe(
                js[["Jogador", "goals", "assists", "shots", "passesmade", "rating", "Craque"]]
                .rename(columns={"goals": "G", "assists": "A", "shots": "Chutes", "passesmade": "Passes", "rating": "Nota"})
                .sort_values("Nota", ascending=False),
                hide_index=True, width="stretch",
                column_config={"Nota": st.column_config.NumberColumn(format="%.1f")})


pid = st.query_params.get("partida")
if pid:
    detalhe(pid)
else:
    lista()
