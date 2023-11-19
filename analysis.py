import pandas as pd
import os
from statistics import mean 

def expected_score(opponent_ratings: list[float], own_rating: float) -> float:
    """How many points we expect to score in a tourney with these opponents"""
    return sum(
        1 / (1 + 10**((opponent_rating - own_rating) / 400))
        for opponent_rating in opponent_ratings
    )


def performance_rating(opponent_ratings: list[float], score: float) -> int:
    """Calculate mathematically perfect performance rating with binary search"""
    lo, hi = 0, 4000

    while hi - lo > 0.001:
        mid = (lo + hi) / 2

        if expected_score(opponent_ratings, mid) < score:
            lo = mid
        else:
            hi = mid

    return round(mid)





def perf_linear(opponent_ratings: list[float], score: float) -> int:
    if score < 0 or 2 * len(opponent_ratings) < score:
        return -1
    if len(opponent_ratings)==0:
        return -1
    return round(mean(opponent_ratings) + 8*((score/ len(opponent_ratings))*100 - 50));

def perf_fide(ratings: list[float], double_score: float) -> int:
    if double_score < 0 or 2 * len(ratings) < double_score:
        return -1
    if len(ratings)==0:
        return -1
    average=mean(ratings)
    dp = [0, 7, 14, 21, 29, 36, 43, 50, 57, 65, 72, 80, 87, 95, 102,
          110, 117, 125, 133, 141, 149, 158, 166, 175, 184, 193, 202,
          211, 220, 230, 240, 251, 262, 273, 284, 296, 309, 322, 336,
          351, 366, 383, 401, 422, 444, 470, 501, 538, 589, 677, 800]
    percentage = round(double_score / len(ratings)*100)
    if double_score < 0 or 2 * len(ratings) < double_score:
        return ""
    if percentage >= 50:
        return round(average + dp[percentage - 50])
    else:
        return round(average - dp[50 - percentage])


def scoretable(dataframe,p_round): # Генерирует таблицу на раунд
    table=dict.fromkeys(dataframe['player'].to_list(),None)
    for player in table:
        tmp=dataframe.loc[dataframe['player'] == player]
        tmp=tmp.loc[tmp['p_round'] <=p_round]
        table[player]=tmp['p_result'].sum()
    return(table)






ansfolder=r'C:\Users\user\Documents\chess' #папка для ответа
#ansfolde=r'/home/user/Documents/chess #linux
folder=r'C:\Users\user\Documents\chess\xlsx' #папка с исходными XLSX
#folder=r'/home/user/Documents/chess/XLSX #linux



turnList=os.listdir(folder)# получаем список файлов турниров


performanceTable=dict.fromkeys('Hikaru',{'OpponentRatings710':[],'points710':0,'OpponentRatings11prizes':[],'points11prizes':0,'OpponentRatings11noprizes':[],'points11noprizes':0})

    
for file in turnList:
    
    
    df=pd.read_excel(os.path.join(folder, file), index_col=0) # Считываем xmls файл в DataFrame
    round10table=scoretable(df,10)# Получаем таблизу 10 раунда с текущего турнира
    


        

    for player in round10table: # для каждого учасника турнира
    
        if player in performanceTable: # Добавляем в таблицу перформанса учаснока если его там нет
            pass
        else:
            performanceTable[player]={'OpponentRatings710':[],'points710':0,'OpponentRatings11prizes':[],'points11prizes':0,'OpponentRatings11noprizes':[],'points11noprizes':0}
            
        
        
        tmp=df.loc[df['player'] == player]# Получаем из DataFrame все партии текущего игрока
        tmp=tmp.loc[tmp['p_round'] >=7]# Из них выбираем только раунды 7-11
        
        round11=tmp.loc[tmp['p_round'] == 11]#тут раунд 11
        round710=tmp.loc[tmp['p_round'] < 11]#тут раунды 7-10
        
        
        #К добавляем к рейтингам оппонентов рейтинги опонентов из текущего турнира
        performanceTable[player]['OpponentRatings710']=performanceTable[player]['OpponentRatings710']+round710['p_ratingOpponent'].to_list()
        #К добавляем к общему счету счет из текущего турнира
        performanceTable[player]['points710']=performanceTable[player]['points710']+round710['p_result'].sum()
        
        if round10table[player] >= max(round10table.values())-1: #Условие призов в 10 туре отставать от первого место не более 1 очка
            performanceTable[player]['OpponentRatings11prizes']=performanceTable[player]['OpponentRatings11prizes']+round11['p_ratingOpponent'].to_list()
            performanceTable[player]['points11prizes']=performanceTable[player]['points11prizes']+round11['p_result'].sum()
        else:
            performanceTable[player]['OpponentRatings11noprizes']=performanceTable[player]['OpponentRatings11noprizes']+round11['p_ratingOpponent'].to_list()
            performanceTable[player]['points11noprizes']=performanceTable[player]['points11noprizes']+round11['p_result'].sum()
            


resultdf = pd.DataFrame({'player' : [],'Performance710' : [],'numgames710' : [],'performance11prizes' : [],'numgames11P' : [],'performance11moprizes' : [],'numgames11noP' : [],'delta':[]})

for player in performanceTable: 
    if len(performanceTable[player]['OpponentRatings710'])>10:
        if len(performanceTable[player]['OpponentRatings11prizes'])>10:
            #Вычисляем перформанс рейтинг для раундов 7-10
            a=perf_fide(performanceTable[player]['OpponentRatings710'], performanceTable[player]['points710'])
            #Вычисляем количество партий в раундах 7-10
            gamesa=len(performanceTable[player]['OpponentRatings710'])
            #Вычисляем перформанс рейтинг для раунда 11 с возможностью призов
            b=perf_fide(performanceTable[player]['OpponentRatings11prizes'], performanceTable[player]['points11prizes'])
            #Вычисляем количество партий в 11 раунде с возможностью призов
            gamesb=len(performanceTable[player]['OpponentRatings11prizes'])
            #Вычисляем перформанс рейтинг для раундов 1 без возможности призов
            c=perf_fide(performanceTable[player]['OpponentRatings11noprizes'], performanceTable[player]['points11noprizes'])
            #Вычисляем количество партий в 11 раунде без возможности призов
            gamesc=len(performanceTable[player]['OpponentRatings11noprizes'])
            #Вычисляем разницу между перформансом 7-10 раундов и перформансом для раунда 11 с возможностью призов
            delta=b-a
            
            list_row = [player,a,gamesa,b,gamesb,c,gamesc,delta]
            resultdf.loc[len(resultdf)] = list_row

with pd.ExcelWriter(os.path.join(ansfolder,'{}TTans.xlsx'.format(len(turnList))), engine='xlsxwriter') as writer:
    resultdf.to_excel(writer, sheet_name='data', index=False, startrow=0 , startcol=0)
    
    
        
        
    
    
    


        

    