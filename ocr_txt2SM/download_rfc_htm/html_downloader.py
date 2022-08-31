import urllib.request
from urllib.error import URLError
import re

urllist = ['tcp', 'dns', 'icmp', 'tls', 'ssh', 'udp', 'smtp', 'ftp', 'http', 'dhcp', 'ntp', 'bgp', 'nfs', 'nntp', 'ppp', 'arp', 'bootp', 'ip']

with open('protocoltables.html', 'r') as fh:
    lines = fh.readlines()

for line in lines:
    if len(line)<10:
        continue
    matchObj = re.search( r'.*(\"\S+.htm\").*', line)
    if matchObj:
        urllist.append(matchObj.group(1)[1:-5])

urllist = list(set(urllist))
print(len(urllist))

for k in urllist:
    target_url = "https://web.archive.org/web/20210417112354/http://www.networksorcery.com/enp/protocol/{}.htm".format(k)
    try:
        print('trying:', k)
        response = urllib.request.urlopen(target_url)
        html_content = response.read()
     
        with open('downloaded/'+k+'.htm',"wb") as fp:
            fp.write(html_content)
     
    except URLError as e:
        print("Unable to download page: "+str(e.reason))