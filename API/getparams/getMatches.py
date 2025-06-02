def getMatches(objfromMain):
    
   #armazenar os dados de cada partida em um dicionário (reaproveitar array para encaminhar liga, times)
    matchData= []
    for index, team in enumerate(objfromMain, start=1):
        # Get the name of the teams
        team_home= team['teams']['home']['name'] 
        team_away= team['teams']['away']['name']

        # Get the score of the teams for match
        score_home= team['goals']['home']
        score_away= team['goals']['away']

        # Get fixture id from each match
        fixture_id= team['fixture']['id']
        fixture_league= team['league']['name']
        

        #store index and fixture id in a array with objects
        matchData.append({str(index): str(fixture_id)})

        print(f"{index}. {team_home} ({score_home}) x {team_away} ({score_away}) - ({fixture_league})")

    return matchData

def getDataFromSpecificMatch(matchData):
    route= "/fixtures?"
    match= int(input("\nEnter the match number to get more details: "))
    data= {
        'id': matchData[match-1][str(match)],
        }
    
   
    return route, data 


# criar metodo para verificar cada liga do dia de hoje
#def verifyLeague()