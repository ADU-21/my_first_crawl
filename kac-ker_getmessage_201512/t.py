import urllib.request,re
hack_url = 'http://hac-ker.net/?page=20000'
req = urllib.request.urlopen(hack_url)
html = req.read()
