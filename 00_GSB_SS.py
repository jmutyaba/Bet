import os
import sys
import json
import cloudpickle
import requests
import requests_cache
from pprint import pprint
from requests.exceptions import ProxyError
from requests.exceptions import ConnectionError
import itertools
import calendar
import time
import pandas as pd
import dataframe_image as dfi
from random import randint
from collections import namedtuple, OrderedDict
from operator import attrgetter
from collections import namedtuple
from datetime import datetime, timedelta
from matplotlib import pyplot as plt
import matplotlib.dates as mdates
import warnings
import streamlit as st
from fuzzywuzzy import fuzz
import codecs


if sys.platform.startswith('win'):
    from scraper_api import proxies
    import winsound
warnings.filterwarnings('ignore')

start_time = datetime.now()

pd.set_option('display.expand_frame_repr', False)
pd.set_option("display.max_rows", None, "display.max_columns", None)

# if sys.platform.startswith('lin'):
#     requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = "TLS13-CHACHA20-POLY1305-SHA256:TLS13-AES-128-GCM-SHA256" \
#                                                           ":TLS13-AES-256-GCM-SHA384:ECDHE:!COMPLEMENTOFDEFAULT "


def println(my_list=(), enum=False):
    """
    :type my_list: []
    :type enum: bool
    """
    print("Printing List")
    if enum is True:
        for i, item in enumerate(my_list):
            try:
                print(i, '\t', item)
            except UnicodeError:
                pass
    else:
        for item in my_list:
            print(item)


def headers(head):
    if sys.platform.startswith('win'):
        header_ = {'headers_sofa': {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 '
                                                  '(KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'},
                   'headers_pawa': {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 '
                                                  '(KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
                                    'Referer': 'https://www.betpawa.ug/upcoming'}}
    else:
        header_ = {'headers_sofa': {'User-Agent': 'Mozilla/5.0 (Linux; U; Android 4.0; en-us; GT-I9300 Build/IMM76D) '
                                                  'AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30'},
                   'headers_pawa': {'User-Agent': 'Mozilla/5.0 (Linux; U; Android 4.0; en-us; GT-I9300 Build/IMM76D) '
                                                  'AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
                                    'Referer': 'https://www.betpawa.ug/upcoming'}}
    return header_.get(head)


def proxy_request(url, header):
    return requests.get(url, proxies=proxies, headers=headers(header), verify=False)


def direct_request(url, header):
    time.sleep(randint(0, 1))
    try:
        resp = requests.get(url, headers=headers(header))
    except (ProxyError, ConnectionError):
        print('First Try Failed', url)
        time.sleep(10)
        try:
            resp = requests.get(url, headers=headers(header))
        except (ProxyError, ConnectionError):
            print('Second Try Failed', url)
            time.sleep(20)
            try:
                resp = requests.get(url, headers=headers(header))
            except (ProxyError, ConnectionError):
                print('Third Try Failed', url)
                time.sleep(30)
                try:
                    resp = requests.get(url, headers=headers(header))
                except (ProxyError, ConnectionError):
                    print('Fourth Try Failed', url)
                    time.sleep(60)
                    resp = requests.get(url, headers=headers(header))
    return resp


def direct_request_(url, header):
    resp = ''
    for i in range(1, 6):
        try:
            resp = requests.get(url, headers=headers(header))
            break
        except (ProxyError, ConnectionError):
            print('{} Try Failed'.format(i))
            time.sleep(10 * (i + 1))
    return resp


gsb_session = requests_cache.CachedSession('gsb_cache')
sofa_session = requests_cache.CachedSession('sofa_cache')


def session_request(url, site_session, header):
    resp = ''
    for i in range(1, 6):
        try:
            resp = site_session.get(url, headers=headers(header))
            break
        except (ProxyError, ConnectionError):
            print(f'Request Failed {i} times' if not i ==
                  1 else f'Request Failed {i} time')
            time.sleep(10 * (i + 1))
    return resp


# def combined_request(selector=0):
#     if selector == 0:

def files(my_file='', folder=''):
    bp_lin = r"/storage/emulated/0/qpython/scripts3/"
    # bp_win = os.path.dirname(os.path.abspath(__file__))
    bp_win = 'C:\Users\Administrator\BetFiles'

    my_file = my_file.replace('/', '')
    return os.path.join(bp_win,
                        folder,
                        my_file) if sys.platform.lower().startswith('win') else os.path.join(bp_lin, folder, my_file)
    # path = os.path.join(bp_win,
    #                     folder,
    #                     my_file) if sys.platform.lower().startswith('win') else os.path.join(bp_lin, folder, my_file)
    # if not os.path.exists(path):
    #     with open(path, 'w+') as f:
    #         pass
    # return path


with open(files('log.txt'), 'w', encoding='utf-8') as logger:
    logger.write('Start\n')

with open(files('logger.txt'), 'w', encoding='utf-8') as logger:
    logger.write('Start\n')


def log(log_item, enum=False):
    with open(files('log.txt'), 'a', encoding='utf-8') as logger:
        # logger.write('\n\n')  # + log_item.__name__)
        # print(type(log_item))
        if type(log_item) is str:
            logger.write(log_item + '\n')
        elif type(log_item) is list and enum is True:
            for i, row in enumerate(log_item):
                logger.write(str(i) + str(row) + '\n')
        elif type(log_item) is list and enum is False:
            for row in log_item:
                logger.write(str(row) + '\n')


def logger(log_item, enum=False):
    with open(files('logger.txt'), 'a', encoding='utf-8') as logger:
        # logger.write('\n\n')  # + log_item.__name__)
        # print(type(log_item))
        if type(log_item) is str:
            logger.write(log_item + '\n')
        elif type(log_item) is list and enum is True:
            for i, row in enumerate(log_item):
                logger.write(str(i) + str(row) + '\n')
        elif type(log_item) is list and enum is False:
            for row in log_item:
                logger.write(str(row) + '\n')


def clear():
    # folder_list = ['BetPawa_Json', 'Fixtures', 'SofaScore_Json']
    folder_list = ['BetPawa_Json', 'SofaScore_Json', 'SofaScore_Json', 'PNGS']
    for fld in folder_list:
        base_folder = files(folder=fld)
        for root, folders, fileNames in os.walk(base_folder):
            for fileName in fileNames:
                if fileName.endswith(('.json', '.sqlite', '.png')):
                    full_path = os.path.join(root, fileName)
                    print('Deleting ' + full_path)
                    log('Deleting ' + full_path)
                    os.remove(full_path)
    for file_name in ['05 Gal Events.txt', '06 Matched.txt', 'gsb.json']:
        with open(r'' + file_name, 'wb') as f:
            # print(f.readlines())
            pass
    for cache_filename in ('sofa_cache.sqlite', 'gsb_cache.sqlite'):
        cache_path = os.path.join(os.path.split(os.path.abspath(
            os.path.dirname(__file__)))[0], cache_filename)
        print('Deleting ' + cache_path)
        log('Deleting ' + cache_path)
    pass


def std_date_time_format():
    return '%Y-%m-%d %H%M%S'


def std_date_time_format_dotted():
    return '%Y-%m-%d %H:%M:%S'


def std_date_format():
    return '%Y-%m-%d'


def z_date_time_format():
    return '%Y-%m-%dT%H:%M:%SZ'


def datetime_z2std(z_time: str):
    return (datetime.strptime(z_time, z_date_time_format()) + timedelta(hours=3)).strftime(std_date_time_format())


def printseperator():
    print('-' * 100 + '\n' + '-' * 100)


def all_gsb_events_request():
    url = 'https://gsb.ug/Services/onlineapi/Event/GetEvents?bettypeids=-1'
    data = requests.get(url)
    gsb_json = files('gsb.json')
    with open(gsb_json, 'w') as out_file:
        json.dump(data.json(), out_file, indent=4)
    return data.json()


def gal():
    gal = namedtuple('gal', 'timeStamp, eventId, leagueId, homeTeam, awayTeam')
    my_file = all_gsb_events_request()
    events = [gal(timeStamp=datetime_z2std(event['data']['time']),
                  eventId=event['data']['id'],
                  leagueId=event['data']['leagueId'],
                  homeTeam=event['data']['home'],
                  awayTeam=event['data']['away'])
              for event in my_file['events'] if event['data']['sportName'] == 'Soccer']
    events = sorted(events, key=attrgetter('timeStamp'))
    println(events, enum=True)
    cloudpickle.dump(events, open(files('05 Gal Events.txt'), 'wb'))


def gal_odds(event_id):
    # TODO: Introduce Ordered Dict Here
    with open(files('gsb.json'), 'r') as in_file:
        my_data = json.load(in_file)
        for event in my_data['events']:
            if event['data']['sportName'] == 'Soccer' and event['data']['id'] == event_id:
                for item in event['bts']:
                    my_dict = {item['data']['name']: {}}
                    # OrderedDict([('one', 1), ('two', 2), ('three', 3)])
                    for elem in item['odds']:
                        my_dict[item['data']['name']][elem['name']] = (
                            elem['shortcut'], elem['price'])
                    print(my_dict)
                print('')


def sofa_score(date_query, save_file):
    # timestamp = calendar.timegm(time.gmtime())
    # url = 'https://www.sofascore.com/football//' + date_query + '/json?_=' + str(timestamp)
    url = 'https://api.sofascore.com/api/v1/sport/football/scheduled-events/' + date_query
    print(url)
    with open(save_file, "w") as outfile:
        response = session_request(url, sofa_session, 'headers_sofa')
        print(response)
        json.dump(response.json(), outfile, indent=4)


def sofa_score_teams(query_date, read_file, write_file):
    sofa = namedtuple(
        'sofa', 'timeStamp, customId, eventId, homeTeamId, awayTeamId, homeTeam, awayTeam, slug')
    test1 = query_date + ' 000000'
    test2 = (datetime.strptime(query_date, std_date_format()) + timedelta(days=1)).strftime(
        std_date_format()) + ' 000000'
    with open(read_file, "r") as infile:
        my_json = json.load(infile)
        # final = (event for tournament in my_json["events"])
        # final = (event for tournament in my_json["sportItem"]["tournaments"] for event in tournament['events'])
        data = (sofa(timeStamp=datetime.fromtimestamp(event["startTimestamp"]).strftime(std_date_time_format()),
                     customId=event["customId"],
                     eventId=event['id'],
                     homeTeamId=event["homeTeam"]['id'],
                     awayTeamId=event["awayTeam"]['id'],
                     homeTeam=event["homeTeam"]['name'],
                     awayTeam=event["awayTeam"]['name'],
                     slug=event["slug"],
                     ) for event in my_json['events'])
        data = (
            event for event in data if 'SRL' not in event.homeTeam or 'SRL' not in event.awayTeam)
        data = [event for event in data if test1 <= event.timeStamp <= test2]
        with open(write_file, 'wb') as d:
            cloudpickle.dump(sorted(data), d)


def date_maker(offset=0):
    return (datetime.today() + timedelta(days=offset)).strftime(std_date_format())


def sofa_score_multiple_query(query, offset=5):
    for i in range(0, offset):
        query_date = date_maker(i)
        print(query_date, ' Parsing Json')
        read_file = files(query_date + ' SofaScore.json', folder='Fixtures')
        write_file = files(
            query_date + ' SofaScoreCleaned.txt', folder='Fixtures')
        if query:
            sofa_score(query_date, read_file)
            sofa_score_teams(query_date, read_file, write_file)

    combined = []
    for i in range(0, offset):
        query_date = date_maker(i)
        read_file = files(
            query_date + ' SofaScoreCleaned.txt', folder='Fixtures')
        with open(read_file, 'rb') as d:
            combined += cloudpickle.load(d)
    println(combined, enum=True)
    with open(files('03 SofaScore Events.txt'), 'wb') as r:
        cloudpickle.dump(combined, r)


def combine(start_off=0, off=1):
    # bp = cloudpickle.load(open(files('02 BetPawa_events.txt'), 'rb'))
    gal = cloudpickle.load(open(files('05 Gal Events.txt'), 'rb'))
    sf = cloudpickle.load(open(files('03 SofaScore Events.txt'), 'rb'))
    x = 0
    in_20_min = (datetime.now() + timedelta(minutes=20)
                 ).strftime(std_date_time_format())
    combination_start, combination_offset = date_maker(
        offset=start_off), date_maker(offset=off)
    matched_items, matched, harmonize = [], [], {}
    for g in gal:
        if g.homeTeam == 'Hungary' and g.awayTeam == 'England':
            continue
        for s in sf:
            if g.timeStamp == s.timeStamp \
                    and fuzz.token_set_ratio(g.homeTeam + ' - ' + g.awayTeam, s.homeTeam + ' - ' + s.awayTeam) >= 65 \
                    and g.timeStamp >= in_20_min and combination_start <= g.timeStamp < combination_offset:
                # print(str(x), b, s, sep='\t')
                # harmonize[b.teamNames] = (s.homeTeamId, s.homeTeam, s.awayTeamId, s.awayTeam)
                matched_items.append(g)
                matched.append((g, s))
                x += 1
    unmatched = [item for item in gal if item not in matched_items]
    # print('\nUnmatched')
    # println(unmatched)
    log(unmatched, enum=True)
    # TODO: Come up with a Better Output here
    # print('\nHarmonized List')
    # println(harmonize.items())
    with open(files('06 Matched.txt'), 'wb') as d:
        cloudpickle.dump(matched, d)


def get_gsb_sf_events(min_matches=3, under=1.5, over=2.5, min_xh_wins=20, mm=10):
    with open(files('06 Matched.txt'), 'rb') as d:
        data = cloudpickle.load(d)
        # print(data)
        for gsb, sf in data:
            # print(sf, gsb)
            get_sf_event_bets(sf)
            qualify1 = parse_sf_event_bets(
                sf, min_matches=min_matches, under=under, over=over, no_of_months=mm)
            qualify2 = get_past_winners(sf, gsb, no_of_months=mm)
            # TODO: Qualify
            # get_standing_table(sf)
            if qualify1 or qualify2:
                # print(sf)
                # print(bp)
                print('____________________________________________')
                print(sf.homeTeamId)
                print(sf.awayTeamId)
                save_folder_ = f'U{under} O{over}'
                check = double_team_history(sf, save_folder_, int(sf.homeTeamId), int(
                    sf.awayTeamId), min_wins=min_xh_wins, )
                # if check:
                print(1 * '\n')
                print('____________________________________________')
                print('\n###', gsb.timeStamp, sf.homeTeam, sf.awayTeam, sep='\t')
                print('In', (datetime.strptime(gsb.timeStamp,
                      std_date_time_format()) - datetime.now()).days, 'days')
                print('https://www.gsb.ug/event/' + str(gsb.eventId))
                print('https://www.sofascore.com/' +
                      sf.slug + '/' + sf.customId)
                print(gsb)
                gal_odds(gsb.eventId)
                # TODO: Switch this function
                print(1 * '\n')
                print('____________________________________________')
                # TODO: add here


def get_gsb_event_bets(gsb):
    url = 'https://www.betpawa.ug/events/ws/getPricesForEvent/' + \
        str(gsb.eventId)
    file_name = gsb.timeStamp + ' ' + gsb.teamNames + '.json'
    file_path = files(file_name, folder='BetPawa_Json')
    # TODO: Dump to file only if it doesn't exist or if its empty
    if not os.path.exists(file_path):
        response = direct_request(url, 'headers_pawa')
        with open(file_path, 'w') as f:
            json.dump(response.json(), f, indent=4)
        json_data = response.json()
        # println(json_data["Data"]["Markets"])
    my_data = gsb()
    for event in my_data['events'][:2]:
        if event['data']['sportName'] == 'Soccer':
            for item in event['bts']:
                print(item)
                my_dict = {item['data']['name']: {}}
                for elem in item['odds']:
                    my_dict[item['data']['name']][elem['name']] = (
                        elem['shortcut'], elem['price'])
                print(my_dict)
                print(pd.DataFrame(my_dict))
            print('')


def get_sf_event_bets(sf):
    url = 'https://api.sofascore.com/api/v1/event/' + \
        str(sf.customId) + '/h2h/events'
    # print(url)
    file_title = sf.timeStamp + ' ' + sf.slug + '.json'
    file_path = files(file_title, folder='SofaScore_Json')
    if not os.path.exists(file_path):
        response = session_request(url, sofa_session, 'headers_sofa')
        with open(file_path, 'w') as f:
            json.dump(response.json(), f, indent=4)
        json_data = response.json()
        # println(json_data)


def parse_sf_event_bets(sf, min_matches=3, under=1.5, over=2.5, no_of_months=10):
    file_name = sf.timeStamp + ' ' + sf.slug + '.json'
    print(sf)
    sofa = namedtuple('sofa',
                      'timeStamp, homeTeam, hG1h, tG1h, aG1h, hG2h, tG2h, aG2h, homeScore, totalScore, awayScore, '
                      'awayTeam, BTTS, winnerCode')
    with open(files(file_name, folder='SofaScore_Json'), 'r') as f:
        json_data = json.load(f)
        try:
            json_data['events']
            proceed = True
        except KeyError:
            proceed = final = False
        if proceed:
            events = [sofa(timeStamp=datetime.fromtimestamp(event['startTimestamp']).strftime(std_date_time_format()),
                           homeTeam=event['homeTeam']['name'],
                           awayTeam=event['awayTeam']['name'],
                           homeScore=event.get('homeScore').get(
                               'normaltime', 0),
                           hG1h=event.get('homeScore').get("period1"),
                           awayScore=event.get('awayScore').get(
                               'normaltime', 0),
                           aG1h=event.get('awayScore').get("period1"),
                           totalScore=event.get('homeScore').get('normaltime', 0) +
                           event.get('awayScore').get('normaltime', 0),
                           tG1h=event.get('homeScore').get(
                               'period1', 0) + event.get('awayScore').get('period1', 0),
                           hG2h=event.get('homeScore').get(
                               'normaltime', 0) - event.get('homeScore').get("period1", 0),
                           aG2h=event.get('awayScore').get(
                               'normaltime', 0) - event.get('awayScore').get("period1", 0),
                           tG2h=event.get('homeScore').get('normaltime', 0) - event.get('homeScore').get("period1", 0) +
                           event.get('awayScore').get('normaltime', 0) -
                           event.get('awayScore').get("period1", 0),
                           BTTS='BTTS-Yes' if event.get('homeScore').get('normaltime', 0) > 0 and event.get(
                               'awayScore').get('normaltime', 0) > 0 else 'BTTS -No',
                           winnerCode=event['homeTeam']['name'] + ' at Home' if event.get("winnerCode", 3) == 1 else event['awayTeam']['name'] + ' at Away' if event.get("winnerCode", 3) == 2 else 'Draw at Home of ' + event['homeTeam']['name']) for event in json_data['events'] if event['status']['type'] == "finished"]

            two_years_ago = (datetime.today() - timedelta(days=(365 + 1))
                             ).strftime(std_date_time_format())
            few_months_ago = (datetime.today(
            ) - timedelta(days=(30 * no_of_months))).strftime(std_date_time_format())

            events1 = [
                event for event in events if event.timeStamp >= two_years_ago]
            events2 = [
                event for event in events if event.timeStamp < two_years_ago]
            # print(events1)
            try:
                last_match_time = events1[0].timeStamp >= few_months_ago
            except IndexError:
                last_match_time = False
            # println(events1)
            over_ = [event.totalScore for event in events1]
            under_ = [event.totalScore for event in events1]
            over_1h = [event.tG1h for event in events1]
            under_1h = [event.tG1h for event in events1]

            if not over_ == [] and len(over_) >= min_matches and (int(max(under_)) < under or int(min(over_)) > over) and last_match_time:
                print('____________________________________________')
                print('____________________________________________')
                print(sf.timeStamp, '\t', sf.homeTeam, '\t', sf.awayTeam)
                total_score = '*****  Under ' + str(under) + '  *****' if int(
                    max(under_)) < under else '*****  Over ' + str(over) + '  *****'
                total_score_log = 'Under ' + \
                    str(under) if int(max(under_)) < under else'Over ' + str(over)
                save_folder = f'U{under} O{over}'
                # h_line = under if int(max(under_)) < under else over
                print(total_score)
                log(total_score)
                logger(
                    f'{sf.timeStamp}\t{sf.homeTeam}\t{sf.awayTeam}\t{total_score_log}')
                for line in events1:
                    print(line.homeScore, line.awayScore,
                          line.totalScore, line.winnerCode)
                    log('\t'.join([str(line.homeScore), str(line.awayScore), str(
                        line.totalScore), str(line.winnerCode)]))
                out_frame = pd.DataFrame(events1)
                out_frame_ = pd.DataFrame(events2[:10])
                all_events_frame = pd.DataFrame(
                    events[:(len(events1) + len(events2[:10]))])

                plotter(sf, all_events_frame, total_score_log, mdates.YearLocator(), save_folder, 'all')
                plotter(sf, out_frame, total_score_log, mdates.MonthLocator(), save_folder, 'form')
                plotter1h(sf, all_events_frame, total_score_log, mdates.YearLocator(), save_folder, '1h')
                plotter_home(sf, all_events_frame, total_score_log, mdates.YearLocator(), save_folder, 'home')
                plotter_away(sf, all_events_frame, total_score_log, mdates.YearLocator(), save_folder, 'jaway')

                # fileName1, sub1 = plotter(plt.subplots(figsize=(12, 8)), sf, all_events_frame, total_score_log, mdates.YearLocator(), 'all')
                # fileName2, sub2 = plotter(plt.subplots(figsize=(6, 8)), sf, out_frame, total_score_log, mdates.MonthLocator(), 'form')
                # plt.savefig(fileName1)

                # TODO: Modify Dataframe for plotting

                try:
                    out_frame1 = out_frame.drop(
                        ['homeScore', 'totalScore', 'awayScore'], axis=1)
                    print("First Half")
                    print(out_frame1)
                    dfi.export(out_frame1, files(f'{sf.timeStamp} {sf.homeTeam} {sf.awayTeam} 1H.png', f'PNGS\{save_folder}'))
                    printseperator()
                except (KeyError, UnicodeEncodeError):
                    pass
                try:
                    out_frame2 = out_frame_.drop(
                        ['homeScore', 'totalScore', 'awayScore'], axis=1)
                    print(out_frame2)
                    dfi.export(out_frame2, files(f'{sf.timeStamp} {sf.homeTeam} {sf.awayTeam} 1X2.png', f'PNGS\{save_folder}'))
                    printseperator()
                except (KeyError, UnicodeEncodeError):
                    pass

                print(pd.DataFrame(events1))
                log(pd.DataFrame(events1))
                print(out_frame_)
                final = True
            else:
                final = False
    return final


def plotter(sf, frame, boundary_condition, mdates_locator, save_me, file_id):
    pf = frame.copy()
    # print('Plotting df')
    # print(pf.head())
    pf['homePlot'] = [hS if hT == sf.homeTeam else aS for hS, aS, hT, aT in zip(
        pf['homeScore'], pf['awayScore'], pf['homeTeam'], pf['awayTeam'])]
    pf['awayPlot'] = [aS if aT == sf.awayTeam else hS for hS, aS, hT, aT in zip(
        pf['homeScore'], pf['awayScore'], pf['homeTeam'], pf['awayTeam'])]

    pf['homePlot1h'] = [hG1h if hT == sf.homeTeam else aG1h for hG1h, aG1h,
                        hT, aT in zip(pf['hG1h'], pf['aG1h'], pf['homeTeam'], pf['awayTeam'])]
    pf['awayPlot1h'] = [aG1h if aT == sf.awayTeam else hG1h for hG1h, aG1h,
                        hT, aT in zip(pf['hG1h'], pf['aG1h'], pf['homeTeam'], pf['awayTeam'])]

    pf['timeStamp'] = [datetime.strptime(
        tStamp[:10], std_date_format()) for tStamp in pf['timeStamp']]
    fig, ax = plt.subplots(figsize=(12, 8))
    # fig, ax = subplots
    ax.set_ylim(bottom=0, top=10)

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y/%m'))
    plt.gca().xaxis.set_major_locator(mdates_locator)
    plt.plot(pf["timeStamp"], pf["totalScore"])
    plt.gcf().autofmt_xdate()

    # plt.axhline(y=h_line, color='r', linestyle='-')
    plt.axhline(y=2.5, color='r', linestyle='-')
    plt.axhline(y=1.5, color='r', linestyle='-')
    plt.axhline(y=3.5, color='r', linestyle='-')
    for i, label in enumerate(pf["timeStamp"]):
        ax.annotate(text=f'{pf["homeTeam"][i]} - {pf["awayTeam"][i]}\n{pf["homeScore"][i]} - {pf["awayScore"][i]}',
                    xy=(pf["timeStamp"][i], pf["totalScore"][i]), ha='center', rotation=90)

    plt.xticks(rotation=22.5)
    plt.grid(visible=True, which='both', axis='both')
    plt.title(
        label=f'{sf.timeStamp} : {sf.homeTeam} -- {sf.awayTeam}', loc='center')

    plt.plot(pf["timeStamp"], pf["homePlot"], color='g')
    plt.plot(pf["timeStamp"], pf["awayPlot"], color='y')

    plt.plot(pf["timeStamp"], pf["homePlot1h"], color='black', linestyle='dashed')
    plt.plot(pf["timeStamp"], pf["awayPlot1h"], color='m', linestyle='dashed')

    # plt.show()
    plt.savefig(files(
        f'{sf.timeStamp} {sf.homeTeam} {sf.awayTeam} {boundary_condition} {file_id}.png', f'PNGS\{save_me}'))
    # return files(f'{sf.timeStamp} {sf.homeTeam} {sf.awayTeam} {boundary_condition} {file_id}.png', 'PNGS'), plt
    # TODO: implement streamlit output and plotting


def plotter1h(sf, frame, boundary_condition, mdates_locator, save_me, file_id):
    pf = frame.copy()
    # print('Plotting df')
    # print(pf.head())

    pf['homePlot1h'] = [hG1h if hT == sf.homeTeam else aG1h for hG1h, aG1h,
                        hT, aT in zip(pf['hG1h'], pf['aG1h'], pf['homeTeam'], pf['awayTeam'])]
    pf['awayPlot1h'] = [aG1h if aT == sf.awayTeam else hG1h for hG1h, aG1h,
                        hT, aT in zip(pf['hG1h'], pf['aG1h'], pf['homeTeam'], pf['awayTeam'])]
    pf['totalPlot1h'] = pf['homePlot1h'] + pf['awayPlot1h']
    pf['timeStamp'] = [datetime.strptime(
        tStamp[:10], std_date_format()) for tStamp in pf['timeStamp']]
    fig, ax = plt.subplots(figsize=(12, 8))
    # fig, ax = subplots
    ax.set_ylim(bottom=0, top=10)

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y/%m'))
    plt.gca().xaxis.set_major_locator(mdates_locator)
    plt.plot(pf["timeStamp"], pf["totalPlot1h"])
    plt.gcf().autofmt_xdate()

    # plt.axhline(y=h_line, color='r', linestyle='-')
    plt.axhline(y=2.5, color='r', linestyle='-')
    plt.axhline(y=1.5, color='r', linestyle='-')
    plt.axhline(y=0.5, color='r', linestyle='-')
    plt.axhline(y=3.5, color='r', linestyle='-')
    for i, label in enumerate(pf["timeStamp"]):
        ax.annotate(text=f'{pf["homeTeam"][i]} - {pf["awayTeam"][i]}\n{pf["homePlot1h"][i]} - {pf["awayPlot1h"][i]}',
                    xy=(pf["timeStamp"][i], pf["totalPlot1h"][i]), ha='center', rotation=90)

    plt.xticks(rotation=22.5)
    plt.grid(visible=True, which='both', axis='both')
    plt.title(
        label=f'{sf.timeStamp} : {sf.homeTeam} -- {sf.awayTeam}', loc='center')
    plt.plot(pf["timeStamp"], pf["totalPlot1h"], color='green', linestyle='-')
    plt.plot(pf["timeStamp"], pf["homePlot1h"], color='black', linestyle='dashed')
    plt.plot(pf["timeStamp"], pf["awayPlot1h"], color='m', linestyle='dashed')

    # plt.show()
    plt.savefig(files(
        f'{sf.timeStamp} {sf.homeTeam} {sf.awayTeam} {boundary_condition} {file_id}.png', f'PNGS\{save_me}'))
    # return files(f'{sf.timeStamp} {sf.homeTeam} {sf.awayTeam} {boundary_condition} {file_id}.png', 'PNGS'), plt
    # TODO: implement streamlit output and plotting


def plotter_home(sf, frame, boundary_condition, mdates_locator, save_me, file_id):
    pf = frame.copy()
    pf = pf[pf['homeTeam'] == sf.homeTeam]
    pf.reset_index(drop=True, inplace=True)
    pf['timeStamp'] = [datetime.strptime(
        tStamp[:10], std_date_format()) for tStamp in pf['timeStamp']]
    fig, ax = plt.subplots(figsize=(12, 8))
    # fig, ax = subplots
    ax.set_ylim(bottom=0, top=10)

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y/%m'))
    plt.gca().xaxis.set_major_locator(mdates_locator)
    plt.plot(pf["timeStamp"], pf["totalScore"])
    plt.gcf().autofmt_xdate()

    # plt.axhline(y=h_line, color='r', linestyle='-')
    plt.axhline(y=2.5, color='r', linestyle='-')
    plt.axhline(y=1.5, color='r', linestyle='-')
    plt.axhline(y=3.5, color='r', linestyle='-')
    for i, label in enumerate(pf["timeStamp"]):
        ax.annotate(text=f'{pf["homeTeam"][i]} - {pf["awayTeam"][i]}\n{pf["homeScore"][i]} - {pf["awayScore"][i]}',
                    xy=(pf["timeStamp"][i], pf["totalScore"][i]), ha='center', rotation=90)

    plt.xticks(rotation=22.5)
    plt.grid(visible=True, which='both', axis='both')
    plt.title(
        label=f'{sf.timeStamp} : {sf.homeTeam} -- {sf.awayTeam}', loc='center')
    # plt.show()
    plt.savefig(files(
        f'{sf.timeStamp} {sf.homeTeam} {sf.awayTeam} {boundary_condition} {file_id}.png', f'PNGS\{save_me}'))
    # return files(f'{sf.timeStamp} {sf.homeTeam} {sf.awayTeam} {boundary_condition} {file_id}.png', 'PNGS'), plt
    # TODO: implement streamlit output and plotting


def plotter_away(sf, frame, boundary_condition, mdates_locator, save_me, file_id):
    pf = frame.copy()
    pf = pf[pf['homeTeam'] == sf.awayTeam]
    pf.reset_index(drop=True, inplace=True)
    pf['timeStamp'] = [datetime.strptime(
        tStamp[:10], std_date_format()) for tStamp in pf['timeStamp']]
    fig, ax = plt.subplots(figsize=(12, 8))
    # fig, ax = subplots
    ax.set_ylim(bottom=0, top=10)

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y/%m'))
    plt.gca().xaxis.set_major_locator(mdates_locator)
    plt.plot(pf["timeStamp"], pf["totalScore"])
    plt.gcf().autofmt_xdate()

    # plt.axhline(y=h_line, color='r', linestyle='-')
    plt.axhline(y=2.5, color='r', linestyle='-')
    plt.axhline(y=1.5, color='r', linestyle='-')
    plt.axhline(y=3.5, color='r', linestyle='-')
    for i, label in enumerate(pf["timeStamp"]):
        ax.annotate(text=f'{pf["homeTeam"][i]} - {pf["awayTeam"][i]}\n{pf["homeScore"][i]} - {pf["awayScore"][i]}',
                    xy=(pf["timeStamp"][i], pf["totalScore"][i]), ha='center', rotation=90)

    plt.xticks(rotation=22.5)
    plt.grid(visible=True, which='both', axis='both')
    plt.title(
        label=f'{sf.timeStamp} : {sf.homeTeam} -- {sf.awayTeam}', loc='center')
    # plt.show()
    plt.savefig(files(
        f'{sf.timeStamp} {sf.homeTeam} {sf.awayTeam} {boundary_condition} {file_id}.png', f'PNGS\{save_me}'))
    # return files(f'{sf.timeStamp} {sf.homeTeam} {sf.awayTeam} {boundary_condition} {file_id}.png', 'PNGS'), plt
    # TODO: implement streamlit output and plotting


def get_pair_json(sf):
    # print(sf)
    # url = 'https://www.sofascore.com/team/football/' + west-bromwich-albion/8'
    file_name = sf.timeStamp + ' ' + sf.slug + '.json'
    # print(file_name)
    sofa = namedtuple(
        'sofa', 'timeStamp, homeTeam, awayTeam, homeTeamSlug, awayTeamSlug, homeTeamId, awayTeamId')
    with open(files(file_name, folder='SofaScore_Json'), 'r') as f:
        json_data = json.load(f)
        events = [sofa(timeStamp=datetime.fromtimestamp(event['startTimestamp']).strftime(std_date_time_format()),
                       homeTeam=event['homeTeam']['name'],
                       awayTeam=event['awayTeam']['name'],
                       homeTeamId=event['homeTeam']['id'],
                       awayTeamId=event['awayTeam']['id'],
                       homeTeamSlug=event['homeTeam']['slug'],
                       awayTeamSlug=event['awayTeam']['slug'],
                       ) for event in json_data['events'] if event['status']['type'] == "notstarted"]
        sf_ = sorted(events)[0]
        # print('length', str(len(events)))
        home_team_url = 'https://www.sofascore.com/team/football/' + \
            sf_.homeTeamSlug + '/' + str(sf_.homeTeamId)
        away_team_url = 'https://www.sofascore.com/team/football/' + \
            sf_.awayTeamSlug + '/' + str(sf_.awayTeamId)
        print(home_team_url)
        log(home_team_url)
        print(away_team_url)
        log(away_team_url)
        # over = [event.totalScore for event in events]
    pass


def get_single_team_history():
    with open(r"Real_Sociedad.json", 'r') as openfile:
        # Reading from json file
        team_json = json.load(openfile)

    events = team_json['events']
    history = namedtuple(
        'history', 'timeStamp, homeTeam, awayTeam, homeId, awayId')
    for event in events:
        timestamp_ = event['startTimestamp']
        timestamp = datetime.fromtimestamp(timestamp_)
        print(timestamp)

        history = history(timeStamp=datetime.fromtimestamp(event['startTimestamp']).strftime(std_date_time_format()),
                          homeTeam=event['homeTeam']['slug'],
                          awayTeam=event['awayTeam']['slug'],
                          homeId=event['homeTeam']['id'],
                          awayId=event['awayTeam']['id'])
        print(event['homeTeam']['slug'], 'Vs',
              event['awayTeam']['slug'], sep='\t')
        print(event['homeTeam']['id'], 'Vs', event['awayTeam']['id'], sep='\t')
        print(event['homeScore']['normaltime'], 'Vs',
              event['awayScore']['normaltime'], sep='\t')
        print(event['homeScore']['period1'], 'Vs',
              event['awayScore']['period1'], sep='\t')
        print(history)
        try:
            # score2 = event['homeScore']['period2']
            print(event['homeScore']['period2'], 'Vs',
                  event['awayScore']['period2'], sep='\t')
        except KeyError:
            pass
        print('')


def get_past_winners(sf, gsb, no_of_months=10):
    file_name = sf.timeStamp + ' ' + sf.slug + '.json'
    # print(sf)
    sofa = namedtuple(
        'sofa', 'timeStamp, homeTeam, homeScore, totalScore, awayScore, awayTeam, winnerCode')
    with open(files(file_name, folder='SofaScore_Json'), 'r') as f:
        json_data = json.load(f)
        try:
            json_data['events']
            proceed = True
        except KeyError:
            proceed = final = False
        if proceed:
            events = [sofa(timeStamp=datetime.fromtimestamp(event['startTimestamp']).strftime(std_date_time_format()),
                           homeTeam=event['homeTeam']['name'],
                           awayTeam=event['awayTeam']['name'],
                           homeScore=event.get('homeScore').get(
                               'normaltime', 0),
                           awayScore=event.get('awayScore').get(
                               'normaltime', 0),
                           totalScore=event.get('homeScore').get('normaltime', 0) +
                           event.get('awayScore').get('normaltime', 0),
                           winnerCode=event['homeTeam']['name'] if event.get("winnerCode") == 1 else event['awayTeam'][
                'name'] if event.get("winnerCode") == 2 else 'Draw'
            ) for event in json_data['events'] if event['status']['type'] == "finished"]
            two_years_ago = (datetime.today() - timedelta(days=366)
                             ).strftime(std_date_time_format())
            few_months_ago = (datetime.today() - timedelta(days=30 *
                                                           no_of_months)).strftime(std_date_time_format())

            events1 = [
                event for event in events if event.timeStamp >= two_years_ago]
            events2 = [
                event for event in events if event.timeStamp < two_years_ago]
            # TODO: Check events to add half time events
            # print(events1)
            # print(events2)
            try:
                last_match_time = events1[0].timeStamp >= few_months_ago
            except IndexError:
                last_match_time = False
            over = {event.winnerCode for event in events1}
            # print('This is supposed to be a set')
            # print(over)

            if len(events1) >= 2 and len(over) == 1 and list(over)[0] == sf.homeTeam and last_match_time:
                print('____________________________________________')
                # print(sf.eventId)
                print('____________________________________________')
                print('\n###', gsb.timeStamp, sf.homeTeam, sf.awayTeam, sep='\t')
                print('In', (datetime.strptime(gsb.timeStamp,
                                               std_date_time_format()) - datetime.now()).days, 'days')
                total_score = '*****  We Have a Winner  *****'
                print(total_score)
                logger(
                    f'{sf.timeStamp}\t{sf.homeTeam}\t{sf.awayTeam}\t{sf.homeTeam}')

                for line in events1:
                    # print(line)
                    print(line.homeScore, line.awayScore,
                          line.totalScore, line.winnerCode)
                print(pd.DataFrame(events1))
                print(pd.DataFrame(events2[:10]))
                final = True
            else:
                final = False
    return final


def permutation():
    # TODO: Generate Tickets skipping taking n events n-m times
    pass


def single_team_history(team_id):
    team_id = str(team_id)
    final = []
    for i in range(0, 4):
        url = 'https://api.sofascore.com/api/v1/team/' + \
            team_id + '/events/last/' + str(i)
        # team_id = re.split('team/(.*?)/events', url, re.DOTALL)[1]
        # print(team_id + '-' + str(i))

        if not os.path.exists(files(team_id + '-' + str(i) + '.json', 'History')):
            req = session_request(url, sofa_session, header='headers_sofa')
            with open(files(team_id + '-' + str(i) + '.json', 'History'), 'w', encoding='utf-8') as f:
                json.dump(req.json(), f, indent=4)
            # print(req.json())
        with open(files(team_id + '-' + str(i) + '.json', 'History'), 'r', encoding='utf-8') as f:
            json_file = json.load(f)
            History = namedtuple('History',
                                 'timeStamp, tournament, homeTeamId, homeTeam, homeScore, awayScore, awayTeam, awayTeamId, winnerCode')
            if not json_file.get('error', False):
                events = [
                    History(timeStamp=str(datetime.fromtimestamp(event["startTimestamp"]).strftime('%Y-%m-%d %H%M%S')),
                            tournament=event['tournament']['name'],
                            homeTeamId=event['homeTeam']['id'],
                            homeTeam=event['homeTeam']['name'],
                            homeScore=event['homeScore']['normaltime'] if event.get('homeScore').get(
                                'normaltime') is not None else event.get('homeScore').get('display', None),
                            # 'normaltime
                            awayScore=event['awayScore']['normaltime'] if event.get('awayScore').get(
                                'normaltime') is not None else event.get('awayScore').get('display', None),
                            # 'normaltime
                            awayTeam=event['awayTeam']['name'],
                            awayTeamId=event['awayTeam']['id'],
                            winnerCode=event.get('winnerCode', None)) for event in json_file['events'] if
                    event["status"]["description"] is not "Canceled"]
                final = final + events
    cloudpickle.dump(final, open(files(team_id + '.txt', 'History'), 'wb'))
    # for item in final:
    #     print(item)


def double_team_history(sf,  save_folder='', id1=42, id2=3179, min_wins=10):
    single_team_history(id1)
    single_team_history(id2)

    team1 = cloudpickle.load(open(files(str(id1) + '.txt', 'History'), 'rb'))
    team2 = cloudpickle.load(open(files(str(id2) + '.txt', 'History'), 'rb'))

    team1 = [
        line for line in team1 if line.timeStamp is not None and line.winnerCode is not None]
    team2 = [
        line for line in team2 if line.timeStamp is not None and line.winnerCode is not None]
    team1 = [line for line in sorted(team1,
                                     key=lambda x: x.timeStamp,
                                     reverse=True) if str(line.timeStamp) >= '2021-08-01 000000']
    team2 = [line for line in sorted(team2,
                                     key=lambda x: x.timeStamp,
                                     reverse=True) if str(line.timeStamp) >= '2021-08-01 000000']
    out_list = []
    # form1 = filter(lambda x: x[1] if x[0]<=9 else None, enumerate(team1))
    form1 = [match for i, match in enumerate(team1) if i <= 9]
    form2 = [match for i, match in enumerate(team2) if i <= 9]
    forms = [(x.timeStamp, x.homeTeam, x.homeTeamId, x.homeScore, x.winnerCode, x.awayScore, x.awayTeamId, x.awayTeam,
              y.timeStamp, y.homeTeam, y.homeTeamId, y.homeScore, y.winnerCode, y.awayScore, y.awayTeamId, y.awayTeam) for x, y in zip(form1, form2)]
    form = pd.DataFrame(forms)
    form[4] = ['D' if w == 3 else 'W' if w == 1 and h == id1 else 'W' if w ==
               2 and a == id1 else 'L' for h, w, a in zip(form[2], form[4], form[6])]
    form[12] = ['D' if w == 3 else 'W' if w == 1 and h == id2 else 'W' if w ==
                2 and a == id2 else 'L' for h, w, a in zip(form[10], form[12], form[14])]
    form.drop([2, 6, 10, 14], axis=1, inplace=True)
    print(form)

    for pair1 in team1:
        # print(pair1)
        h1, a1 = pair1.homeTeamId, pair1.awayTeamId
        for pair2 in team2:
            # print(pair2)
            h2, a2 = pair2.homeTeamId, pair2.awayTeamId
            common = {h1, a1, h2, a2}
            inter = {h1, a1}.intersection({h2, a2})
            if len(common) == 3 and list(inter)[0] != 1 and list(inter)[0] != id1 and list(inter)[0] != id2:
                # print(h1, h2, a1, a2, inter)
                out1 = [pair1.timeStamp, pair1.homeTeam, pair1.homeScore, pair1.awayScore, pair1.awayTeam,
                        'Draw' if pair1.winnerCode == 3 else 'Win' if pair1.winnerCode == 1 and pair1.homeTeamId == id1 else
                        'Win' if pair1.winnerCode == 2 and pair1.awayTeamId == id1 else 'Loss']
                out2 = [pair2.timeStamp, pair2.homeTeam, pair2.homeScore, pair2.awayScore, pair2.awayTeam,
                        'Draw' if pair2.winnerCode == 3 else 'Win' if pair2.winnerCode == 1 and pair2.homeTeamId == id2 else
                        'Win' if pair2.winnerCode == 2 and pair2.awayTeamId == id2 else 'Loss']
                out_list.append(out1 + out2)
                team2.remove(pair2)
                break
    # println(out_list)
    frame = pd.DataFrame(out_list,
                         columns=['timeStamp1', 'homeTeam1', 'hG1', 'aG1', 'awayTeam1', 'Analysis1',
                                  'timeStamp2', 'homeTeam2', 'hG2', 'aG2', 'awayTeam2', 'Analysis2'])

    group1 = frame.groupby('Analysis1').count()
    group2 = frame.groupby('Analysis2').count()
    group1 = group1.rename(columns={'Analysis1': 'Analysis'})
    group2 = group2.rename(columns={'Analysis2': 'Analysis'})
    group1.drop(['timeStamp2', 'homeTeam1', 'hG1', 'aG1', 'awayTeam1', 'homeTeam2',
                 'hG2', 'aG2', 'awayTeam2'], inplace=True, axis=1)

    group2.drop(['timeStamp2', 'homeTeam1', 'hG1', 'aG1', 'awayTeam1', 'homeTeam2',
                 'hG2', 'aG2', 'awayTeam2'], inplace=True, axis=1)

    try:
        group1.loc['Win'].iloc[0]
    except KeyError:
        dfx = pd.DataFrame({'timeStamp1': 0, 'Analysis2': 0}, index=['Win'])
        group1.loc['Win'] = dfx.loc['Win']

    try:
        group2.loc['Win'].iloc[0]
    except KeyError:
        dfy = pd.DataFrame({'timeStamp1': 0, 'Analysis1': 0}, index=['Win'])
        group2.loc['Win'] = dfy.loc['Win']

    df = group1 - group2
    dfp = df
    df.drop(['Analysis1', 'Analysis2'], inplace=True, axis=1)
    try:
        # wins = abs(int(df.loc['Win'].iloc[0]))
        wins = int(df.loc['Win'].iloc[0])
        if wins >= min_wins:
            printseperator()
            print(f'Wheat\t{wins}')
            print(frame)
            dfi.export(frame, files(f'{sf.timeStamp} {sf.homeTeam} {sf.awayTeam} XWins-Wheat.png', f'PNGS\{save_folder}'))
            # print(dfp)
            # print(group1)
            # print(group2)
            print(df)
            print(f'Wins\t{wins}')
            return True
        else:
            printseperator()
            print(f'Chaff\t{wins}')
            print(frame)
            dfi.export(frame, files(f'{sf.timeStamp} {sf.homeTeam} {sf.awayTeam} XWins-Chaff.png', f'PNGS\{save_folder}'))
            # print(dfp)
            # print(group1)
            # print(group2)
            print(df)
            print(f'Wins\t{wins}')
            return True
    except (ValueError, KeyError):
        print('Error on Comparison')
        return False
        pass


def main(min_, over, under, sf, min_xh_wins=20, look_back_mm=20, starting_offset=0, sf_offset=2):
    hours_ = 10

    t1 = open(files(r'000 timer.txt'), 'r', encoding='utf-8')
    try:
        run_time = datetime.strptime(
            t1.readlines()[-1], std_date_time_format_dotted())
        # run_time = datetime.strptime('2021-01-01 00:00:00', std_date_time_format_dotted())
    except (IndexError, ValueError):
        run_time = datetime.strptime(
            '2021-01-01 00:00:00', std_date_time_format_dotted())
    # run_time = datetime.strptime(t1.readlines()[-1],
    #                              std_date_time_format_dotted()) if t1.readlines()[-1] is not "" else '2021-01-01 00:00:00'
    # print(datetime.now() - run_time)
    # starting_offset, sf_offset = 0, 2
    if datetime.now() - timedelta(hours=hours_) >= run_time:
        t1.close()
        try:
            with open(files(r'000 timer.txt'), 'w', encoding='utf-8') as t2:
                t2.write('Start\n')
                t2.write(datetime.now().strftime(
                    std_date_time_format_dotted()))
                clear()
                # pawa_last_time_stamp = betpawa()
                # TODO: switch out betpawa()
                gal()
                # sf_offset = ((datetime.strptime(pawa_last_time_stamp,
                #                                 std_date_time_format()) - datetime.now()).days + 1)//3
                # sf_offset = 4
                print(sf_offset)
                # print('Last Date ', pawa_last_time_stamp, ' ', sf_offset, ' Days of Offset')
                print('Last Date ', sf_offset, ' Days of Offset')
                sofa_score_multiple_query(query=sf, offset=sf_offset)
                combine(start_off=starting_offset, off=sf_offset)
                # TODO: switch combine()
                get_gsb_sf_events(min_matches=min_, over=over, under=under,
                                  min_xh_wins=min_xh_wins, mm=look_back_mm)
                # TODO: switch out get_bp_sf_events()

        except ConnectionError:
            with open(files(r'000 timer.txt'), 'w', encoding='utf-8') as t3:
                t3.write('Start\n')
                t3.write(str(datetime.now() - timedelta(hours=hours_)))
    else:
        combine(start_off=starting_offset, off=sf_offset)
        get_gsb_sf_events(min_matches=min_, over=over, under=under,
                          min_xh_wins=min_xh_wins, mm=look_back_mm)

# main(min_=3, over=1.5, under=3.5, sf=True, min_xh_wins=3, look_back_mm=6, starting_offset=0, sf_offset=2)
n = 2

main(min_=2, over=3.5, under=1.5, sf=True, min_xh_wins=3, look_back_mm=12, starting_offset=0, sf_offset=n)
main(min_=2, over=2.5, under=2.5, sf=True, min_xh_wins=3, look_back_mm=8, starting_offset=0, sf_offset=n)
main(min_=2, over=1.5, under=3.5, sf=True, min_xh_wins=3, look_back_mm=6, starting_offset=0, sf_offset=n)

main(min_=2, over=0.5, under=7.5, sf=True, min_xh_wins=3, look_back_mm=6, starting_offset=0, sf_offset=1)
main(min_=2, over=0.5, under=7.5, sf=True, min_xh_wins=3, look_back_mm=6, starting_offset=1, sf_offset=2)
# main(min_=2, over=0.5, under=7.5, sf=True, min_xh_wins=3, look_back_mm=6, starting_offset=2, sf_offset=3)
# main(min_=2, over=0.5, under=7.5, sf=True, min_xh_wins=3, look_back_mm=6, starting_offset=3, sf_offset=4)


if sys.platform.startswith('win'):
    end_sound = 'C:\Program Files\Microsoft Office\Office16\MEDIA\LYNC_fastbusy.wav'
    winsound.PlaySound(end_sound, winsound.SND_FILENAME)
end_time = datetime.now()
print(end_time - start_time)

