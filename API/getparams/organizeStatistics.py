#/fixtures?id=1208815
def getBothTeamsAndLeague(contents):
    import sys
    from pathlib import Path
    sys.path.append(str(Path(__file__).parent.parent))
    from app import requestToApi
    
    route='/teams/statistics?'
    
    for content in contents:
        team_home= content['teams']['home']['name']
        team_away= content['teams']['away']['name']
        team_home_id= content['teams']['home']['id']
        team_away_id= content['teams']['away']['id']

        league_id= content['league']['id']
        league_name= content['league']['name']
        league_season= content['league']['season']

        team_home_goals, team_away_goals= content['goals']['home'], content['goals']['away']

    teams_id= [team_home_id, team_away_id]

    print("***********Teams***************")
    print(f"Home team: {team_home} ({team_home_goals})")  
    print(f"Team away: {team_away} ({team_away_goals})\nLeague Name: {league_name}")
    

    for team in teams_id:
       
        data={
        'league': str(league_id),
        'team': str(team),
        'season':"2023" #atenção 
        }
       
        object_json= requestToApi(route, data)
        getStatisticsFromTeams(object_json)
   

#teams/statistics?league=39&team=33&season=2019
def getStatisticsFromTeams(statistics_content):

    
    team= statistics_content['team']['name']
    fixtures= statistics_content['fixtures']
    wins_home= fixtures['wins']['home']
    wins_away= fixtures['wins']['away']
    draws_home= fixtures['draws']['home']
    draws_away= fixtures['draws']['away']
    loses_home= fixtures['loses']['home']
    loses_away= fixtures['loses']['away']

    # Media de gols a favor 
    goals_for= statistics_content['goals']['for']
    average_goals_home= goals_for['average']['home']
    average_goals_away= goals_for['average']['away']
    average_goals_for= goals_for['average']['total']
   

    # Media de gols contra
    goals_against= statistics_content['goals']['against']
    goals_against_home= goals_against['average']['home']
    goals_against_away= goals_against['average']['away']
    average_goals_against= goals_against['average']['total']

    print("***********INFO***************")
    print(f"Team: {team}")
    print(f"Wins Home: {wins_home}")
    print (f"Loses in home: {loses_home}")
    print(f"Average goals in home: {average_goals_home}")
    print(f"Average goals conceded at home: {goals_against_home} ")
    print(f"Average goals away: {average_goals_away}")
    print (f"Average goals conceded away: {goals_against_away}")
   
    #print (goals_for['minute'])
    # Minutos onde o time mais faz gol
    minutesWithMoregoals(goals_for['minute'])


def minutesWithMoregoals(object_data):
    print("***********Minutes with more goals***************")
    for minute in object_data:
        print(f"Minuto:{minute} goals: {object_data[minute]['total']}")
