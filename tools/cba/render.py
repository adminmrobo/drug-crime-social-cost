import sys
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page()
    for h,o in zip(sys.argv[1::2],sys.argv[2::2]):
        pg.goto('file://'+h); pg.wait_for_timeout(300); pg.pdf(path=o,format='A4',print_background=True,prefer_css_page_size=True)
    b.close()
