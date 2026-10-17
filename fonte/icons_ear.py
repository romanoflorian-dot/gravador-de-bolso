import asyncio
from playwright.async_api import async_playwright
ear=open('ear.svg',encoding='utf-8').read()
OUT='/home/claude/gravador-de-bolso/lite/'
def page(size, k, bg):
    h=size*k; w=h*100/124
    return f'<html><body style="margin:0;width:{size}px;height:{size}px;background:{bg};display:grid;place-items:center">' + ear.replace('class="ear"', f'width="{w}" height="{h}"') + '</body></html>'
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch()
        # 'any' com fundo transparente: na tela de abertura do Android aparece só a orelha, sem quadrado
        for name,size,k,bg in [('icon-192.png',192,.86,'transparent'),('icon-512.png',512,.86,'transparent'),('icon-maskable-512.png',512,.66,'#fff'),('apple-touch-icon.png',180,.8,'#fff')]:
            pg=await b.new_page(viewport={'width':size,'height':size})
            await pg.set_content(page(size,k,bg)); await pg.wait_for_timeout(200)
            await pg.screenshot(path=OUT+name, omit_background=(bg=='transparent'))
        await b.close()
asyncio.run(main())
