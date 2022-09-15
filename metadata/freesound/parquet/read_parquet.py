import pandas as pd

# read freesound_parquet.parquet
metadata_file = r"F:\yuchenxi\UDEM\diro\CLAP\audio-dataset\metadata\freesound\parquet\freesound_parquet.parquet"
df = pd.read_parquet(metadata_file)
pd.to_csv(r"F:\yuchenxi\UDEM\diro\CLAP\CLAP_各个数据集metadatas\freesound\metadata(csv)\freesound_parquet.csv",sep = ",", encode = "utf-8")
print(df.columns)

#tuples = zip(df['id'], df['title'], df["tags:"],df["description"], df["username"], df["download_url"])