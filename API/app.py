import http.client
import json
from urllib.parse import urlencode
from getparams.selectLeague import getLeague
from getparams.getMatches import getMatches
from getparams.getMatches import getDataFromSpecificMatch
from getparams.organizeStatistics import getBothTeamsAndLeague
from dotenv import load_dotenv
import os

def requestToApi(route, data):
    load_dotenv()
    url='v3.football.api-sports.io'
    KEY= os.getenv("API_KEY")
    conn = http.client.HTTPSConnection(url)

    headers = {
        'x-rapidapi-host': "v3.football.api-sports.io",
        'x-rapidapi-key': KEY
        }
    data = urlencode(data)
    conn.request("GET",route + data, headers=headers)
    res= conn.getresponse()
    content = res.read()
    object_json = json.loads(content)
    conn.close()
    return object_json['response']


def main():
    try:
        # function to request data from the API
        # Get the league and season from user input
        route, data = getLeague()
        geting_content= requestToApi(route, data)

        #get the list with the id matches and show every match in the terminal
        machData= getMatches(geting_content)
        valid_userInput= str(input("\nWanna know more about a match ? (Y/N): "))

        if valid_userInput.lower()== "y":
            new_route, new_data= getDataFromSpecificMatch(machData)
            object_json= requestToApi(new_route, new_data)
            getBothTeamsAndLeague (object_json)
           
            
        else:
            print("Programn finished!")


    # Criar um metodo para organizar os dados vindo do getDataFromSpecificMatch
    # Ambiente deve ser separado para evitar conflitos e facilitar o teste

    
    except Exception as e:
     print(f"An error occurred: {e}")

    
if __name__ == "__main__":
   main()