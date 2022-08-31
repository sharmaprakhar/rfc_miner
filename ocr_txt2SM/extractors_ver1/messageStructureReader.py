


def get_cases_indices(l):
  cases = []
  indices = []
  i = 0
  cont = True
  while cont:
    i = l.find('\\', i)
    if i == -1:
      cont = False
      break
    if l[i-1] == '-':
      cases.append([cases.pop(), lines[0][:i].count('+') - 1])
    else:
      indices.append(i)
      cases.append(lines[0][:i].count('+') - 1)
    i += 1
  
  return cases, indices



def find_texts(box, indices):
  texts = [''] * len(indices)
  for l in box[1:]:
    for k in range(len(indices)):
      i = indices[k]
      if i == -1:
        continue
      if any( not c.isspace() for c in l[i:i+6]):
        j = l[i:i+6].find(l[i:i+6].strip())
        if l[i+j].isalnum():
          s = i+j
          e = i+j
          while not l[s-2:s].isspace():
            s -= 1
          while not l[e:e+2].isspace():
            e += 1
          texts[k] += ' ' + l[s:e]
        indices[k] = i + j
      else:
        indices[k] = -1

  return texts



def fill_cases(res, cases, texts):
  for k in range(len(cases)):
    if type(cases[k]) == list:
      for j in range(cases[k][0],cases[k][1]+1):
          a, b = res[j]
          a += texts[k]
          res[j] = (a,b)
    else:
      a, b = res[cases[k]]
      a += texts[k]
      res[cases[k]] = (a,b)



def follow_lines(box, res):
  ## Get the cases to fill
  cases, indices = get_cases_indices(box[0])

  ## Follow the \ to the text
  texts = find_texts(box, indices)

  ## fill the cases
  fill_cases(res, cases, texts)
  
  return res



msg = open("msgSamples/msgSample2.txt", "r")


lines = msg.readlines()

#How many bits?
if any(c.isnumeric() for c in lines[1]) and any(c.isnumeric() for c in lines[0]):
  numBits = len(lines[1].split())
  charByBits = (len(lines[1].strip()) - 1 ) / ( numBits - 1 )
elif any(c.isnumeric() for c in lines[0]):
  numBits = len(lines[0].split())
  charByBits = (len(lines[0].strip()) - 1 ) / ( numBits - 1 )
else:
  numBits = 'unknown'
  charByBits = -1

print('Number of bits:', numBits, "Char by bits:", charByBits)


boxes=[]
box=[]

#Get the boxes
for line in lines:
  if len(line.split()) == 1:
    boxes.append(box)
    box=[]
  else:
    box.append(line)


words = ['nbs']
bits=[]
res=[]

for b in range(1, len(boxes)):
  row = boxes[b]
  nl=0
  w=''
  words=[]

  for l in row:
    
    if l.strip()[0] == '|':
      nl += 1
    
    if any(c.isalpha() for c in l):
      
      if l.strip()[0] == '/':
        res.append((l.strip('\n| /'), 'undefined'))
        break

      strippedLine = l.strip('\n ').split('|')
      strippedLine.pop()
      strippedLine.pop(0)


      if len(strippedLine) > 1:
        if words == []:
          words = strippedLine
        else:
          words = [ words[i] + ' ' + strippedLine[i].strip() for i in range(len(strippedLine))]
      
      w = w + ' ' + l.strip('\n| /')

  else:
    if words != []:
      for item in words:
        if charByBits == -1:
          res.append((item.strip(), 1))
        else:
          res.append((item.strip(), (len(item) + 1) / charByBits))
    else:
      res.append((w.strip(), nl * numBits))


if box != []:
  res = follow_lines(box,res)

print('Result:', res)
