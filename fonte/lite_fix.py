"""Ajustes de abertura da Lite: fundo branco desde o primeiro quadro, fontes sem bloquear
a pintura da página e entrada da orelha em dissolvência (sem salto depois da tela do sistema).
Pode ser aplicado mais de uma vez sem duplicar nada."""
import re, sys

MARK = '/* abertura-suave */'

def fix(html):
    if MARK in html:
        return html
    # 1) fontes do Google sem bloquear a primeira pintura
    m = re.search(r'<link href="(https://fonts\.googleapis\.com/css2\?[^"]+)" rel="stylesheet">', html)
    assert m, 'link das fontes não encontrado'
    url = m.group(1)
    html = html.replace(m.group(0),
        '<style>html,body{background:#fff}</style>\n'
        f'<link rel="preload" as="style" href="{url}" onload="this.onload=null;this.rel=\'stylesheet\'">\n'
        f'<noscript><link rel="stylesheet" href="{url}"></noscript>', 1)
    # 2) orelha entra por dissolvência; as notas começam depois
    css = (MARK + '\n#abertura svg{animation:abIn .4s ease-out both;will-change:opacity}\n'
           '#abertura .nota{animation-delay:.45s}\n#abertura .n2{animation-delay:1.25s}\n'
           '@keyframes abIn{from{opacity:0}to{opacity:1}}\n'
           '@media (prefers-reduced-motion:reduce){#abertura svg{animation:none}}\n')
    i = html.index('#abertura.sai{opacity:0;pointer-events:none}')
    j = html.index('</style>', i)
    html = html[:j] + css + html[j:]
    # 3) abertura dura um pouco mais, para caber a dissolvência
    a = "setTimeout(() => a.classList.add('sai'), 1700); setTimeout(() => a.remove(), 2200);"
    assert a in html, 'tempo da abertura não encontrado'
    html = html.replace(a, "setTimeout(() => a.classList.add('sai'), 2000); setTimeout(() => a.remove(), 2500);")
    return html

if __name__ == '__main__':
    p = sys.argv[1]
    s = open(p, encoding='utf-8').read()
    open(p, 'w', encoding='utf-8').write(fix(s))
    print('ok')
