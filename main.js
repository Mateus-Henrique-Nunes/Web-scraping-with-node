const express = require('express');
const app = express();
const pup = require('puppeteer');
const url = 'https://www.flashscore.com.br';



const main = async (time) => {
    let browser;
    try {

         browser = await pup.launch({
            headless: true, args: [
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-dev-shm-usage',
                '--disable-accelerated-2d-canvas',
            ]
        });

        const page = await browser.newPage();

        await page.setRequestInterception(true);
        page.on('request', (req) => {
            try {
                const resourceType = req.resourceType();
                if (['image', 'font', 'media'].includes(resourceType)) {
                    req.abort();
                } else {
                    req.continue();
                }
            } catch (e) {
                req.continue();
            }
        });

        await page.goto(url, { timeout: 10000 });


        await page.click("#search-window")
        await page.waitForSelector(".searchInput__input");
        await page.type(".searchInput__input", "Manchester City");
        await page.waitForSelector('.searchResult')



        await Promise.all([
            page.waitForNavigation(),
            page.click('.searchResult')

        ])


        await page.waitForSelector('#li2')
        const link = await page.evaluate(() => {
            const link = document.querySelector('#li2').getAttribute('href');
            return link;
        })


        await page.goto(`https://www.flashscore.com.br${link}`, { timeout: 2000 });

        const linkMatchs = await page.evaluate(() => {
            const matchs = Array.from(document.querySelectorAll('.event__match>a'));
            const link = matchs.map((e) => {
                return e.getAttribute('href');
            })
            return link;
        })

        const sufixlink = '/estatisticas-de-jogo/0'

        // const fullLink=linkMatchs[0]+sufixlink;
        // await page.goto(fullLink)


        const awaitStatistics = async () => {
            await page.waitForSelector('.wcl-category_ITphf')
            await page.waitForSelector('.participant__participantName>a')
            const cornerKicks = await page.evaluate(() => {
                const teams = Array.from(document.querySelectorAll('.participant__participantName>a'));
                const wrapper = Array.from(document.querySelectorAll('.wcl-category_ITphf'));
                const content = wrapper.map((e) => {
                    const contenItSelf = Array.from(e.querySelectorAll('strong'));

                    return contenItSelf.map(e => e.innerText)


                });
                return {
                    TeamHome: teams[0].innerText, TeamAway: teams[1].innerText,
                    Statistics: content
                };

            });

            return cornerKicks

        }

        const matchs = {}
        for (i = 0; i <= 3; i++) {
            try {
                const fullLink = linkMatchs[i] + sufixlink;
                await page.goto(fullLink, { timeout: 2000 })
                const data = await awaitStatistics();
                matchs[i] = data
            } catch (err) {
                console.error('Erro identificado: ', err)
            }


        }


        await browser.close();
        return matchs

        /*
            Próximas etapas:
            1. Organizar saida no cornerKicks, mais especificamente no return {TeamHome....}
            2. Tirar media dos dados essenciais (escanteios e chutes a gol)
            3. Criar uma rota para acessar os dados em Json (matchs.json()?)
        */

    }
    catch (err) {
        console.error('Erro geral: ', err)
        if (browser) {
            await browser.close();
        }
    }

}



main().then((data) => {
    console.log(data)
})