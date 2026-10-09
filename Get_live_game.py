from bs4 import BeautifulSoup
from func import drop_similar,drop_duplicate
import pandas as pd
import requests,os





def get_live_game(Live_match_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'LIVE_MATCH_FILE.csv')):
    try:
        os.remove(Live_match_path)
    except:
        pass

    url =f'https://www.soccer-rating.com/live-tips'

    res = requests.get(url)
    soup = BeautifulSoup(res.content,"html.parser")
    data = {
        'HOME TEAM': [],
        'AWAY TEAM': [],

        'OPEN ODD': [],
        'AVAL ODD': [],
        'WINNER':[]
        }
    
    all_live = soup.find_all('tr')
    for a in all_live:

        a = a.text.split('\n')
        if 'Early Tips' in a[0]:
            break
        print('\t \t LEN a =',len(a))

        if len(a)==3:
            odd =a[0].split('  ')[0].split(' ')[0]
            home_team1 = a[0].split('  ')[0].split(' ')[1:]
            home_team = ''
            for x in home_team1:
                home_team+= ' '+x

            for y in home_team:
                if y.islower() == True:
                    home_team_starts = home_team.index(y)
                    break
            home_team = home_team[home_team_starts-1:].replace('↑','').replace('↓','').strip()

            ao_rating = a[1]

            away_team1 = a[0].split('  ')[1].replace('↑','').replace('↓','').strip()
            for x in away_team1[::-1]:  
                try:
                    int(x)
                    away_team1_index = away_team1.index(x)
                except:
                    if away_team1[away_team1_index-1] == '-':
                        oo_rating = '-'+away_team1[away_team1_index:]
                    away_team = away_team1[0:away_team1_index-1].replace('↑','').replace('↓','').strip()
                    break
                
            print(odd)
            print(home_team)        
            print(away_team)
            print(oo_rating)
            print(ao_rating)
            data['HOME TEAM'].append(home_team)
            data['AWAY TEAM'].append(away_team)

            data['OPEN ODD'].append(oo_rating)
            data['AVAL ODD'].append(ao_rating)

            if int(oo_rating) <0:
                data['WINNER'].append(home_team)
            else:
                data['WINNER'].append(away_team)

            # saving_files(data=data,path=Live_match_path)



        if len(a)==4:
            oo_rating = a[1]
            ao_rating = a[2]
            odd =a[0].split('  ')[0].split(' ')[0]
            home_team1 = a[0].split('  ')[0].split(' ')[1:]

            home_team = ''
            for x in home_team1:
                home_team+= ' '+x
            for y in home_team:
                if y.islower() == True:
                    home_team_starts = home_team.index(y)
                    break
            home_team = home_team[home_team_starts-1:].replace('↑','').replace('↓','').replace('(W)','(Women)').strip()
            
            away_team1 = a[0].split('  ')[1].replace('↑','').replace('↓','').strip()
            for x in away_team1[::-1]:
                try:
                    int(x)
                    away_team1_index = away_team1.index(x)
                except:
                    away_team = away_team1[0:away_team1_index-1].replace('↑','').replace('↓','').strip()
                    break
            print(odd)
            print(home_team)        
            print(away_team)
            print(oo_rating)
            print(ao_rating)

            data['HOME TEAM'].append(home_team)
            data['AWAY TEAM'].append(away_team)

            data['OPEN ODD'].append(oo_rating)
            data['AVAL ODD'].append(ao_rating)

            if int(oo_rating) <0:
                data['WINNER'].append(home_team)
            else:
                data['WINNER'].append(away_team)

            # saving_files(data=data,path=Live_match_path)

    df = pd.DataFrame(data)
    df.to_csv(Live_match_path,index=False)

    drop_similar(path=Live_match_path,val1='HOME TEAM',val2='AWAY TEAM')
    drop_duplicate(path=Live_match_path)
get_live_game()