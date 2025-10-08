import os
import shutil

from multiprocessing import Pool
import subprocess

import pypdf
from pypdf import PdfMerger
from pypdf.annotations import FreeText

from fpdf import FPDF

team_dict = {
    'TRF': 'Tampa Bay Rays Futures',
    'CC': 'Corpus Christi Hooks',
    'GT': 'Georgia Tech Yellow Jackets',
    'SA': 'San Antonio Missions',
    'CLT': 'Charlotte Knights',
    'WS': 'Winston-Salem Dash',
    'RC': 'Rancho Cucamonga Quakes',
    'DTF': 'Detroit Tigers Futures',
    'MIS': 'Mississippi Braves',
    'RR': 'Round Rock Express',
    'PHF': 'Philadelphia Phillies Futures',
    'WNP': 'Washington Nationals Prospects',
    'CRF': 'Cincinnati Reds Futures',
    'ABF': 'Atlanta Braves Futures',
    'MCC': 'Manatee C.C. Lancers',
    'NEW': 'New Orleans Zephyrs',
    'NWA': 'Northwest Arkansas Naturals',
    'CHS':  'Charleston RiverDogs',
    'KIW': 'Kiwoom Heroes',
    'NYF': 'New York Yankees Futures',
    'UGA': 'Georgia Bulldogs',
    'LGT': 'LG Twins',
    'OKL': 'Oklahoma RedHawks',
    'SL': 'Salt Lake Bees',
    'SLEO': 'St. Leo\'s Lions',
    'SYR': 'Syracuse SkyChiefs',
    'PNS': 'Pensacola Blue Wahoos',
    'CUB': 'Cuba',
    'FAU': 'Florida Atlantic Owls',
    'POR': 'Portland Beavers',
    'KIA': 'Kia Tigers',
    'NHF': 'Hokkaido Nippon Ham Fighters',
    'TUL': 'Tulsa Drillers',
    'YOM': 'Tokyo Yomiuri Giants',
    'SOF': 'Stars of the Future',
    'ECK': 'Eckerd Tritons',
    'MAN': 'State College of Florida, Manatee-Sarasota',
    'TAC': 'Tacoma Rainiers',
    'GBO': 'Greensboro Grasshoppers',
    'UM': 'Minnesota Golden Gophers',
    'MID': 'Midland RockHounds',
    'PMB': 'Palm Beach Cardinals',
    'VER': 'Rojos del Aguila de Veracruz',
    'BC': 'Boston College Eagles',
    'VT': 'Virginia Tech Hokies',
    'AL': 'American League All-Stars',
    'ARM': 'Army Black Knights',
    'ABQ': 'Albuquerque Isotopes',
    'ALT': 'Altoona Curve',
    'ANA': 'Anaheim Angels',
    'FLA': 'Florida Marlins',
    'SLB': 'St. Louis Browns',
    'KCA': 'Kansas City Athletics',
    'PHA': 'Philadelphia Athletics',
    'NYG': 'New York Giants',
    'BRO': 'Brooklyn Dodgers',
    'WAS': 'Washington Senators',
    'BSN': 'Boston Braves',
    'AZ': 'Arizona Diamondbacks',
    'ASU': 'Arizona State Sun Devils',
    'ATL': 'Atlanta Braves',
    'AUS': 'Australia',
    'BAL': 'Baltimore Orioles',
    'BIR': 'Birmingham Barons',
    'BOS': 'Boston Red Sox',
    'CAL': 'California Angels',
    'CAN': 'Canada',
    'CCC': 'Coastal Carolina University Chanticleers',
    'CHC': 'Chicago Cubs',
    'CIN': 'Cincinnati Reds',  # Cincinnati Redlegs 1954-1959
    'CLE': 'Cleveland Guardians',  # Cleveland Indians before 2022
    'CAR': 'Carolina Mudcats',
    'COL': 'Colorado Rockies',
    'CPBL': 'CPBL All-Stars',
    'CWS': 'Chicago White Sox',
    'DET': 'Detroit Tigers',
    'DOM': 'Dominican Republic',
    'DUR': 'Durham Bulls',
    'ELP': 'El Paso Chihuahuas',
    'ESP': 'Spain',
    'FSU': 'Florida State Seminoles',
    'FIU': 'Florida International University Panthers',
    'FSC': 'Florida Southern College Mocs',
    'FRE': 'Fresno Grizzlies',
    'FRI': 'Frisco RoughRiders',
    'FTM': 'Fort Myers Miracle',
    'GBR': 'Great Britain',
    'GCU': 'Grand Canyon Antelopes',
    'GEO': 'Georgetown University Hoyas',
    'HAN': 'Hanshin Tigers',
    'HOU': 'Houston Astros',  # Houston Colt 45's - before 1965
    'ISR': 'Israel',
    'ITA': 'Italy',
    'JAX': 'Jacksonville Suns',
    'JPN': 'Japan',
    'KC': 'Kansas City Royals',
    'KOR': 'Korea',
    'LAA': 'Los Angeles Angels',
    'LA': 'Los Angeles Dodgers',
    'LAD': 'Los Angeles Dodgers',
    'LE': 'Lake Elsinore Storm',
    'LHV': 'Lehigh Valley IronPigs',
    'MEX': 'Mexico',
    'MIA': 'Miami Marlins',
    'MIL': 'Milwaukee Brewers', # Milwuakee Braves before 1966
    'MIN': 'Minnesota Twins',
    'MON': 'Montreal Expos',
    'MEM': 'Memphis Redbirds',
    'MTY': 'Sultanes de Monterrey',
    'NL': 'National League All-Stars',
    'NCA': 'Nicaragua',
    'NED': 'Kingdom of the Netherlands',
    'NEU': 'Northeastern University Huskies',
    'NOR': 'Norfolk Tides',
    'NYM': 'New York Mets',
    'NYY': 'New York Yankees',
    'OAK': 'Oakland Athletics',
    'OMA': 'Omaha Storm Chasers',
    'PAN': 'Panama',
    'PHI': 'Philadelphia Phillies',
    'PIT': 'Pittsburgh Pirates',
    'PUR': 'Puerto Rico',
    'TIG': 'Tigres de Quintana Roo',
    'ROC': 'Rochester Red Wings',
    'RSA': 'South Africa',
    'SD': 'San Diego Padres',
    'SEA': 'Seattle Mariners', # Seattle Pilots before 1977
    'SEU': 'Southeastern U. Fire',
    'SF': 'San Francisco Giants',
    'SFF': 'San Francisco Giants Futures',
    'SPR': 'Springfield Cardinals',
    'SAC': 'Sacramento River Cats',
    'STL': 'St. Louis Cardinals',
    'SUG': 'Sugar Land Space Cowboys',
    'TB': 'Tampa Bay Rays',  # Tampa Bay Devil Rays - before 2008
    'TEX': 'Texas Rangers',
    'TOR': 'Toronto Blue Jays',
    'UA': 'University of Arizona Wildcats',
    'USA': 'United States',
    'USF': 'University of South Florida Bulls',
    'UT': 'University of Tampa Spartans',
    'UWM': 'University of Wisconsin-Milwaukee Panther',
    'VEN': 'Venezuela',
    'WSH': 'Washington Nationals',
    'MTG': 'Montgomery Biscuits'
}


def f(team):
    team_files = sorted(os.listdir(f"/Volumes/B_Crom_SSD/binding_books_2/{team}"))
    if len(team_files) > 200 and team != 'AL' and team != 'NL':
        for year in range(1950, 2024):
            has_scorecards = False
            this_merger = PdfMerger()
            for team_file in team_files:
                if team_file[0:2] == '._': continue
                if team_file[0:4] == str(year) and 'title' not in team_file:
                    if has_scorecards is False:
                        this_merger.append(f"/Volumes/B_Crom_SSD/binding_books_2/{team}/{year}-{team}-title.pdf")
                        has_scorecards = True

                    this_merger.append(f'/Volumes/B_Crom_SSD/binding_books_2/{team}/{team_file}')

            if has_scorecards:
                this_merger.write(f'/Volumes/B_Crom_SSD/bound_books/{team}/{year}-{team}-two-page.pdf')

            this_merger.close()
            this_merger = None
    else:
        this_merger = PdfMerger()
        this_merger.append(f"/Volumes/B_Crom_SSD/binding_books_2/{team}/{team}-title.pdf")
        for team_file in team_files:
            if team_file[0:2] == '._': continue
            if 'title' not in team_file:
                this_merger.append(f'/Volumes/B_Crom_SSD/binding_books_2/{team}/{team_file}')

        this_merger.write(f'/Volumes/B_Crom_SSD/bound_books/{team}/{team}-two-page.pdf')
        this_merger.close()
        this_merger = None

if __name__ == '__main__':
    team_list = [t for t in team_dict]
    with Pool(16) as p:
        p.map(f, team_list)
