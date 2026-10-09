from bs4 import BeautifulSoup
from func import saving_files,sorting_values
import pandas as pd
import requests,difflib,os
        



def get_results(url1,url2,data_col1,data_col2,data):
    all_res = requests.get(url1)
    soup = BeautifulSoup(all_res.content,"html.parser")
    all_result = soup.find_all('tr')
    for x in all_result:
        x = x.text.split('\n')
        if 'Probability' in x[0]:
            data[data_col1].append(float(x[0].replace('Probability 1 x 2','').split('%')[0].strip()))

    all_res2 = requests.get(url2)
    soup = BeautifulSoup(all_res2.content,"html.parser")
    all_result = soup.find_all('tr')
    for x in all_result:
        x = x.text.split('\n')
        if 'Probability' in x[0]:
            data[data_col2].append(float(x[0].replace('Probability 1 x 2','').split('%')[2].strip()))




def search_calculate(path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'CALCULATED_MATCH_FILE.csv')):
    try:
        os.remove(path)
    except:
        pass 
    all_european_teams = list(pd.read_csv(os.path.join(os.path.dirname(os.path.abspath(__file__)),'EUROPEAN_TEAMS.csv'))['COUNTRY'])
    all_european_teams = [x.replace(' ','') for x in all_european_teams]

    user_input = 'live'#input(' \n >>>>> ( LIVE GAME OR DAY GAME ) :')
    
    if 'live' in user_input.lower():
        usage_match_path = pd.read_csv(os.path.join(os.path.dirname(os.path.abspath(__file__)),'LIVE_MATCH_FILE.csv'))
    if 'day' in user_input.lower():
        usage_match_path = pd.read_csv(os.path.join(os.path.dirname(os.path.abspath(__file__)),'DAY_MATCH_FILE.csv'))

    for x in range(len(usage_match_path)):
        home_team = usage_match_path['HOME TEAM'][x]
        away_team = usage_match_path['AWAY TEAM'][x]
        oo_rating = usage_match_path['OPEN ODD'][x]
        ao_rating = usage_match_path['AVAL ODD'][x]
        winner = usage_match_path['WINNER'][x]
        print(home_team)
        print(away_team)

        home_aval_team = difflib.get_close_matches(home_team,all_european_teams,n=1,cutoff=0.75)
        away_aval_team = difflib.get_close_matches(away_team,all_european_teams,n=1,cutoff=0.75)

        if len(home_aval_team) > 0 and len(away_aval_team) > 0:
            boss = 'Manchester City'
            home_h_url = f'https://www.soccer-rating.com/calculator.php?team1s={home_team}&team2s={boss}'
            home_a_url = f'https://www.soccer-rating.com/calculator.php?team1s={boss}&team2s={home_team}'

            away_h_url = f'https://www.soccer-rating.com/calculator.php?team1s={away_team}&team2s={boss}'
            away_a_url = f'https://www.soccer-rating.com/calculator.php?team1s={boss}&team2s={away_team}'

        if len(home_aval_team) < 1 and len(away_aval_team) < 1:
            boss = 'South Korea'
            home_h_url = f'https://www.soccer-rating.com/calculator_world.php?team1s={home_team}&team2s={boss}'
            home_a_url = f'https://www.soccer-rating.com/calculator_world.php?team1s={boss}&team2s={home_team}'
 
            away_h_url = f'https://www.soccer-rating.com/calculator_world.php?team1s={away_team}&team2s={boss}'
            away_a_url = f'https://www.soccer-rating.com/calculator_world.php?team1s={boss}&team2s={away_team}'
            

        data = {
            'HOME TEAM': home_team,
            'AWAY TEAM': away_team,
            'OPEN RATING':oo_rating,
            'AVAL RATING':ao_rating,

            'HOME H PROBA': [],
            'HOME A PROBA': [],
            'AWAY H PROBA':[],
            'AWAY A PROBA':[],

            'MY WINNER':[],
            'SOCCERVISTA WINNER':winner,
            'WIN REP':[]
            }

        try:
            get_results(url1=home_h_url,url2=home_a_url,data_col1='HOME H PROBA',data_col2='HOME A PROBA',data=data)
            get_results(url1=away_h_url,url2=away_a_url,data_col1='AWAY H PROBA',data_col2='AWAY A PROBA',data=data)
            
            if float(data['HOME H PROBA'][0]) > float(data['AWAY H PROBA'][0]) and float(data['HOME A PROBA'][0]) > (data['AWAY A PROBA'][0]):
                data['MY WINNER'].append(data['HOME TEAM'])

            if float(data['AWAY H PROBA'][0]) > float(data['HOME H PROBA'][0]) and float(data['AWAY A PROBA'][0]) > (data['HOME A PROBA'][0]):
                data['MY WINNER'].append(data['AWAY TEAM'])
            if len(data['MY WINNER']) == 0:
                data['MY WINNER'].append('NONE')

            if data['MY WINNER'][0].strip() in winner:
                data['WIN REP'].append(1)
            if data['MY WINNER'][0].strip() not in winner:
                data['WIN REP'].append(0)

            saving_files(data=data,path=path)
        except Exception as e:
            print(f' \n {e} \n ')
    try:
        sorting_values(path=path,path_to_save=path,value='WIN REP',ascending_mode=False)
    except:
        pass
 
search_calculate()

