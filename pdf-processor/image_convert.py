import os

from multiprocessing import Pool
import subprocess


def f(x):
    subprocess.call(
        f"rsvg-convert -h 4496 -f pdf -o /Volumes/B_Crom_SSD/pdf2/{x}.pdf /Volumes/B_Crom_SSD/scorecards/{x}.svg",
        shell=True
    )


if __name__ == '__main__':
    file_list = [
        f.split('.', 1)[0]
        for f in os.listdir('/Volumes/B_Crom_SSD/scorecards')
        if f[-3:] == 'svg'
    ]
    with Pool(16) as p:
        p.map(f, file_list)
