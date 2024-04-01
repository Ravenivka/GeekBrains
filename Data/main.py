import random
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt


lst = ['robot'] * 10
lst += ['human'] * 10
random.shuffle(lst)
data = pd.DataFrame({'whoAmI':lst})
data.head()
#print(data)

data_set = set(data['whoAmI'])

frame = pd.DataFrame()
for x in data_set:
    lst = [int(data['whoAmI'][i] == x) for i in range(len(data))]    
    frame[x] = lst
print(frame)

#indexis = [i for i in range(len(frame))]
#frame['index'] = indexis
#sns.barplot(x='index', y='robot', data=frame)

#plt.show()
