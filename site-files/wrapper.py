import hashlib
import os
import shutil

from lmdbm import Lmdb

import baseball

from ddtrace import tracer

def my_hash(input):
    h = hashlib.new('md5')
    h.update(input.encode("utf-8"))
    return h.hexdigest()


class MyLmdb(Lmdb):
    def _pre_key(self, value):
        return str(value).encode("utf-8")
    def _post_key(self, value):
        return value.decode("utf-8")
    def _pre_value(self, value):
        return str(value).encode("utf-8")
    def _post_value(self, value):
        return value.decode("utf-8")


@tracer.wrap(service="get_todays_games", resource="wrapper")
def get_todays_games():
    with MyLmdb.open("/mnt/delay/hash.db", "c", map_size=2**30, autogrow=False) as hash_map:
        for this_file in os.listdir('/mnt/delay/3600'):
            file_path = f'/mnt/delay/3600/{this_file}'
            hash_map[file_path] = ""

        shutil.rmtree('/mnt/delay/3600')
        os.mkdir('/mnt/delay/3600')
        for i in range(3595, -5, -5):
            for this_file in os.listdir(f'/mnt/delay/{str(i)}'):
                source_path = f'/mnt/delay/{str(i)}/{this_file}'
                dest_dir = f'/mnt/delay/{str(i+5)}/'
                dest_path = f'{dest_dir}{this_file}'
                source_hash = hash_map.get(source_path, 0)
                dest_hash = hash_map.get(dest_path, 0)
                if source_hash == 0:
                    with open(source_path, 'r') as filehandle:
                        source_text = filehandle.read()
                        source_hash = my_hash(source_text)
                        hash_map[source_path] = source_hash
                else:
                    with open(source_path, 'r') as fh:
                        text1 = fh.read()

                if dest_hash == 0:
                    if os.path.isfile(dest_path):
                        with open(dest_path, 'r') as filehandle:
                            dest_text = filehandle.read()
                            dest_hash = my_hash(dest_text)
                            hash_map[dest_path] = dest_hash
                    else:
                        shutil.copy(source_path, dest_dir)
                        dest_hash = source_hash
                        hash_map[dest_path] = dest_hash

                if source_hash != dest_hash:
                    shutil.copy(source_path, dest_dir)
                    dest_hash = source_hash
                    hash_map[dest_path] = dest_hash

        prime_dir = "/mnt/delay/0/"
        dest_dir = '/var/www/html/'
        baseball.generate_today_game_svgs(prime_dir, True, True, True)
        files = os.listdir(prime_dir)
        for this_file in files:
            source_path = f'{prime_dir}{this_file}'
            dest_path = f'{dest_dir}{this_file}'
            with open(source_path, 'r') as filehandle:
                source_text = filehandle.read()
                hash_text = my_hash(source_text)
                hash_map[source_path] = hash_text
                try:
                    with open(dest_path, 'r') as filehandle_2:
                        dest_svg_text = filehandle_2.read()
                        if source_svg_text != dest_svg_text:
                            shutil.copy(source_path, dest_dir)
                except:
                    shutil.copy(f'{prime_dir}{this_file}', dest_dir)


if __name__ == '__main__':
    get_todays_games()
