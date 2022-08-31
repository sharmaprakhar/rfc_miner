
import numpy as np

#f = open("siprfc.txt", "r")

# f = open("../rfcs/rfc1002.txt", "r") #TCP

#f = open("../rfcs/rfc2616.txt", "r") #HTTP
#f = open("../rfcs/rfc1034.txt", "r") #DNS
#f = open("../rfcs/rfc1035.txt", "r") #DNS
#f = open("../rfcs/rfc5246.txt", "r") #TLS
#f = open("../rfcs/rfc3659.txt", "r") #FTP
#f = open("../rfcs/rfc959.txt", "r") #FTP

# rfc = input("RFC number: ")
# f = open("../rfcs/rfc"+rfc+".txt", "r")
f = open("/Users/e32414/Downloads/MQTT_proxy.txt", "r")



def countWhites(line):
  w=[]
  for i in range(len(line)):
    if line[i] == ' ':
      if i != 0 and line[i-1] == ' ':
        w[-1] += 1
      else:
        w.append(1)
  return w



lines = f.readlines()
indexes = []

for k in range(len(lines)):
  line = lines[k]
  if '--' in line:
    indexes.append(k)
  
pragraphs = []

for i in indexes:
  start = i
  end = i
  line = lines[i]

  while line != '\n':
    start -= 1
    line = lines[start]

  line = lines[i]
  while line != '\n':
    end += 1
    line = lines[end]

  pragraphs.append([start,end])

cleanlist = []
for x in pragraphs:
  if x not in cleanlist:
    cleanlist.append(x)


# Now that we have the paragraphs, we have to sort them
scores=[]

## Score1
## variance of whitespaces number at the lines begining
for para in cleanlist:
  whitespaces = []
  for line in lines[para[0]+1:para[1]]:
    whitespaces.append(countWhites(line)[0])
  scores.append(np.var(whitespaces))

## Score 2
## look for table lines == identical lines

for i in range(len(cleanlist)):
  para=cleanlist[i]
  nbmax = 0
  for l1 in lines[para[0]+1:para[1]]:
    nb = 0
    for l2 in lines[para[0]+1:para[1]]:
      if l1==l2:
        nb += 1
    if nb > nbmax:
      nbmax = nb
  if nbmax > (para[1] - para[0]) / 4 and para[1] - para[0] > 4:
    scores[i] -= 1000



## Score 3
## Getting the captions and looking for keywords
keywords=['Figure', 'example', 'flow', 'structure', 'message']
captions=[]
for i in range(len(cleanlist)):
  para=cleanlist[i]
  captions.append(lines[para[1]+1])
  for keyword in keywords:
    if keyword in captions[i]:
      scores[i] -= 100



# Print ordered by scores
order = np.argsort(scores)
for i in order:
  print('score:\t\t', scores[i])
  print('line:\t\t', cleanlist[i][0])
  print('caption:', captions[i])
  for line in lines[cleanlist[i][0]:cleanlist[i][1]+1]:
    print(line[:-1])
  print('<============>')