import pandas as pd
import re

names = [7932, 7959, 7977]

dfs = []

for name in names:
    dfs.append(pd.read_csv('./source/{0}.csv'.format(name), dtype=str))

data32New = []
newData = []
dataByOffer = []

for i in range(len(dfs)):
    offerData = []
    for value in dfs[i]['Zips']:
        offerData.append(i)
        if value not in newData:
            if i == 0:
                data32New.append(value)
                newData.append(value)
            else:
                newData.append(value)

    dataByOffer.append(offerData)
            

file = open('./source/32.txt', 'r')
data = list(file.read().split(', '))
file.close()

unique = open('./output/total.txt', 'r')
uniqueData = list(unique.read().split(', '))
unique.close()


for i in range(len(data)):
    data[i] = re.sub(r'\"', '', data[i])

for i in range(len(uniqueData)):
    uniqueData[i] = re.sub(r'\'', '', uniqueData[i])

# checl differ from old 7932
differ = []

for value in data32New:
    if value not in data:
         differ.append(value)


#add new unique 32 values to new unique total

for val in differ:
    if val not in newData:
        newData.append(val)

differ_2 = []

for dif in newData:
    if dif not in uniqueData:
        differ_2.append(dif)

print(len(differ_2))
first = True

baseString = "insert into ivr_values (ivr, value)\nvalues "

for value in differ_2:
    if first:
        first = False
        baseString += "({0}, '{1}')".format(17, value)

    else:
        baseString += ", ({0}, '{1}')".format(17, value)

    file = open("./output/aster_extra.sql", "w")
    file.write(baseString)
    file.close()