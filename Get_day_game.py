from func import saving_files,main_date,drop_similar,drop_duplicate
from bs4 import BeautifulSoup
import pandas as pd
import requests,os




def get_day_games(currently_date = 0,day_match_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'DAY_MATCH_FILE.csv')):
    try:
        os.remove(day_match_path)
    except:
        pass
    url =f'https://www.soccer-rating.com/today.php?date={str(main_date(currently_date))}&timezone=1'

    res = requests.get(url)
    soup = BeautifulSoup(res.content,"html.parser")

    links = [name.get('href') for name in soup.findAll('a')]

    link_exceptions = ['https://www.soccer-rating.com/', '/', '/login', '/login', '/live-tips', '/sure-bets', '/football-country-ranking/', '/football-odds-calculator', '/tips/', '/today-prediction', '/picks', '/betting-tools', '/banker-bets', '/betting-challenge', '/bet', '/newsletter', '/strange-odds', '/lucky.php', '/wlogin.php', '/tips/', '/vip', '/bet', "javascript:if (document.getElementById('help').style.display!='block') {document.getElementById('help').style.display='block';} else {document.getElementById('help').style.display='none';};void(0)", '/picks', '/banker-bets', '/tips/', '/football-odds-calculator', '/sure-bets', '/strange-odds', '/wlogin.php', '/vip', '/profile.php', '/betting-challenge', '/bet', '/today.php?all=1', 'today.php?leagues=1']

    all_link = []
    for link in links:
        if link != None:
            if link not in all_link and link not in link_exceptions:
                all_link.append('https://www.soccer-rating.com'+link)

    # USING LINKS TO GET ELEMENT IN THAT TEAMS
    print('LENGHT OF ALL LINKS = ',len(all_link))
    # print(all_link)


    for i,x in enumerate(all_link):
        print('\n url = ',x)

        data = {'DATE': [],
                'LEAGUE': [],

                'HOME TEAM': [],
                'AWAY TEAM': [],

                'OPEN ODD': [],
                'AVAL ODD': [],
                'WINNER':[]
                }

        index_pos = i
        print(f'>>>>>>>>>>>>>>>>>>>>  NUMBER = {index_pos} HAS STARTED TO RUN, WITH TOTAL RUNS OF {len(all_link)}  & REMANING OF {len(all_link) - (index_pos+1)} <<<<<<<<<<<<<<<<<<<< \n')
        
        try:
            res = requests.get(x)
            soup = BeautifulSoup(res.content,'html.parser')
            main_sub = soup.find('td',width="33%")

            match_date = main_sub.text.split()[0]
            league = main_sub.text.split()[1]

            home_team = main_sub.find_next().find_next().text
            away_team = main_sub.find_next().find_next().find_next().text


            for x in main_sub.find_all_next(): 
                if 'Betting Tip:' in x.text:
                    x = x.text.replace('↓','').replace('↑','').replace('.','').split(' ')[-2]
                    print(x)
                    OO_rating = x.split('|')[0].strip()
                    AO_rating = x.split('|')[1].strip() 
                    print(OO_rating,AO_rating)           
                    break

            print(match_date,league,home_team,away_team,OO_rating,AO_rating)
            
            data['DATE'].append(match_date)
            data['LEAGUE'].append(league)

            data['HOME TEAM'].append(home_team)
            data['AWAY TEAM'].append(away_team)

            data['OPEN ODD'].append(OO_rating)
            data['AVAL ODD'].append(AO_rating)

            if OO_rating <0:
                data['WINNER'].append(home_team)
            else:
                data['WINNER'].append(away_team)

            saving_files(data=data,path=day_match_path)
        except Exception as e:
            print(f' \n {e} \n ')

    drop_similar(path=day_match_path,val1='HOME TEAM',val2='AWAY TEAM') 
    drop_duplicate(path=day_match_path)
get_day_games()