# CLAUDE.md

Clube do Robson em Python: painel Streamlit de um clube de Pro Clubs (FIFA 21, PS4, clubId `6703918`), lendo o SQLite `data/raw/clubedorobson.db` (backup de 24/02/2021, mesmos dados da versão Node/Vue com tabelas em inglês). Também tem um scanner da API da EA.

## Rodar
```
pip install -r requirements.txt
streamlit run app.py                                        # painel em http://localhost:8501
python get_team.py --term rage --platform ps5 --delay 0.2   # scanner de clubes na API da EA
```

## Estrutura
- `app.py`: entrada. `st.navigation` (barra no topo) com as páginas Clube (`/clube`, padrão), Jogadores (`/jogadores`) e Partidas (`/partidas`).
- `paginas/`: uma página por arquivo. Detalhes por query param: `jogadores?jogador=<gamertag>` (carta FIFA, atributos, carreira; personagens fictícios incluídos) e `partidas?partida=<matchId>` (placar, estatísticas, escalações).
- `src/data.py`: todo o acesso ao banco. `table(nome)` lê uma tabela inteira com `st.cache_data` e converte colunas numéricas guardadas como texto. Helpers: `club`, `seasonal`, `members` (Players do clube + Robsoners), `matches` (com `season` e `result` 'w'/'d'/'l' do ponto de vista do Robson), `club_match_stats`, `player_match_stats`, `stadium_capacity`.
- `src/ui.py`: o CSS do tema (mesmos tokens e classes da versão Vue: `.card`, `.cdr-grid`, `.big`, `.kv`, `.bar`, `.badge`...), injetado uma vez no `app.py`. Helpers `crest(club_row)`, `photo(gamertag)`, `attr_color`.
- `static/`: servido em `app/static/` (`enableStaticServing` no `.streamlit/config.toml`). `crests/<id>.png` (escudos), `players/<gamertag>.png` (fotos dos Robsoners), `trophies/`. Copiados da versão Vue.
- `.streamlit/config.toml`: tema escuro (fundo `#120c1c`, dourado `#f5c518`).
- `src/scrapper.py`, `src/create_db*.py`, `src/create_mock_db.py`: scripts de coleta e geração do banco (fora do app).
- `get_team.py` (+ `headers.json`, `last_id.txt`, `teams/`): varre IDs na API `proclubs.ea.com` atrás de clubes por nome.
- `_antigo/`: versões aposentadas, só para consulta. `_antigo/v1/` é o app anterior (Clubs.py + pages/ + src/components + src/utils: textos em inglês, gráficos via kaleido, vencedor calculado pelo ID do clube em vez dos gols). `_antigo/main.py` etc. é um esqueleto de navbar que nunca foi terminado.

## Convenções
- UI em português; funções em inglês ou português, snake_case.
- Páginas montam HTML com `st.html` usando as classes de `src/ui.py`; não colocar CSS solto nas páginas.
- Nunca deixar uma expressão solta no nível do script (ex.: `f() if x else g()`): o "magic" do Streamlit imprime o retorno na tela.
- Teste de fumaça: `streamlit.testing.v1.AppTest.from_file("paginas/<pagina>.py")` com `at.query_params[...]`, verificar `at.exception`.

## Referência
`C:\Users\pedro\projects\clube-do-robson`: versão Node/Express + Vue (mesmo visual). Fonte das imagens em `front-end/public/` e do gerador de SQLite `scripts/dump_to_sqlite.py`.

## Backlog
- O `proName` do `El_Wandershow` aqui é "Show"; no banco do Vue é "Sins".
- Guilherme, Keno, Jaramillo e B. Lolo não têm foto nem cadastro em Robsoners.
- Endpoints da EA do `get_team.py` e do `scrapper.py` são de FIFA 21/FC 24; podem ter mudado.
