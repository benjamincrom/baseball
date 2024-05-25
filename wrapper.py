import os
import shutil

from lmdbm import Lmdb

import baseball

from ddtrace import tracer


class MyLmdb(Lmdb):
    def _pre_key(self, value):
        return value.encode("utf-8")
    def _post_key(self, value):
        return value.decode("utf-8")
    def _pre_value(self, value):
        return value.to_bytes(8, byteorder="big", signed=True)
    def _post_value(self, value):
        return int.from_bytes(value, byteorder="big", signed=True)


@tracer.wrap(service="get_todays_games", resource="wrapper")
def get_todays_games():
    with MyLmdb.open("/mnt/delay_volume/hash.db", "c") as hash_map:
        for this_file in os.listdir('/mnt/delay_volume/3600'):
            file_path = f'/mnt/delay_volume/3600/{this_file}'
            hash_map[file_path] = 0

        shutil.rmtree('/mnt/delay_volume/3600')
        os.mkdir('/mnt/delay_volume/3600')
        for i in range(3595, -5, -5):
            for this_file in os.listdir(f'/mnt/delay_volume/{str(i)}'):
                source_path = f'/mnt/delay_volume/{str(i)}/{this_file}'
                dest_dir = f'/mnt/delay_volume/{str(i+5)}/'
                dest_path = f'{dest_dir}{this_file}'
                source_hash = hash_map.get(source_path)
                dest_hash = hash_map.get(dest_path)
                if source_hash is None:
                    with open(source_path, 'r') as filehandle:
                        source_svg_text = filehandle.read()
                        source_hash = hash(source_svg_text)
                        hash_map[source_path] = source_hash

                if dest_hash is None:
                    if os.path.isfile(dest_path):
                        with open(dest_path, 'r') as filehandle_2:
                            dest_svg_text = filehandle.read()
                            dest_hash = hash(dest_svg_text)
                            hash_map[dest_path] = dest_hash
                    else:
                        shutil.copy(source_path, dest_dir)
                        dest_hash = source_hash
                        hash_map[dest_path] = dest_hash

                if source_hash != dest_hash:
                    shutil.copy(source_path, dest_dir)
                    dest_hash = source_hash
                    hash_map[dest_path] = dest_hash

        prime_dir = "/mnt/delay_volume/0/"
        dest_dir = '/var/www/html/'
        baseball.generate_today_game_svgs(prime_dir, True, True, True)
        files = os.listdir(prime_dir)
        for this_file in files:
            source_path = f'{prime_dir}{this_file}'
            dest_path = f'{dest_dir}{this_file}'
            with open(source_path, 'r') as filehandle:
                source_svg_text = filehandle.read()
                hash_map[source_path] = hash(source_svg_text)
                try:
                    with open(dest_path, 'r') as filehandle_2:
                        dest_svg_text = filehandle_2.read()
                        if source_svg_text != dest_svg_text:
                            shutil.copy(source_path, dest_dir)
                except:
                    shutil.copy(f'{prime_dir}{this_file}', dest_dir)


if __name__ == '__main__':
    get_todays_games()
