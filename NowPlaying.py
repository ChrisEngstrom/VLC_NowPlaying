#!/usr/bin/env python
#===============================================================================
# title           :NowPlaying.py
# description     :This script will create a NowPlaying.txt file that contains
#                   the info for the song that is currently being played via VLC
# author          :Tipher88
# contributors    :AbyssHunted, Etuldan
# date            :20190227
# version         :1.7.0
# usage           :python NowPlaying.py
# notes           :For this script to work you need to follow the instructions
#                   in the included README.txt file
# python_version  :2.7.10 & 3.4.3
#===============================================================================

import sys, os, time, datetime, requests, codecs
import xml.etree.ElementTree as ET

# Global variable to keep track of what version of python is running
pythonVersion = 0

if sys.version_info[0] > 2:
    # Python 3 or greater
    pythonVersion = 3
    from html.parser import HTMLParser
else:
    # Python 2.6-2.7
    pythonVersion = 2
    from HTMLParser import HTMLParser

    
# Global variable to keep track of song info being printed and check for changes
currentSongInfo = ''

def getInfo():
    # CUSTOM: Separator can be changed to whatever you want
    separator = u'   |   '
    
    nowPlaying = u'UNKNOWN'
    songTitle = u'UNKNOWN'
    songArtist = u'UNKNOWN'
    fileName = u''

    s = requests.Session()
    
    # CUSTOM: Username is blank, just provide the password
    s.auth = ('', 'password')
    
    # Attempt to retrieve song info from the web interface
    try:
        r = s.get('http://localhost:8080/requests/status.xml', verify=False)
        
        if('401 Client error' in r.text):
            print('Web Interface Error: Do the passwords match as described in the README.txt?')
            return
    except:
        print('Web Interface Error: Is VLC running? Did you enable the Web Interface as described in the README.txt?')
        return

    # Okay, now we know we have a response with our xml data in it
    # Save the xml element tree response data
    parser = ET.XMLParser(encoding="utf-8")
    root = ET.fromstring(r.content, parser=parser)
    
    # Only update when the player is playing or when we don't already have the song information
    if(root.find('state').text == "playing" or
       currentSongInfo == ''):
        # Loop through all metadata info nodes to find relevant metadata
        for info in root.findall("./information/category[@name='meta']/info"):
            # Save the name attribute of the info node
            name = info.get('name')
            
            # See if the info node we are looking at is now_playing
            if(name == 'now_playing'):
                nowPlaying = removeBOM(info.text)
            else:
                # See if the info node we are looking at is for the artist
                if(name == 'artist'):
                    songArtist = removeBOM(info.text)
                
                # See if the info node we are looking at is for the title
                if(name == 'title'):
                    songTitle = removeBOM(info.text)
                
                # See if the info node we are looking at is for the filename
                if(name == 'filename'):
                    fileName = info.text
                    fileName = removeBOM(os.path.splitext(fileName)[0])
        # END: for info in root.findall("./information/category[@name='meta']/info")
        
        # If the now_playing node exists we should use that and ignore the rest
        if(nowPlaying != 'UNKNOWN'):
            writeSongInfoToFile(nowPlaying, separator)
        else:
            # Make sure a songTitle and songArtist were found in the metadata
            if(songTitle != 'UNKNOWN' and
               songArtist != 'UNKNOWN'):
                # Both songTitle and song Artist have been set so use both
                titleAndArtist = ('%s - %s' % (songTitle, songArtist))
                writeSongInfoToFile(titleAndArtist, separator)
            elif( songTitle != 'UNKNOWN' ):
                # Just use the songTitle
                writeSongInfoToFile(songTitle, separator)
            elif( fileName != '' ):
                # Use the fileName as a last resort
                writeSongInfoToFile(fileName, separator)
            else:
                # This should print 'UNKNOWN - UNKNOWN' because no relevant metadata was
                #   found
                writeSongInfoToFile('%s - %s' % (songTitle, songArtist), separator)
# END: getInfo()

def writeSongInfoToFile( songInfo, separator ):
    global currentSongInfo
    htmlParser = HTMLParser()
    
    if(currentSongInfo != songInfo):
        if(pythonVersion > 2):
            currentSongInfo = songInfo
        else:
            currentSongInfo = unicode(songInfo.encode('utf-8'), 'utf-8-sig')
        
        safeprint(htmlParser.unescape(currentSongInfo))
    
        # CUSTOM: The output file name can be changed
        textFile = codecs.open('NowPlaying.txt', 'w', encoding='utf-8', errors='ignore')
        textFile.write(htmlParser.unescape(currentSongInfo + separator))
        textFile.close()
        
        timeStamp = '{:%H:%M:%S}'.format(datetime.datetime.now())
    
        # CUSTOM: The output file name can be changed
        textFile = codecs.open('NowPlaying_History.txt', 'a', encoding='utf-8', errors='ignore')
        textFile.write(htmlParser.unescape(('%s: %s%s') % (timeStamp, currentSongInfo, os.linesep)))
        textFile.close()
# END: writeSongInfoToFile( songInfo, separator )

def removeBOM(s):
    result = u''

    # Check for python v2 string
    if (sys.version_info < (3,) and
        isinstance(s, str)):
        # Remove possible BOM and return unicode
        result = unicode(s.encode('utf-8'), 'utf-8-sig')
    else:
        result = s
    
    return result
# END: removeBOM(s)

def safeprint(s):
    try:
        print(s)
    except UnicodeEncodeError:
        if sys.version_info >= (3,):
            print(s.encode('utf-8').decode(sys.stdout.encoding))
        else:
            print(s.encode('utf-8').decode(sys.stdout.encoding))
# END: safeprint(s)

if __name__ == '__main__':
    while 1:
        getInfo()
        
        # CUSTOM: Sleep for a number of seconds before checking again
        time.sleep(5)
# END: if __name__ == '__main__'