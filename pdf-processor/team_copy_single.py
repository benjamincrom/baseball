import os
import shutil

from multiprocessing import Pool

team_set = {'ABF', 'ABQ', 'AL', 'ALT', 'ANA', 'ARM', 'ASU', 'ATL', 'AUS', 'AZ', 'BAL', 'BC', 'BIR',
            'BOS', 'BRO', 'BSN', 'CAL', 'CAN', 'CAR', 'CC', 'CCC', 'CHC', 'CHS', 'CIN', 'CLE',
            'CLT', 'COL', 'CPBL', 'CRF', 'CUB', 'CWS', 'DET', 'DOM', 'DTF', 'DUR', 'ECK', 'ELP',
            'ESP', 'FAU', 'FIU', 'FLA', 'FRE', 'FRI', 'FSC', 'FSU', 'FTM', 'GBO', 'GBR', 'GCU',
            'GEO', 'GT', 'HAN', 'HOU', 'ISR', 'ITA', 'JAX', 'JPN', 'KC', 'KCA', 'KIA', 'KIW',
            'KOR', 'LA', 'LAA', 'LAD', 'LE', 'LGT', 'LHV', 'MAN', 'MCC', 'MEM', 'MEX', 'MIA',
            'MID', 'MIL', 'MIN', 'MIS', 'MON', 'MTG', 'MTY', 'NCA', 'NED', 'NEU', 'NEW', 'NHF',
            'NL', 'NOR', 'NWA', 'NYF', 'NYG', 'NYM', 'NYY', 'OAK', 'OKL', 'OMA', 'PAN', 'PHA',
            'PHF', 'PHI', 'PIT', 'PMB', 'PNS', 'POR', 'PUR', 'RC', 'ROC', 'RR', 'RSA', 'SA', 'SAC',
            'SD', 'SEA', 'SEU', 'SF', 'SFF', 'SL', 'SLB', 'SLEO', 'SOF', 'SPR', 'STL', 'SUG', 'SYR',
            'TAC', 'TB', 'TEX', 'TIG', 'TOR', 'TRF', 'TUL', 'UA', 'UGA', 'UM', 'USA', 'USF', 'UT',
            'UWM', 'VEN', 'VER', 'VT', 'WAS', 'WNP', 'WS', 'WSH', 'YOM'}

def f(team):
    files = os.listdir("/Volumes/B_Crom_SSD/pdf2")
    os.mkdir(f'/Volumes/B_Crom_SSD/binding_books_1/{team}')
    team_file_list = [f for f in files if f'-{team}-' in f]
    for team_file in team_file_list:
        shutil.copy(f"/Volumes/B_Crom_SSD/pdf2/{team_file}",
                    f"/Volumes/B_Crom_SSD/binding_books_1/{team}/")

if __name__ == '__main__':
    with Pool(16) as p:
        p.map(f, team_set)
