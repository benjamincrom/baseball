import os

mlb_team_dict = {
    'CAL': 'California Angels',
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
    'ATL': 'Atlanta Braves',
    'BAL': 'Baltimore Orioles',
    'BOS': 'Boston Red Sox',
    'CHC': 'Chicago Cubs',
    'CWS': 'Chicago White Sox',
    'CIN': 'Cincinnati Reds',
    'CLE': 'Cleveland Guardians',
    'COL': 'Colorado Rockies',
    'DET': 'Detroit Tigers',
    'LAA': 'Los Angeles Angels',
    'LAD': 'Los Angeles Dodgers',
    'HOU': 'Houston Astros',
    'KC': 'Kansas City Royals',
    'MIA': 'Miami Marlins',
    'MIL': 'Milwaukee Brewers',
    'MIN': 'Minnesota Twins',
    'MON': 'Montreal Expos',
    'NYM': 'New York Mets',
    'NYY': 'New York Yankees',
    'OAK': 'Oakland Athletics',
    'PHI': 'Philadelphia Phillies',
    'PIT': 'Pittsburgh Pirates',
    'SD': 'San Diego Padres',
    'SEA': 'Seattle Mariners',
    'SF': 'San Francisco Giants',
    'STL': 'St. Louis Cardinals',
    'TB': 'Tampa Bay Rays',
    'LA': 'Los Angeles Dodgers',
    'TEX': 'Texas Rangers',
    'TOR': 'Toronto Blue Jays',
    'WSH': 'Washington Nationals'
}

team_dict = {
    'UGA': 'Georgia Bulldogs',
    'PHF': 'Philadelphia Phillies Futures',
    'BIR': 'Birmingham Barons',
    'NYF': 'New York Yankees Futures',
    'MEX': 'Mexico',
    'FIU': 'Florida International University Panthers',
    'NEW': 'New Orleans Zephyrs',
    'POR': 'Portland Beavers',
    'SFF': 'San Francisco Giants Futures',
    'JPN': 'Japan',
    'SL': 'Salt Lake Bees',
    'CLT': 'Charlotte Knights',
    'OMA': 'Omaha Storm Chasers',
    'FSU': 'Florida State Seminoles',
    'ECK': 'Eckerd Tritons',
    'ALT': 'Altoona Curve',
    'DTF': 'Detroit Tigers Futures',
    'MAN': 'State College of Florida, Manatee-Sarasota',
    'SLEO': "St. Leo's Lions",
    'MCC': 'Manatee C.C. Lancers',
    'GT': 'Georgia Tech Yellow Jackets',
    'CUB': 'Cuba',
    'BC': 'Boston College Eagles',
    'FAU': 'Florida Atlantic Owls',
    'NWA': 'Northwest Arkansas Naturals',
    'GBR': 'Great Britain',
    'UA': 'University of Arizona Wildcats',
    'WS': 'Winston-Salem Dash',
    'NEU': 'Northeastern University Huskies',
    'CRF': 'Cincinnati Reds Futures',
    'PUR': 'Puerto Rico',
    'YOM': 'Tokyo Yomiuri Giants',
    'AUS': 'Australia',
    'ITA': 'Italy',
    'LE': 'Lake Elsinore Storm',
    'FSC': 'Florida Southern College Mocs',
    'CAN': 'Canada',
    'TRF': 'Tampa Bay Rays Futures',
    'SAC': 'Sacramento River Cats',
    'ARM': 'Army Black Knights',
    'SYR': 'Syracuse SkyChiefs',
    'NCA': 'Nicaragua',
    'RSA': 'South Africa',
    'SOF': 'Stars of the Future',
    'DUR': 'Durham Bulls',
    'LGT': 'LG Twins',
    'NL': 'National League All-Stars',
    'SUG': 'Sugar Land Space Cowboys',
    'MEM': 'Memphis Redbirds',
    'LHV': 'Lehigh Valley IronPigs',
    'WNP': 'Washington Nationals Prospects',
    'KIA': 'Kia Tigers',
    'ABF': 'Atlanta Braves Futures',
    'ROC': 'Rochester Red Wings',
    'AL': 'American League All-Stars',
    'USF': 'University of South Florida Bulls',
    'MID': 'Midland RockHounds',
    'ELP': 'El Paso Chihuahuas',
    'NED': 'Kingdom of the Netherlands',
    'MTY': 'Sultanes de Monterrey',
    'TAC': 'Tacoma Rainiers',
    'PAN': 'Panama',
    'TUL': 'Tulsa Drillers',
    'VER': 'Rojos del Aguila de Veracruz',
    'JAX': 'Jacksonville Suns',
    'CCC': 'Coastal Carolina University Chanticleers',
    'VT': 'Virginia Tech Hokies',
    'DOM': 'Dominican Republic',
    'RC': 'Rancho Cucamonga Quakes',
    'SPR': 'Springfield Cardinals',
    'RR': 'Round Rock Express',
    'FRI': 'Frisco RoughRiders',
    'PNS': 'Pensacola Blue Wahoos',
    'CPBL': 'CPBL All-Stars',
    'SEU': 'Southeastern U. Fire',
    'CAR': 'Carolina Mudcats',
    'NOR': 'Norfolk Tides',
    'MIS': 'Mississippi Braves',
    'FRE': 'Fresno Grizzlies',
    'TIG': 'Tigres de Quintana Roo',
    'FTM': 'Fort Myers Miracle',
    'UM': 'Minnesota Golden Gophers',
    'PMB': 'Palm Beach Cardinals',
    'ASU': 'Arizona State Sun Devils',
    'GBO': 'Greensboro Grasshoppers',
    'ISR': 'Israel',
    'GEO': 'Georgetown University Hoyas',
    'UT': 'University of Tampa Spartans',
    'VEN': 'Venezuela',
    'ESP': 'Spain',
    'HAN': 'Hanshin Tigers',
    'CC': 'Corpus Christi Hooks',
    'UWM': 'University of Wisconsin-Milwaukee Panther',
    'MTG': 'Montgomery Biscuits',
    'GCU': 'Grand Canyon Antelopes',
    'KIW': 'Kiwoom Heroes',
    'ABQ': 'Albuquerque Isotopes',
    'OKL': 'Oklahoma RedHawks',
    'KOR': 'Korea',
    'SA': 'San Antonio Missions',
    'CHS': 'Charleston RiverDogs',
    'USA': 'United States',
    'NHF': 'Hokkaido Nippon Ham Fighters'
}

url = 'https://spaces-host.nyc3.cdn.digitaloceanspaces.com/scorecard-pdf-archive'
HTML = (
    '<html><head>'
    '<script>'
    '(function(h,o,u,n,d) {{ '
    'h=h[d]=h[d]||{{q:[],onReady:function(c){{h.q.push(c)}}}} \n'
    'd=o.createElement(u);d.async=1;d.src=n \n'
    'n=o.getElementsByTagName(u)[0];n.parentNode.insertBefore(d,n) '
    '}})(window,document,\'script\',\'https://www.datadoghq-browser-agent.com/'
    'datadog-rum.js\',\'DD_RUM\')\n'
    'DD_RUM.onReady(function() {{ '
    'DD_RUM.init({{ '
    'clientToken: \'pubddae1190ff21ff570dd36eaffc141c4d\', '
    'applicationId: \'8d72601e-b047-42da-af09-1ab422e756fa\', '
    'site: \'datadoghq.com\', '
    'service:\'get-todays-games\', '
    'env:\'none\', '
    'sampleRate: 100, '
    'trackInteractions: true, '
    '}})'
    '}})'
    '</script>'
    '</head><body style="background-color:black;"><font size="7" color="white"><strong>Scorebook Archive</strong><br /></font>'
    '<font size="4" color="white"><i>Note: To print the two-page scorebooks, turn on Landscape and Double-Sided printing and turn off Auto-Rotate.</i><br /><br /></font>'
    '<table>'
    f'<tr><td colspan="2"><font size="4" color="white"><strong>Every Single Scorebook in a Zip File (211 GB)</strong></font></td></tr>'
    f'<td><a href="{url}/scorecard-pdf-archive-1950-2023.zip" style="color:lightblue">scorecard-pdf-archive-1950-2023.zip (211 GB)</a></td><td></td></tr><tr><td colspan="2"><br /></td></tr>'
    '{}</table></body></html>'
)

rows_str = ''



for team, team_name in sorted((mlb_team_dict | team_dict).items(), key=lambda item: item[1]):
    if team in mlb_team_dict:
        rows_str += f'<tr><td colspan="2"><font size="4" color="white"><strong>{team_name}</strong></font></td></tr>\n'
        files = os.listdir(f'/Volumes/B_Crom_SSD/bound_books/{team}')
        year_str_set = sorted(set([file[0:4] for file in files]))
        for year in year_str_set:
            if team == 'CLE' and int(year) < 2022:
                team_name = 'Cleveland Indians'
            elif team == 'CLE' and int(year) >= 2022:
                team_name = 'Cleveland Guardians'
            elif team == 'CIN' and int(year) >= 1954 and int(year) <= 1959:
                team_name = 'Cincinnati Redlegs'
            elif team == 'CIN' and (int(year) < 1954 or int(year) > 1959):
                team_name = 'Cincinnati Reds'
            elif team == 'TB' and int(year) < 2008:
                team_name = 'Tampa Bay Devil Rays'
            elif team == 'TB' and int(year) >= 2008:
                team_name = 'Tampa Bay Rays'
            elif team == 'HOU' and int(year) < 1965:
                team_name = 'Houston Colt 45\'s'
            elif team == 'HOU' and int(year) >= 1965:
                team_name = 'Houston Astros'
            elif team == 'MIL' and int(year) < 1966:
                team_name = 'Milwaukee Braves'
            elif team == 'MIL' and int(year) >= 1966:
                team_name = 'Milwaukee Brewers'
            elif team == 'SEA' and int(year) < 1977:
                team_name = 'Seattle Pilots'
            elif team == 'SEA' and int(year) >= 1977:
                team_name = 'Seattle Mariners'

            rows_str += (f'<tr><td><a href="{url}/{team}/{year}-{team}.pdf" style="color:lightblue">{year} {team_name} (single-page)</a></td>\n'
                         f'<td><a href="{url}/{team}/{year}-{team}-two-page.pdf" style="color:lightblue">{year} {team_name} (two-page)</a></td></tr>\n')

        rows_str += f'<tr><td colspan="2"><br /></td></tr>\n'

    elif team in team_dict:
        rows_str += f'<tr><td colspan="2"><font size="4" color="white"><strong>{team_name}</strong></font></td></tr>\n'
        rows_str += (f'<tr><td><a href="{url}/{team}/{team}.pdf" style="color:lightblue">{team_name} (single-page)</a></td>\n'
                     f'<td><a href="{url}/{team}/{team}-two-page.pdf" style="color:lightblue">{team_name} (two-page)</a></td></tr>\n')

        rows_str += f'<tr><td colspan="2"><br /></td></tr>\n'

with open('out.html', 'w') as fh:
    fh.write(HTML.format(rows_str))
