import os
from multiprocessing import Pool

from pypdf import PdfWriter, PdfReader, Transformation, PageObject, PaperSize
from pypdf.generic import RectangleObject

import fitz


def f(arg):
    with open(f'/Volumes/B_Crom_SSD/split-pdfs/{arg}-B.pdf', "rb") as in_f:
        input1 = PdfReader(in_f)
        output = PdfWriter()
        page = input1.get_page(0)

        scale_factor = 0.985
        transform = Transformation().scale(scale_factor, scale_factor).translate(18, 18)
        page.add_transformation(transform)

        mb = page.mediabox
        new_height = (mb.top - mb.bottom) * 1.09228317028
        page.mediabox = RectangleObject((mb.left, mb.bottom, mb.right, mb.bottom + new_height))
        page.cropbox = RectangleObject((mb.left, mb.bottom, mb.right, mb.bottom + new_height))
        page.trimbox = RectangleObject((mb.left, mb.bottom, mb.right, mb.bottom + new_height))
        page.bleedbox = RectangleObject((mb.left, mb.bottom, mb.right, mb.bottom + new_height))
        page.artbox = RectangleObject((mb.left, mb.bottom, mb.right, mb.bottom + new_height))
        output.add_page(page)

        with open(f'/Volumes/B_Crom_SSD/join-pdfs/{arg}-B.pdf', "wb") as out_f:
            output.write(out_f)

        doc = fitz.open(f'/Volumes/B_Crom_SSD/join-pdfs/{arg}-B.pdf')
        doc[0].draw_rect([mb.left, 0, mb.right, 160],
                         fill=(1, 1, 1),
                         color=(1, 1, 1),
                         width=2)

        doc.save(f'/Volumes/B_Crom_SSD/join-mask-pdf/{arg}-B.pdf')
        doc.close()
        os.remove(f'/Volumes/B_Crom_SSD/join-pdfs/{arg}-B.pdf')


if __name__ == '__main__':
    file_list = [
        f.split('.', 1)[0]
        for f in os.listdir('/Volumes/B_Crom_SSD/pdf2')
        if f[-3:] == 'pdf'
    ]

    with Pool(16) as p:
        p.map(f, file_list)
    #for file in file_list:
    #    f(file)
    #    print(file)
