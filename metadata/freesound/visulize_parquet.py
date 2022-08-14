
import pandas as pd

parquet_file = "f:\\yuchenxi\\UDEM\\diro\\CLAP\\audio-dataset\\metadata\\freesound\\parquet\\freesound_parquet.parquet" 
df = pd.read_parquet(parquet_file)

df1 = df.loc[0:1000 ["tags", "description"]]
i = 0
for tag, description in zip (df1["tags"], df1["description"]):
    print(i)
    print("tags are: ",tag)
    print("description is",description)

