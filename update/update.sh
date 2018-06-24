cd ..
mv apikey.txt ..
mv apikey_weather.txt ..
mv client_secret.json ..
mv credentials.json ..
cd ..

rm -rf ./SmartMirror
git clone 'https://github.com/JasonLeviGoodison/SmartMirror'

mv ./apikey.txt SmartMirror
mv ./apikey_weather.txt SmartMirror
mv ./client_secret.json SmartMirror
mv ./credentials.json SmartMirror

cd SmartMirror/
python main.py & python gui.py

