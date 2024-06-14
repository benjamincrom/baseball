import os
import shutil

from multiprocessing import Pool

import pypdf
from pypdf import PdfMerger

import pypdf
from pypdf import PdfMerger, PdfReader, PdfWriter, Transformation
from pypdf.generic import RectangleObject

from fpdf import FPDF

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
    'MIL': 'Milwaukee Brewers',
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
    'SEA': 'Seattle Mariners',
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

def f():
    for team in team_dict:
        team_name = team_dict[team]
        writer = FPDF('P', 'mm', (841, 1189))
        writer.add_page()
        writer.set_font('helvetica', size=117)
        writer.set_xy(65, 332)
        writer.multi_cell(715, 46, border=0, txt=f"{team_name}", align='C')
        writer.output(f"/Volumes/B_Crom_SSD/binding_books_1/{team}/{team}-title.pdf")

        with open(f'/Volumes/B_Crom_SSD/binding_books_1/{team}/{team}-title.pdf', "rb") as in_f:
            input1 = PdfReader(in_f)

            output = PdfWriter()
            page = input1.get_page(0)
            op = Transformation().scale(sx=0.7723, sy=0.7723).translate(tx=275, ty=300)
            page.add_transformation(op)
            page.scale_by(0.7723)
            page.rotate(90)

            x, y = page.mediabox.upper_right
            page.trimbox.lower_left = (0, 0)
            page.trimbox.upper_right = (x, y*0.9163)
            page.cropbox.lower_left = (0, 0)
            page.cropbox.upper_right = (x, y*0.9163)
            page.mediabox = RectangleObject((0, 0, x, y*0.9163))

            output.add_page(page)
            output.write(f'/Volumes/B_Crom_SSD/binding_books_2/{team}/{team}-title.pdf')

        team_files = os.listdir(f"/Volumes/B_Crom_SSD/binding_books_1/{team}")
        for team_file in team_files:
            for year in range(1950, 2024):
                if team == 'CLE' and year < 2022:
                    team_name = 'Cleveland Indians'
                elif team == 'CLE' and year >= 2022:
                    team_name = 'Cleveland Guardians'
                elif team == 'CIN' and year >= 1954 and year <= 1959:
                    team_name = 'Cincinnati Redlegs'
                elif team == 'CIN' and (year < 1954 or year > 1959):
                    team_name = 'Cincinnati Reds'
                elif team == 'TB' and year < 2008:
                    team_name = 'Tampa Bay Devil Rays'
                elif team == 'TB' and year >= 2008:
                    team_name = 'Tampa Bay Rays'
                elif team == 'HOU' and year < 1965:
                    team_name = 'Houston Colt 45\'s'
                elif team == 'HOU' and year >= 1965:
                    team_name = 'Houston Astros'
                elif team == 'MIL' and year < 1966:
                    team_name = 'Milwaukee Braves'
                elif team == 'MIL' and year >= 1966:
                    team_name = 'Milwaukee Brewers'

                if str(year) == team_file[0:4]:
                    writer = FPDF('P', 'mm', (841, 1189))
                    writer.add_page()
                    writer.set_font('helvetica', size=117)
                    writer.set_xy(65, 332)
                    writer.multi_cell(715, 46, border=0, txt=f"{team_name} - {year}", align='C')
                    writer.output(f"/Volumes/B_Crom_SSD/binding_books_1/{team}/{year}-{team}-title.pdf")

                    with open(f'/Volumes/B_Crom_SSD/binding_books_1/{team}/{year}-{team}-title.pdf', "rb") as in_f:
                        input1 = PdfReader(in_f)

                        output = PdfWriter()
                        page = input1.get_page(0)
                        op = Transformation().scale(sx=0.7723, sy=0.7723).translate(tx=275, ty=300)
                        page.add_transformation(op)
                        page.scale_by(0.7723)
                        page.rotate(90)

                        x, y = page.mediabox.upper_right
                        page.trimbox.lower_left = (0, 0)
                        page.trimbox.upper_right = (x, y*0.9163)
                        page.cropbox.lower_left = (0, 0)
                        page.cropbox.upper_right = (x, y*0.9163)
                        page.mediabox = RectangleObject((0, 0, x, y*0.9163))

                        output.add_page(page)
                        output.write(f'/Volumes/B_Crom_SSD/binding_books_2/{team}/{year}-{team}-title.pdf')


if __name__ == '__main__':
    f()
