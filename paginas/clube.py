import streamlit as st

from src import data, ui

c = data.club()
s = data.seasonal()
total = s["totalgames"] or 1
pct = {k: s[k] / total * 100 for k in ("wins", "ties", "losses")}
saldo = s["alltimegoals"] - s["alltimegoalsagainst"]

st.html(f"""
<div class="card hero">
  <img src="{ui.crest(c)}" alt="{c['name']}">
  <div style="flex:1">
    <p class="cdr-title">{c['name']}</p>
    <p class="cdr-sub">🏟️ {c['stadname']} · ⭐ Reputação {s['starlevel']}</p>
    <div class="hero-rec">
      <div><div class="big">{s['totalgames']}</div><div class="lbl">Jogos</div></div>
      <div><div class="big w">{s['wins']}</div><div class="lbl">Vitórias</div></div>
      <div><div class="big d">{s['ties']}</div><div class="lbl">Empates</div></div>
      <div><div class="big l">{s['losses']}</div><div class="lbl">Derrotas</div></div>
    </div>
    <div class="bar">
      <div style="width:{pct['wins']}%;background:var(--win)"></div>
      <div style="width:{pct['ties']}%;background:var(--draw)"></div>
      <div style="width:{pct['losses']}%;background:var(--loss)"></div>
    </div>
    <p class="cdr-sub" style="margin:8px 0 0">Venceu {pct['wins']:.0f}% dos jogos</p>
  </div>
</div>

<div class="cdr-grid g3" style="margin-top:16px">
  <div class="card"><div class="card-h">Ataque e defesa</div>
    <div class="kv"><span>Gols marcados</span><span>{s['alltimegoals']}</span></div>
    <div class="kv"><span>Gols sofridos</span><span>{s['alltimegoalsagainst']}</span></div>
    <div class="kv"><span>Saldo</span><span class="{'w' if saldo >= 0 else 'l'}">{saldo:+d}</span></div>
    <div class="kv"><span>Gols por jogo</span><span>{s['alltimegoals'] / total:.2f}</span></div>
  </div>
  <div class="card"><div class="card-h">Temporadas</div>
    <div class="kv"><span>Disputadas</span><span>{s['seasons']}</span></div>
    <div class="kv"><span>Acessos</span><span class="w">{s['promotions']}</span></div>
    <div class="kv"><span>Rebaixamentos</span><span class="l">{s['relegations']}</span></div>
    <div class="kv"><span>Melhor divisão</span><span>{s['bestdivision']}ª</span></div>
  </div>
  <div class="card"><div class="card-h">Ranking</div>
    <div class="kv"><span>Pontos no ranking</span><span>{s['rankingpoints']}</span></div>
    <div class="kv"><span>Melhor pontuação</span><span>{s['bestpoints']}</span></div>
    <div class="kv"><span>Títulos</span><span class="gold">{s['titleswon']}</span></div>
    <div class="kv"><span>Divisão atual</span><span>{s['currentdivision']}</span></div>
  </div>
</div>
""")

trofeus = [
    ("1ª Divisão", s["leaguewins"], "league_final"),
    ("Divisões 2 e 3", s["divswon2"], "2-3_final"),
    ("Divisões 4 a 7", s["divswon3"], "4-5-6-7_final"),
    ("Divisões 8 a 10", s["divswon4"], "8-9-10_final"),
]
cards = "".join(
    f'<div class="card trophy {"zero" if not n else ""}"><img src="app/static/trophies/{img}.png" alt="{nome}">'
    f'<div class="big">{n}</div><div class="lbl">{nome}</div></div>'
    for nome, n, img in trofeus)
st.html(f'<div class="cdr-section">Sala de troféus <span class="gold">{s["titleswon"]}</span></div>'
        f'<div class="cdr-grid g4">{cards}</div>')

# Forma recente: últimas 10 partidas registradas
ultimas = data.matches().head(10)
clubs = data.clubs()
st.html('<div class="cdr-section">Últimos jogos</div>')
for col, (_, m) in zip(st.columns(5) + st.columns(5), ultimas.iterrows()):
    adv = m["awayClub"] if m["homeClub"] == data.CLUB_ID else m["homeClub"]
    ac = clubs.loc[adv]
    with col:
        ui.link(
            f"ult_{m['matchId']}",
            f'<div class="card" style="text-align:center;padding:12px" title="{ac["name"]}">'
            f'<img src="{ui.crest(ac)}" style="width:48px;height:48px;object-fit:contain">'
            f'<div style="font-family:var(--display);font-weight:800;font-size:1.3rem">{m["homeGoals"]:.0f}–{m["awayGoals"]:.0f}</div>'
            f'<span class="badge {m["result"]}">{ui.RESULT_LABEL[m["result"]]}</span></div>',
            page="paginas/partidas.py", partida=m["matchId"])
