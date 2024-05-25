import os
import shutil

def del_folder_contents(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

del_folder_contents('/mnt/delay_volume')

for i in range(0, 3605, 5):
    os.mkdir(f'/mnt/delay_volume/{str(i)}')
