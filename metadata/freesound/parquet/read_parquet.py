import pandas as pd
import glob

# read freesound_parquet.parquet
file_list = glob.glob(r'F:\yuchenxi\UDEM\diro\CLAP\audio-dataset\metadata\Epidemic_sound(sound effects)/**/*.parquet', recursive=True)
#metadata_file = r"F:\yuchenxi\UDEM\diro\CLAP\audio-dataset\metadata\freesound\parquet\freesound_parquet.parquet"
total_entry = 0
for file in file_list:
    df = pd.read_parquet(file)
    total_entry += len(df)
# df = pd.read_parquet(metadata_file)
# pd.to_csv(r"F:\yuchenxi\UDEM\diro\CLAP\CLAP_各个数据集metadatas\freesound\metadata(csv)\freesound_parquet.csv",sep = ",", encode = "utf-8")
print(total_entry)

#tuples = zip(df['id'], df['title'], df["tags:"],df["description"], df["username"], df["download_url"])