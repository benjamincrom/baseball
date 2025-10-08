#!/bin/bash
# 3:25 PM 2025-06-24
echo "Making directories..." &&
mkdir binding_books_1 binding_books_2 bound_books join-mask-pdf join-pdfs pdf2 scorecards split-pdfs mislabeled &&
echo "Generating SVGs..." &&
python3 ~/repos/baseball/pdf-processor/generate_svgs.py >> errors &&
echo "Moving mislabeled files..." &&
mv scorecards/2015-06-27-AL-NL-1.html scorecards/2015-06-27-AL-NL-1.svg scorecards/2023-05-09-ATL-SD-1.html scorecards/2023-05-09-ATL-SD-1.svg scorecards/2023-05-09-HOU-ATL-1.html scorecards/2023-05-09-HOU-ATL-1.svg scorecards/2023-05-09-HOU-MON-1.html scorecards/2023-05-09-HOU-MON-1.svg scorecards/2023-05-10-CIN-SD-1.html scorecards/2023-05-10-CIN-SD-1.svg scorecards/2023-05-10-HOU-ATL-1.html scorecards/2023-05-10-HOU-ATL-1.svg scorecards/2023-05-10-HOU-SD-1.html scorecards/2023-05-10-HOU-SD-1.svg scorecards/2023-05-10-MON-ATL-1.html scorecards/2023-05-10-MON-ATL-1.svg scorecards/2023-05-10-MON-SD-1.html scorecards/2023-05-10-MON-SD-1.svg scorecards/2023-05-11-HOU-SD-1.html scorecards/2023-05-11-HOU-SD-1.svg scorecards/2023-05-11-HOU-SD-2.html scorecards/2023-05-11-HOU-SD-2.svg mislabeled &&
echo "Copying logos directory..." &&
cp -r ~/repos/baseball/site-files/team_logos scorecards &&
echo "Setting ulimit..." &&
ulimit -n 10000000000000000 &&
echo "Rewriting team_logos links" &&
find scorecards -name '*.svg' -exec sed -i '' -e 's/\/team_logos/\.\/team_logos/g' {} \; &&
echo "Generating PDFs..." &&
python3 ~/repos/baseball/pdf-processor/image_convert.py &&
echo "Unrewriting team_logos links..." &&
find scorecards -name '*.svg' -exec sed -i '' -e 's/\.\/team_logos/\/team_logos/g' {} \; &&
echo "Removing delay header..." &&
find scorecards -name '*.html' -exec sed -i '' -e 's/<div id="delay-header" style="width:100%;/<div id="delay-header" style="visibility: hidden; width:100%;/g' {} \; &&
echo "Splitting PDFs..." &&
python3 ~/repos/baseball/pdf-processor/split_double.py &&
echo "Masking Side A..." &&
python3 ~/repos/baseball/pdf-processor/mask_A_double.py &&
echo "Masking Side B..." &&
python3 ~/repos/baseball/pdf-processor/mask_B_double.py &&
echo "Team Copy Single..." &&
python3 ~/repos/baseball/pdf-processor/team_copy_single.py &&
echo "Team Copy Double..." &&
python3 ~/repos/baseball/pdf-processor/team_copy_double.py &&
echo "Title Pages..." &&
python3 ~/repos/baseball/pdf-processor/title_pages.py &&
echo "Binding Single..." &&
python3 ~/repos/baseball/pdf-processor/binding_single.py &&
echo "Binding Double..." &&
python3 ~/repos/baseball/pdf-processor/binding_double.py &&
echo "Generating Archive HTML file..." &&
python3 ~/repos/baseball/pdf-processor/generate_html.py &&
echo "Preparing scorecards directory..." &&
mv mislabeled scorecards &&
mv errors errors.txt &&
mv errors.txt scorecards &&
mv scorecards svg_scorecards_v3_1950_2023 &&
echo "Preparing scorebooks directory..." &&
mv bound_books pdf_scorecard_archive_v3_1950_2023 &&
echo "Zipping scorecards..." &&
zip -r svg_scorecards_v3_1950_2023.zip svg_scorecards_v3_1950_2023 &&
echo "Zipping scorebooks..." &&
zip -r pdf_scorecard_archive_v3_1950_2023.zip pdf_scorecard_archive_v3_1950_2023 &&
echo "Done.";