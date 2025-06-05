const express = require('express');
const app = express();
const pup = require('puppeteer');
const url = 'https://www.flashscore.com.br';
const sufixlink = '/estatisticas-de-jogo/0'


app.get("/favicon.ico", (req, res) => {
    res.status(204).end();
})

app.get("/:time", (req, res) => {
    const time = req.params.time.replace(/([a-z])([A-Z])/g, '$1 $2');
    main(time).then((data) => {
        res.status(200).json(data);
        console.log('Dados enviados com sucesso');
    }).catch((err) => {
        console.error('Erro ao buscar dados: ', err);
        res.status(500).json({ error: 'Erro ao buscar dados' });
    })
})

const main = async (time) => {
    let teamSearch;
    let browser;
    let matchs = {}

    try {

        browser = await pup.launch({
            headless: false, args: [
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
        await page.type(".searchInput__input", time);
        await page.waitForSelector('.searchResult')

        //Get team correct name
        teamSearch= await page.evaluate(()=>{
            return time= document.querySelector('.searchResult__participantName').innerText
        })
         

        await Promise.all([
            page.waitForNavigation(),
            page.click('.searchResult')

        ])


        // await page.waitForSelector('#li2')
        // const link = await page.evaluate(() => {
        //     const link = document.querySelector('#li2').getAttribute('href');
        //     return link;
        // })


        // await page.goto(`https://www.flashscore.com.br${link}`, { timeout: 10000 });


        // Ambiente de teste

        await page.waitForSelector('.summary-results')
        const nextFixture= await page.evaluate(() => {
            const nextFixture = document.querySelector('.summary-fixtures>.sportName>.event__match');
            const home = nextFixture.querySelector('.event__homeParticipant').innerText;
            const away = nextFixture.querySelector('.event__awayParticipant').innerText;
            return {nextMatch: `${home} vs ${away}`};
        })

        // fim do ambiente de teste

        const linkMatchs = await page.evaluate(() => {
            // before: .event__match>a
            const matchs = Array.from(document.querySelectorAll('.summary-results>.sportName>.event__match>a'));
            const link = matchs.map((e) => {
                return e.getAttribute('href');
            })
            return link;
        })



        const awaitStatistics = async () => {

            try {
                await page.waitForSelector('.wcl-category_ITphf', {timeout:10000})
                await page.waitForSelector('.participant__participantName>a')
                const cornerKicks = await page.evaluate(() => {
                    const teams = Array.from(document.querySelectorAll('.participant__participantName>a'));
                    const wrapper = Array.from(document.querySelectorAll('.wcl-category_ITphf'));
                    const content = wrapper.map((e) => {
                        const contenItSelf = Array.from(e.querySelectorAll('strong'));

                        return contenItSelf.map(e => e.innerText)
                    });

                    // Organize content into an object
                    const newContent = content.reduce((acc, e) => {
                        acc[e[1]] = { home: e[0], away: e[2] };
                        return acc;
                    }, {})

                

                    return {
                        Teams: { Teamhome: teams[0].innerText, TeamAway: teams[1].innerText },
                        Content: newContent,
                    };

                });

                return cornerKicks
            } catch (err) {
                console.error('Erro ao buscar estatísticas: '+ err);
                return {erro: 'partida sem dados'}
            }

        }

        matchs['teamSearch']= teamSearch;
        matchs['nextFixture']= nextFixture.nextMatch;
        const eachfixture={}
        for (i = 0; i <= 4; i++) {
            try {
                const fullLink = linkMatchs[i] + sufixlink;
                await page.goto(fullLink, { timeout: 2000 })                               
                const data = await awaitStatistics();
                eachfixture[`Jogo ${i+1}`]= data//{teamSearch:teamSearch, ...nextFixture, ...data}
            } catch (err) {
                console.error('Erro identificado: ', err)
                continue
            }


        }
        matchs['matchs'] = eachfixture;

        await browser.close();
        return matchs

    }
    catch (err) {
        console.error('Erro geral: ', err)
        if (browser) {
            await browser.close();
        }
    }

}

app.listen(3000, () => {
    console.log('Servidor rodando na porta 3000');
});
