#from __future__ import unicode_literals
import subprocess
import sys, os
import youtube_dl

def downloadSongFromYoutube(y):
	BASIC="https://www.youtube.com/results?search_query="
	QUERY="THING+I+WANTED+TO+SEARCH"
	
	QUERY=y.replace(" ", "+")
	QUERY=QUERY.replace("&","+")
	
	p = subprocess.Popen('wget ' + BASIC+QUERY + ' -q -O -', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	results = ""
	for line in p.stdout.readlines():
			
		if "yt-lockup-title" in line:
			results=line.split("yt-lockup-title")[1]
			results=results.split("href=")[1]
			results=results.split(" ")[0]
			results = results.split("\"")[1]
			break;
	
	retval = p.wait()
	
	BASIC="https://www.youtube.com"
	if(results != ""):
		request=BASIC+results
		print request
		downloadPlaylist(request);

def downloadPlaylist(request):
	# give a directory name as the second argument
	print "The url is " + request;
	ydl_opts = {
    		'format': 'bestaudio/best',
   		    'postprocessors': [{
        		'key': 'FFmpegExtractAudio',
        		'preferredcodec': 'mp3',
        		'preferredquality': '192',
    		}],
	}
	with youtube_dl.YoutubeDL(ydl_opts) as ydl:
	    ydl.download([request])

	print "Download complete\n";
