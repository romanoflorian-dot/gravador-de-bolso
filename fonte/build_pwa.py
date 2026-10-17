"""Gera o pacote instalável (PWA) e a versão de arquivo único a partir da fonte da página."""
import os, json, shutil
from PIL import Image, ImageDraw

D = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(D, 'gravador-de-bolso.html')
PWA = os.path.join(D, 'pwa', 'gravador-de-bolso')
DIST = os.path.join(D, 'dist')
shutil.rmtree(os.path.join(D, 'pwa'), ignore_errors=True)
os.makedirs(PWA); os.makedirs(DIST, exist_ok=True)

src = open(SRC, encoding='utf-8').read()
i = src.index('<div class="wrap">')
head, body = src[:i].strip(), src[i:].strip()
CDN = '<script src="https://cdn.jsdelivr.net/npm/lamejs@1.2.1/lame.min.js"></script>'
assert CDN in body

def page(head_extra, body_text):
    return ('<!doctype html>\n<html lang="pt-BR">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
            + head_extra + head + '\n</head>\n<body>\n' + body_text + '\n</body>\n</html>\n')

# arquivo único (sem instalação)
open(os.path.join(DIST, 'gravador-de-bolso.html'), 'w', encoding='utf-8').write(page('', body))

# PWA
pwa_head = ('<meta name="theme-color" content="#151816">\n'
            '<meta name="description" content="Gravar, cortar, tratar e exportar áudio para trabalhos de arte sonora.">\n'
            '<link rel="manifest" href="manifest.webmanifest">\n'
            '<link rel="icon" type="image/png" sizes="192x192" href="icon-192.png">\n'
            '<link rel="apple-touch-icon" href="apple-touch-icon.png">\n'
            '<meta name="apple-mobile-web-app-capable" content="yes">\n'
            '<meta name="mobile-web-app-capable" content="yes">\n')
open(os.path.join(PWA, 'index.html'), 'w', encoding='utf-8').write(
    page(pwa_head, body.replace(CDN, '<script src="lame.min.js"></script>')))

manifest = {
    "name": "Gravador de Bolso", "short_name": "Gravador",
    "description": "Gravar, cortar, tratar e exportar áudio para trabalhos de arte sonora.",
    "lang": "pt-BR", "dir": "ltr", "start_url": "./", "scope": "./", "id": "./",
    "display": "standalone", "orientation": "any",
    "background_color": "#e8ebe6", "theme_color": "#151816",
    "categories": ["music", "education", "utilities"],
    "icons": [
        {"src": "icon-192.png", "sizes": "192x192", "type": "image/png", "purpose": "any"},
        {"src": "icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any"},
        {"src": "icon-maskable-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"}
    ]
}
json.dump(manifest, open(os.path.join(PWA, 'manifest.webmanifest'), 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

SW = r"""/* Gravador de Bolso — funciona sem internet depois da primeira visita */
const CACHE = 'gravador-de-bolso-v1';
const SHELL = ['./', './index.html', './manifest.webmanifest', './lame.min.js',
  './icon-192.png', './icon-512.png', './icon-maskable-512.png', './apple-touch-icon.png'];
self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(SHELL)).then(() => self.skipWaiting()));
});
self.addEventListener('activate', e => {
  e.waitUntil(caches.keys()
    .then(ks => Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k))))
    .then(() => self.clients.claim()));
});
self.addEventListener('fetch', e => {
  const r = e.request;
  if (r.method !== 'GET') return;
  if (r.mode === 'navigate') {
    // página: tenta a rede (para receber atualizações) e cai no que está guardado
    e.respondWith(fetch(r).then(res => {
      const cp = res.clone(); caches.open(CACHE).then(c => c.put('./index.html', cp)); return res;
    }).catch(() => caches.match('./index.html')));
    return;
  }
  // demais arquivos (ícones, MP3, fontes): o que está guardado primeiro
  e.respondWith(caches.match(r).then(hit => hit || fetch(r).then(res => {
    if (res.ok || res.type === 'opaque') { const cp = res.clone(); caches.open(CACHE).then(c => c.put(r, cp)); }
    return res;
  })));
});
"""
open(os.path.join(PWA, 'sw.js'), 'w', encoding='utf-8').write(SW)

# ícones: botão de gravar sobre a face escura do aparelho
def icon(size, maskable=False, rounded=True):
    S = 1024
    im = Image.new('RGBA', (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    bg = (21, 24, 22, 255)
    if maskable or not rounded:
        d.rectangle([0, 0, S, S], fill=bg)
    else:
        d.rounded_rectangle([0, 0, S - 1, S - 1], radius=int(S * 0.22), fill=bg)
    k = 0.78 if maskable else 1.0          # área segura dos ícones adaptáveis
    c = S / 2
    ring_r, ring_w, dot_r = 330 * k, 46 * k, 200 * k
    d.ellipse([c - ring_r, c - ring_r, c + ring_r, c + ring_r], outline=(223, 232, 226, 255), width=int(ring_w))
    d.ellipse([c - dot_r, c - dot_r, c + dot_r, c + dot_r], fill=(222, 52, 38, 255))
    return im.resize((size, size), Image.LANCZOS)

icon(192).save(os.path.join(PWA, 'icon-192.png'))
icon(512).save(os.path.join(PWA, 'icon-512.png'))
icon(512, maskable=True).save(os.path.join(PWA, 'icon-maskable-512.png'))
icon(180, rounded=False).convert('RGB').save(os.path.join(PWA, 'apple-touch-icon.png'))

shutil.copy(os.path.join(D, 'package', 'lame.min.js'), os.path.join(PWA, 'lame.min.js'))
shutil.copy(os.path.join(D, 'package', 'LICENSE'), os.path.join(PWA, 'LICENSE-lamejs.txt'))

LEIA = """GRAVADOR DE BOLSO — app para gravar, cortar, tratar e exportar áudio

Esta pasta é o app completo. Ela precisa ficar num endereço https para
gravar pelo microfone e para ser instalada como aplicativo.

1. PUBLICAR A PASTA (uma vez)
   Opção A — GitHub Pages (gratuito):
     - Crie uma conta em github.com e um repositório novo, por exemplo "gravador".
     - Envie todos os arquivos desta pasta (Add file > Upload files).
     - Em Settings > Pages, escolha a branch "main" e salve.
     - O endereço será https://SEU-USUARIO.github.io/gravador/
   Opção B — qualquer servidor https (site da universidade, por exemplo):
     - Copie a pasta inteira para o servidor e use o endereço dela.

2. INSTALAR NO APARELHO (cada estudante)
   Android (Chrome): abra o endereço e toque em "Instalar como app",
     ou no menu ⋮ > "Instalar app" / "Adicionar à tela inicial".
   Windows ou Mac (Chrome ou Edge): abra o endereço e clique em
     "Instalar como app" ou no ícone de instalar na barra de endereço.
     O app ganha ícone no menu Iniciar e janela própria.
   iPhone (Safari): botão Compartilhar > "Adicionar à Tela de Início".

   Depois da primeira abertura, o app funciona sem internet.

3. ATUALIZAR
   Troque os arquivos no servidor e, no arquivo sw.js, mude o número em
   CACHE = 'gravador-de-bolso-v1' (por exemplo para v2). Os aparelhos
   recebem a versão nova na próxima vez que abrirem o app com internet.

Tudo é processado no aparelho de quem usa; nenhum áudio é enviado.
O codificador de MP3 é o lamejs (licença LGPL-3.0, ver LICENSE-lamejs.txt).
"""
open(os.path.join(PWA, 'LEIA-ME.txt'), 'w', encoding='utf-8').write(LEIA)
print('ok:', sorted(os.listdir(PWA)))
