import asyncio
from playwright.async_api import async_playwright
svg=open('icon.svg').read()
async def m():
    async with async_playwright() as p:
        b=await p.chromium.launch()
        for n in (180,192,512):
            pg=await b.new_page(viewport={"width":n,"height":n})
            await pg.set_content(f'<body style="margin:0"><div style="width:{n}px;height:{n}px">{svg.replace("width=\"512\" height=\"512\"",f"width=\"{n}\" height=\"{n}\"")}</div></body>')
            await pg.screenshot(path=f"icon-{n}.png"); await pg.close()
        await b.close()
async def m2():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={"width":512,"height":512})
        await pg.set_content('<body style="margin:0">'+open('icon_maskable.svg').read()+'</body>'); await pg.screenshot(path="icon-maskable-512.png"); await b.close()
asyncio.run(m()); asyncio.run(m2())

from PIL import Image
b=Image.open('icon-512.png').convert('RGB')
for n in (180,192): b.resize((n,n),Image.LANCZOS).save(f'icon-{n}.png')
