import asyncio
from pyppeteer import launch
import json



async def scroll_like_human(page, limit):
    tws = []
    flag = True
    counter = 0

    while flag:
        scroll_height = await page.evaluate('document.body.scrollHeight')
        viewport_height = await page.evaluate('window.innerHeight')
        max_scroll = scroll_height - viewport_height

        for y in range(0, max_scroll, 100):
            try:
                result = await page.evaluate('''
                    () => {
                        const tweets = document.querySelectorAll('article[data-testid="tweet"]');
                        const data = Array.from(tweets).map(quote => {
                            const user = quote.querySelector('div[class="css-146c3p1 r-dnmrzs r-1udh08x r-3s2u2q r-bcqeeo r-1ttztb7 r-qvutc0 r-37j5jr r-a023e6 r-rjixqe r-16dba41 r-18u37iz r-1wvb978"] span    ').innerText;                
                            const txt = quote.querySelector('div[data-testid="tweetText"]').innerText;
                            const reply = quote.querySelector('button[data-testid="reply"]').getAttribute('aria-label');
                            const retweet = quote.querySelector('button[data-testid="retweet"]').getAttribute('aria-label');
                            const like = quote.querySelector('button[data-testid="like"]').getAttribute('aria-label');
                            const time = quote.querySelector('time').getAttribute('datetime');
                            return {
                                'user': user,
                                'txt': txt,
                                'reply': reply,
                                'retweet': retweet,
                                'like': like,
                                'time': time
                            };
                        });
                        return data;
                    }
                ''')

                for value in result:
                    if not any(item['user_tag'] == value['user'] for item in tws) and counter < limit:
                        tws.append({
                            'user_tag': value['user'],
                            'time_stamp': value['time'],
                            'tweet': value['txt'],
                            'reply': int(value['reply'].replace(',', '').split()[0]),
                            'retweet': int(value['retweet'].replace(',', '').split()[0]),
                            'like': int(value['like'].replace(',', '').split()[0]),
                        })
                        counter += 1
                    if counter == limit:
                        return tws

            except Exception as e:
                print(f"Error: {e}")

            await page.evaluate('window.scrollBy(0, 100)')
            await asyncio.sleep(0.1)

    return tws

async def main():
    browser = await launch(headless=False, args=['--no-sandbox', '--disable-setuid-sandbox'])
    page = await browser.newPage()
    await page.setViewport({'height': 900, 'width': 1440})
    await page.goto('https://twitter.com/?lang=es')
    await asyncio.sleep(5)

    await page.evaluate('''
        () => {
            const xpath = '//span[contains(text(), "Iniciar sesión")]';
            const result = document.evaluate(xpath, document, null, XPathResult.ANY_TYPE, null);
            result.iterateNext().click();
        }
    ''')
    await asyncio.sleep(5)

    await page.type('input[autocomplete="username"]', "samargo_")
    await page.keyboard.press('Enter')
    await asyncio.sleep(5)
    await page.type('input[name="password"]', "1033177913samargo")
    await page.keyboard.press('Enter')
    await asyncio.sleep(5)
    await page.type('input[aria-label="Búsqueda"]', 'westcol')
    await page.keyboard.press('Enter')
    await asyncio.sleep(5)

    result = await scroll_like_human(page, 10)
    with open('AnalyzerApp/ScrapingData.json', 'w') as f:
        json.dump(result, f)
        print("JSON guardado correctamente.")
    print(result)


    await browser.close()

asyncio.get_event_loop().run_until_complete(main())
