import requests 
from bs4 import BeautifulSoup

main_url = 'http://www.cricinfo.com/ci/engine/match/1120151.html'

soup = BeautifulSoup(requests.get(main_url).content,'html.parser')

match_info = soup.find_all('div',{'class':'cscore_info-overview'})[0].text

match_notes = soup.find('div',{'class':'cscore_notes'}).span.text

def team_name(soup,i):		
	team = soup.find('a',{'aria-controls':'gp-inning-0'+i}).h2.text.replace(' Innings','')
	return team

def total_score(soup,i):
	total = soup.find('div',{'id':'gp-inning-0'+i}).find('div',{'class':'total'}).find_all('div')[1].text
	return total

def extras(soup,i):
	ext = soup.find('div',{'id':'gp-inning-0'+i}).find('div',{'class':'extras'}).find_all('div')[1].text
	return ext


def fow(soup,i):
	try:
		fall = soup.find('div',{'id':'gp-inning-0'+i}).find_all('div',{'class':'dnb'})[1].text
	except:
		fall = soup.find('div',{'id':'gp-inning-0'+i}).find_all('div',{'class':'dnb'})[0].text
	return fall


def format_fow(soup,i):
	fwtm = []
	try:
		fall = soup.find('div',{'id':'gp-inning-0'+i}).find_all('div',{'class':'dnb'})[1].text
	except:
		fall = soup.find('div',{'id':'gp-inning-0'+i}).find_all('div',{'class':'dnb'})[0].text 
	text =  fall.replace('Fall of wickets: ','').split(',')
	for i in range(0,len(text),2):
		text[i] = text[i] + text[i+1]
	del text[1::2]
	for t in text:
		fw = {'runs':t.split('(')[0].split('-')[1],'namov':t.split('(')[1].replace(')','')}
		fwtm.append(fw)	
	return fwtm

def format_bat_stat(soup,i):
	bat_db = []
	bat_list = batsmen = soup.find('div',{'id':'gp-inning-0'+i}).find_all('div',{'class':'wrap batsmen'})
	for single_bat in bat_list:
		bat_data = {
					'name' : single_bat.find('div',{'class':'cell batsmen'}).a.text,
					'status' : single_bat.find('div',{'class':'commentary'}).text.replace('c ','catch by ').replace('b ','bowler '),
					'runs' : single_bat.find_all('div',{'class':'runs'})[0].text,
					'balls' : single_bat.find_all('div',{'class':'runs'})[2].text,
					'4s' : single_bat.find_all('div',{'class':'runs'})[3].text,
					'6s' : single_bat.find_all('div',{'class':'runs'})[4].text
					}
		bat_db.append(bat_data)
	return bat_db

def format_bowl_stat(soup,i):
	bw_db = []
	bowling = soup.find('div',{'id':'gp-inning-0'+i}).find('div',{'class':'bowling'}).table.find_all('tr')[1:]
	for bw in bowling:
		bw_td = bw.find_all('td')
		bw_dt = {
				 'name': bw_td[0].a.text,
				 'ov': bw_td[2].text,
				 'mai': bw_td[3].text,
				 'runs': bw_td[4].text,
				 'wicket': bw_td[5].text,
				 'econ': bw_td[6].text,
				 'wd':bw_td[7].text,
				 'no':bw_td[8].text,
				} 
		bw_db.append(bw_dt)
	return bw_db
	


team_name_1 = team_name(soup,'0')
team_name_2 = team_name(soup,'1')

total_1 = total_score(soup,'0')
total_2 = total_score(soup,'1')

extra_1 = extras(soup,'0')
extra_2 = extras(soup,'1')

form_fow_1 = format_fow(soup,'0')
form_fow_2 = format_fow(soup,'1')

form_bat_1 = format_bat_stat(soup,'0')
form_bat_2 = format_bat_stat(soup,'1')

form_bowl_1 = format_bowl_stat(soup,'0')
form_bowl_2 = format_bowl_stat(soup,'1')


print(match_info,'\n')
print(team_name_1+' vs '+team_name_2,'\n')


print(team_name_1+' inning\n')
print('Total Score: ',total_1)
print('Extras: ',extra_1,'\n')
print('Batting')
for bat in form_bat_1:
	print(bat['name']+' runs: '+bat['runs']+' in '+bat['balls']+' balls'+' 4s: '+bat['4s']+' 6s: '+bat['6s']+' '+bat['status'])
print('\n')
print('Bowling')
for bwl in form_bowl_1:
	print(bwl['name']+' overs: '+bwl['ov']+' runs: '+bwl['runs']+' wickets: '+bwl['wicket']+' maiden: '+bwl['mai']+' wide: '+bwl['wd']+'  balls: '+bwl['no']+' economy: '+bwl['econ'])
print('\n')
print('Fall of Wickets')
for fow in form_fow_1:
	print(fow['namov']+' at '+fow['runs']+' runs')
print('\n')


print(team_name_2+' inning\n')
print('Total Score: ',total_2)
print('Extras: ',extra_2,'\n')
print('Batting')
for bat in form_bat_2:
	print(bat['name']+' runs: '+bat['runs']+' in '+bat['balls']+' balls '+' 4s: '+bat['4s']+' 6s: '+bat['6s']+' '+bat['status'])
print('\n')
print('Bowling')
for bwl in form_bowl_2:
	print(bwl['name']+' overs: '+bwl['ov']+' runs: '+bwl['runs']+' wickets: '+bwl['wicket']+' maiden: '+bwl['mai']+' wide: '+bwl['wd']+' no balls: '+bwl['no']+' economy: '+bwl['econ'])
print('\n')
print('Fall of Wickets')
for fow in form_fow_2:
	print(fow['namov']+' at '+fow['runs']+' runs')
print('\n')
print(match_notes,'\n')
