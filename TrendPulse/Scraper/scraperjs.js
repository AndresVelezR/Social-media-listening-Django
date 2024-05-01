import puppeteer from "puppeteer";

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
      try{const result = await page.evaluate(() => {

        const tweets = document.querySelectorAll('article[data-testid="tweet"]')
        const data = [...tweets].map(quote => {
            const txt = quote.querySelector('div[class="css-175oi2r"] div[class="css-1rynq56 r-8akbws r-krxsd3 r-dnmrzs r-1udh08x r-bcqeeo r-qvutc0 r-37j5jr r-a023e6 r-rjixqe r-16dba41 r-bnwqim"] span').innerText
            return {
                txt, 
            }
        })
        return data
    })
    
    for (const [key, value] of Object.entries(result)){
      if (tws.includes(String((Object.values(value)))) == false && counter < limit){
          tws.push(String(Object.values(value)))
          counter = counter + 1;
      }
      if (counter == limit){
        return tws
      }

  }
  }
    catch{}
    await page.mouse.wheel({ deltaY: 100 });
    await new Promise(r => setTimeout(r, 100));
    }
  }
};

(async () => {
  const browser = await puppeteer.launch({ headless: false });
  const page = await browser.newPage();
  await page.goto("https://twitter.com/WestCOL_");
  await new Promise(r => setTimeout(r, 5000));

  const tweets = await scrollLikeHuman(page, 10);
  console.log(tweets)

  await browser.close();
})();