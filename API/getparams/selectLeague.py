from datetime import date
def getLeague():
 today = date.today()
 league= int(input("***************************************** " \
 "\n1. Champions league \n2. Copa do Brasil \n3. Libertadores \n4. Premier League  \n5. Today matches\n"
 "***************************************** \n" \
 "Enter a league: "))   
 
 route= '/fixtures?'

 league_value=[2,73,13,39]
 
 if league < 1 or league > 5:
      print("Invalid league selection")
      return None, None
 
 elif league==5:
    data={
        'date': str(today),
    }
 else:
    season= int(input("Enter a season: "))
    data={
        'league': league_value[league-1],
        'season': season,
     } 
    
 return  route, data



     