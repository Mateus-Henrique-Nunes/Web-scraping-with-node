import http.client
import json
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv
import os
from IaToCorrectname import chat
from unidecode import unidecode

def app():
    load_dotenv()
    TOKEN= os.getenv("TOKEN")
    BOT_USERNAME= os.getenv("BOT_USERNAME")

    print("Starting bot...")
    
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(MessageHandler(filters.TEXT, handle_text))

    print("Bot is running...")
    app.run_polling()
   


def main(team):


    url= 'localhost:3000'
    conn = http.client.HTTPConnection(url)
    team = ''.join(word.capitalize() for word in team.split())
    conn.request("GET", "/"+ team)

    try:
        res= conn.getresponse()

        content= res.read()
        object_json= json.loads(content)

        print(json.dumps(object_json, indent=2, ensure_ascii=False ))
        return object_json
        

    except Exception as e:
        print(f"An error occurred: {e}")


# tira a media de escanteios e chutes dos times
def get_average(content):
    shots=[]
    corners=[]
    for key, value in content['matchs'].items():
        if value.get('erro'):
           continue
        else:
            team= content['teamSearch']
            teamhome= value["Teams"]["Teamhome"]
        
            if team== teamhome:
                cornerskick= int(value["Content"]["Escanteios"]['home'])
                shotskick= int(value["Content"]["Finalizações no alvo"]["home"])
                corners.append(cornerskick)
                shots.append(shotskick)
            else:
                cornerKick= int(value["Content"]["Escanteios"]['away'])
                shotsKick= int(value["Content"]["Finalizações no alvo"]["away"])
                corners.append(cornerKick)
                shots.append(shotsKick)

    if corners and shots:        
        averagecorners= sum(corners)/len(corners) 
        averageshots= sum(shots)/len(shots)
    else:
       averagecorners=0
       averageshots=0 
    return round(averagecorners, 2), round(averageshots, 2)

#Até agora é a principal função para lidar com os dados
def handle_message(text):
    try:
        content= main(unidecode(text))
        message=[]
        averagecorners, averageshots= get_average(content)
        if content is None:
            return message, 0, 0
        for key, value in content['matchs'].items():
            if value.get('erro'):
                continue
            else:
                teamhome= value["Teams"]["Teamhome"]
                teamaway= value["Teams"]["TeamAway"]
                cornershome= value["Content"]["Escanteios"]['home']
                cornersaway= value["Content"]["Escanteios"]['away']
                shotshome= value["Content"]["Finalizações no alvo"]["home"]
                shotsaway= value["Content"]["Finalizações no alvo"]["away"]
                message.append(f'{key}\n{teamhome} vs {teamaway}\nJogando em casa: {teamhome}\nJogando como visitante: {teamaway}\n\n***Escanteios***\nEscanteios para o time de casa: {cornershome}\nEscanteios para o time visitante: {cornersaway}\n\n***Chutes a Gol***\nTime de casa: {shotshome}\nTime visitante: {shotsaway}')
        
        return message, averagecorners, averageshots, content['nextFixture']
    except Exception as e:
        print(f'Erro detected: {e}')
        return [], 0, 0


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE): 
    await update.message.reply_text("Olá, bem vindo ao Nortebet, digite abaixo o nome do time o qual gostaria de extrair informações")
    

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name= update.message.from_user.first_name
    text: str = update.message.text
    await update.message.reply_text(f"Aguarde um momento enquanto busco os dados dos os ultimos 5 jogos do {text}.... ")
   
    # API that's IA fix the name of the team

    #newtext= chat(text)
    message, averagecorners, averageshots, nextFixture= handle_message(text)
    if not message:
        await update.message.reply_text("SEM DADOS SOBRE O TIME")
    else:
        for item in message:
            await update.message.reply_text(item)

        await update.message.reply_text(f'Media de escanteios: {averagecorners}\nMedia de chutes a gol: {averageshots}\nProximo jogo: {nextFixture}')
        await update.message.reply_text(f"{user_name}, aqui estão os dados")



if __name__ == '__main__':
 
    app()



