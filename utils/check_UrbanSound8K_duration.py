import pandas as pd
import os

df = pd.read_csv("/home/yuchen/raw_dataset/UrbanSound8K/UrbanSound8K/metadata/UrbanSound8K.csv")
total_time = 0
df_time = df.loc[:,["start","end","class"]].groupby("class").aggregate("sum")
for classLabel, row in df_time.iterrows():
#    print (classLabel, "duration is: ", f'{(row.end-row.start)/3600:.2f}', "hours")
    total_time += row.end - row.start
# print("Total duration is: ", f'{total_time/3600:.2f}', "hours")
# print("--------------------------------------------")
result1 = df.loc[:,["start","class"]].groupby("class").aggregate("count")
print(result1)
