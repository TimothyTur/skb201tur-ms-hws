from steam.webapi import WebAPI
import numpy as np
from time import sleep # чтобы стим не считал обращения за дудос

# личный ключ, вставьте свой
key = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
# account_id, вставлен мой
accid = '256157023'

def get_dota2_to_triangular_destribution():
	api = WebAPI(key)
	
	match_h = []
	# потому что он выдает максимум 500 и по 100 на запрос
	# если сделать обращения за 500 матчей, он вернет только 500-ый
	for i in range(5):
	    if match_h == []:
	        match_h.append(api.IDOTA2Match_570.GetMatchHistory(
	            account_id = accid,
	            game_mode = 22,
	            min_players = '10',
	            matches_requested = '1000')) # бесполезно
	    else:
	        match_h.append(api.IDOTA2Match_570.GetMatchHistory(
	            account_id = accid,
	            game_mode = 22,
	            min_players = '10',
	            matches_requested = '1000',
	            start_at_match_id = \
	                str(match_h[-1]['result']['matches'][-1]['match_id'])))
	    sleep(0.7)
	match_h.append(api.IDOTA2Match_570.GetMatchHistory(
	    account_id = accid,
	    game_mode = 22,
	    min_players = '10',
	    matches_requested = '5',
	    start_at_match_id = \
	        str(match_h[-1]['result']['matches'][-1]['match_id'])))
	
	match_h_ids = [match_h[0]['result']['matches'][i]['match_id'] for i in range(100)] +\
	              [match_h[1]['result']['matches'][i]['match_id'] for i in range(100)] +\
	              [match_h[2]['result']['matches'][i]['match_id'] for i in range(100)] +\
	              [match_h[3]['result']['matches'][i]['match_id'] for i in range(100)] +\
	              [match_h[4]['result']['matches'][i]['match_id'] for i in range(100)] +\
	              [match_h[5]['result']['matches'][i]['match_id'] for i in range(5)]
	match_h_ids = np.unique(np.array(match_h_ids, dtype=np.int64))
	
	# достаем время
	match_h_time = np.zeros(500, dtype=np.int32)
	for i in range(0, 38):
	    match_h_time[i] = api.IDOTA2Match_570.GetMatchDetails(match_id=match_h_ids[i])['result']['duration']
	    sleep(1)
	
	mn = np.min(match_h_time)
	mx = np.max(match_h_time)
	result = (match_h_time-mn).astype('float64')/(mx-mn)
	
	np.savez('dota2_sample.npz', dota2_sample = result)

if __name__ == '__main__':
	get_dota2_to_triangular_destribution()
