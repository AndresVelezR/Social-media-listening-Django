import puppeteer from "puppeteer";
import { createRequire } from "module";
const require = createRequire(import.meta.url);
require('dotenv').config();
const fs = require('fs');

const scrollLikeHuman = async (page, limit) => {
  let tws = [];
  let flag = true;
  let counter = 0;

  while (flag) {
    const scrollHeight = await page.evaluate(() => document.body.scrollHeight);
    const viewportHeight = await page.evaluate(() => window.innerHeight);
    const maxScroll = scrollHeight - viewportHeight;

    await page.mouse.move(0, 0);

    for (let y = 0; y < maxScroll; y += 100) {
      try {
        const result = await page.evaluate(() => {

          const tweets = document.querySelectorAll('article[data-testid="tweet"]')
          const data = [...tweets].map(quote => {
            const user = quote.querySelector('div[class="css-146c3p1 r-dnmrzs r-1udh08x r-3s2u2q r-bcqeeo r-1ttztb7 r-qvutc0 r-37j5jr r-a023e6 r-rjixqe r-16dba41 r-18u37iz r-1wvb978"] span').innerText
            const txt = quote.querySelector('div[data-testid="tweetText"]').innerText
            const reply = quote.querySelector('button[data-testid="reply"]').getAttribute('aria-label')
            const retweet = quote.querySelector('button[data-testid="retweet"]').getAttribute('aria-label')
            const like = quote.querySelector('button[data-testid="like"]').getAttribute('aria-label')
            return {
              'user': user,
              'txt': txt,
              'reply': reply,
              'retweet': retweet,
              'like': like,
            }
          })
          return data
        })

        for (const [key, value] of Object.entries(result)) {
          if (tws.find((item) => item.user === value.user) === undefined && counter < limit) {
            tws.push({
              user_tag: value.user,
              tweet: value.txt,
              reply: parseInt(value.reply.match(/\d+/)[0]),
              retweet: parseInt(value.retweet.match(/\d+/)[0]),
              like: parseInt(value.like.match(/\d+/)[0])
            });
            counter++;
          }
          if (counter == limit) {
            return tws
          }
        }
      }
      catch { }
      await page.mouse.wheel({ deltaY: 100 });
      await new Promise(r => setTimeout(r, 100));
    }
  }
};

(async () => {
  const browser = await puppeteer.launch(
    {
      headless: false,
    }
  )
  const page = await browser.newPage()
  await page.setViewport({ height: 900, width: 1440 });
  await page.goto('https://twitter.com/?lang=es')
  await new Promise(r => setTimeout(r, 5000));

  await page.evaluate(() => {
    const xpath = '//span[contains(text(), "Iniciar sesión")]';
    const result = document.evaluate(xpath, document, null, XPathResult.ANY_TYPE, null);

    result.iterateNext().click();
  })
  await new Promise(r => setTimeout(r, 5000));

  await page.type('input[autocomplete="username"]', process.env.USERNAME);
  await page.keyboard.press('Enter');
  await new Promise(r => setTimeout(r, 5000));
  await page.type('input[name="password"]', process.env.PASSWORD);
  await page.keyboard.press('Enter');
  await new Promise(r => setTimeout(r, 5000));
  await page.type('input[aria-label="Búsqueda"]', 'westcol');
  await page.keyboard.press('Enter');
  await new Promise(r => setTimeout(r, 5000));

  const result = await scrollLikeHuman(page, 10);
  console.log(result);

  await browser.close();
})();