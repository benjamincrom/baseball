import os
import shutil
import baseball

from ddtrace import tracer

@tracer.wrap(service="get_todays_games", resource="wrapper")
def get_todays_games():
    shutil.rmtree(f'/mnt/delay_volume/5000')
    os.mkdir(f'/mnt/delay_volume/5000')
    for i in range(4995, -5, -5):
        files = os.listdir(f'/mnt/delay_volume/{str(i)}')
        for this_file in files:
            source_path = f'/mnt/delay_volume/{str(i)}/{this_file}'
            dest_path = f'/mnt/delay_volume/{str(i+5)}/'
            with open(source_path, 'r') as filehandle:
                if os.path.isfile(f'{dest_path}{this_file}'):
                    with open(f'{dest_path}{this_file}', 'r') as filehandle_2:
                        source_svg_text = filehandle.read()
                        dest_svg_text = filehandle_2.read()
                        if source_svg_text != dest_svg_text:
                            shutil.copy(source_path, dest_path)
                else:
                    shutil.copy(source_path, dest_path)


    baseball.generate_today_game_svgs("/mnt/delay_volume/0", True, True, True)
    files = os.listdir(f'/mnt/delay_volume/0')
    for this_file in files:
        source_path = f'/mnt/delay_volume/0/{this_file}'
        dest_path = f'/var/www/html/'
        with open(source_path, 'r') as filehandle:
            try:
                with open(f'{dest_path}{this_file}', 'r') as filehandle_2:
                    source_svg_text = filehandle.read()
                    dest_svg_text = filehandle_2.read()
                    if source_svg_text != dest_svg_text:
                        shutil.copy("/mnt/delay_volume/0/" + this_file, "/var/www/html")
            except:
                shutil.copy("/mnt/delay_volume/0/" + this_file, "/var/www/html")
                

if __name__ == '__main__':
    get_todays_games()

