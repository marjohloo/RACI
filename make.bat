pause TURN OFF VIRUS CHECKER OR EXCLUDE FOLDER
rem python -m nuitka --mingw64 --plugin-enable=tk-inter --windows-icon-from-ico=lxr.ico --include-data-file=lxr.ico=lxr.ico --include-data-dir=json=json --onefile violaceum.py
rem cd images
rem magick kat16.png kat20.png kat24.png kat32.png kat40.png kat48.png kat60.png kat72.png kat128.png kat256.png ..\Kat.ico
rem magick avataaars16.png avataaars20.png avataaars24.png avataaars32.png avataaars40.png avataaars48.png avataaars60.png avataaars72.png avataaars128.png avataaars256.png ..\Kat.ico
rem cd ..
rem pyinstaller --clean -w --onefile --icon="Kat.ico" --distpath="dist\Kat" Kat.py
pyinstaller --clean -w --onefile --distpath="dist\RACI" RACI.py
rem copy Kat.pdf dist\Kat
rem copy Kat.ico dist\Kat
copy LICENSE dist\RACI
copy coffee.* dist\RACI
cd dist
"C:\Program Files\7-Zip\7z" a -tzip RACI.zip RACI\
cd ..
pause TURN ON VIRUS CHECKER