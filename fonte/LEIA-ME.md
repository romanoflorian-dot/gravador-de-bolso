# Fonte do Gravador de Bolso

Arquivos para refazer o app. O site publicado fica na raiz do repositório (versão Full) e em `lite/` (versão Lite, a usada pelos alunos).

- `gravador-de-bolso.html` — fonte principal (versão Full).
- `make_lite.py` — gera a Lite a partir da Full (troca textos, esconde o tratamento, aplica o visual preto e branco, a orelha, o estúdio em grades). Usa `studio_lite.html`, `lite_extra.css`, `ear.svg`, `ear_notas.svg`.
- `lite_to_repo.py` — embrulha a Lite em `lite/index.html`.
- `build_pwa.py` — gera a versão Full instalável.
- `icons_ear.py` — gera os ícones da orelha da Lite.

## Refazer a Lite

```
cd fonte
cp gravador-de-bolso.html gravador-de-bolso-full.html
python3 make_lite.py
mkdir -p dist && python3 lite_to_repo.py . ..
```

Depois, em `lite/sw.js`, aumentar o número de `CACHE` (ex.: `gravador-de-bolso-lite-v10` → `v11`) para os celulares receberem a versão nova.

Links: https://romanoflorian-dot.github.io/gravador-de-bolso/ (Full) e https://romanoflorian-dot.github.io/gravador-de-bolso/lite/ (Lite).
