

import json
import time
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from playwright.sync_api import sync_playwright
from func import saving_files




BASE_URL = "https://animepahe.si"
url = "https://animepahe.si/play/0404f6c2-7839-3890-2225-e7a7d3fd7b9e/"
path = 'CSV_FILES/MOVIES.csv'


with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    page.goto(url, timeout=60000)
    page.wait_for_selector("a.play", timeout=60000)
    html = page.content()
    soup = BeautifulSoup(html, "lxml")

    episode_links = [urljoin(BASE_URL, a["href"])for a in soup.select("a.play")]
    print(f"Found {len(episode_links)} episodes")

    for ep_url in episode_links:
        print("\nVisiting:", ep_url)
        page.goto(ep_url, timeout=60000)
        page.wait_for_selector("#downloadMenu", timeout=60000)
        download_links = page.eval_on_selector_all(
            "#pickDownload a.dropdown-item",
            "els => els.map(e => ({text: e.innerText.trim(), url: e.href}))")

        item_url = [item["url"] for item in download_links]
        item_text = [item["text"] for item in download_links]
        print(item_url)
        print(item_text)
        time.sleep(9999)  # Pause to inspect the links before proceeding


        DQ = 0
        CAT = 'SUB' #SELECT SUB [ENGLISH SUB] AND DUB [ENGLISH DUB]
        QT = '360'  # SELECT QUALITY 360p, 720p, 1080p
        CAT_QT = [x for x in item_text if QT in x]
        if CAT_QT:
            DQ1 = CAT_QT[0]
            DQ = item_text.index(DQ1)
        else:
            print('\n DIDNT SELECT THE RIGHT QUALITY [360,720,1080] \n DEFAULTING TO QUALITY [360P] ')
        page.goto(item_url[DQ], timeout=60000)

        page.wait_for_selector("a.redirect", timeout=60000)
        continue_link = page.locator("a.redirect", has_text="Continue").get_attribute("href")
        print("Continue URL:", continue_link)
        page.goto(continue_link, timeout=60000)
        page.wait_for_selector("form", timeout=60000)

        form = page.locator("form",has=page.locator("button", has_text="Download"))
        movie_name = page.locator("h1.title").inner_text().strip()
        post_url = form.get_attribute("action")
        token = form.locator("input[name='_token']").get_attribute("value")
        cookies = page.context.cookies()

        with open(f"CSV_FILES/{movie_name}.json", "w") as f:
            json.dump(cookies, f)
        data = {
            'NAME': [movie_name],
            'POST_URL': [post_url],
            'TOKEN': [token]
        }
        saving_files(data=data, path=path)





