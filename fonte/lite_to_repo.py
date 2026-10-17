import os, sys
from lite_fix import fix
S, R = sys.argv[1], sys.argv[2]
src = open(os.path.join(S, 'gravador-de-bolso-lite.html'), encoding='utf-8').read()
i = src.index('<div class="wrap">'); head, body = src[:i].strip(), src[i:].strip()
top = '<!doctype html>\n<html lang="pt-BR">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
extra = ('<meta name="theme-color" content="#ffffff">\n<link rel="manifest" href="manifest.webmanifest">\n'
         '<link rel="icon" type="image/png" sizes="192x192" href="icon-192.png">\n<link rel="apple-touch-icon" href="apple-touch-icon.png">\n')
CDN = '<script src="https://cdn.jsdelivr.net/npm/lamejs@1.2.1/lame.min.js"></script>'
open(os.path.join(R, 'lite', 'index.html'), 'w', encoding='utf-8').write(fix(top + extra + head + '\n</head>\n<body>\n' + body.replace(CDN, '<script src="lame.min.js"></script>') + '\n</body>\n</html>\n'))
open(os.path.join(S, 'dist', 'gravador-de-bolso-lite.html'), 'w', encoding='utf-8').write(top + head + '\n</head>\n<body>\n' + body + '\n</body>\n</html>\n')
print('ok')
