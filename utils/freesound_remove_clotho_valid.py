import pandas as pd

full_csv_path = "F:\\yuchenxi\\UDEM\\diro\\CLAP\\CLAP_各个数据集metadatas\\freesound\\release\\freesound_no_overlap_all.csv"
test_csv_path = "F:\\yuchenxi\\UDEM\\diro\\CLAP\\CLAP_各个数据集metadatas\\freesound\\release\\freesound_no_overlap_test.csv"
train_csv_path = "F:\\yuchenxi\\UDEM\\diro\\CLAP\\CLAP_各个数据集metadatas\\freesound\\release\\freesound_no_overlap_train.csv"

clotho_valid_path = "F:\\yuchenxi\\UDEM\\diro\\CLAP\\CLAP_各个数据集metadatas\\clotho\\clotho_metadata_validation.csv"

print("before")

full_df = pd.read_csv(full_csv_path, encoding="ISO-8859-1")
print(full_df.shape)
test_df = pd.read_csv(test_csv_path, encoding="ISO-8859-1")
print(test_df.shape)
train_df = pd.read_csv(train_csv_path, encoding="ISO-8859-1")
print(train_df.shape)

clotho_valid_df = pd.read_csv(clotho_valid_path, encoding="ISO-8859-1")

clotho_ids = clotho_valid_df["sound_id"].tolist()

for i in range(len(clotho_ids)):
    try:
        clotho_ids[i] = int(clotho_ids[i])
    except:
        clotho_ids[i] = -1
        print("gei ye pa")

# remove entries whose freesound_id is in clotho_ids for the three dataframes

full_df = full_df[~full_df["freesound_id"].isin(clotho_ids)]
test_df = test_df[~test_df["freesound_id"].isin(clotho_ids)]
train_df = train_df[~train_df["freesound_id"].isin(clotho_ids)]

print("after")
print(full_df.shape)
print(test_df.shape)
print(train_df.shape)

full_df.to_csv(full_csv_path[:-4] + "_new.csv" , index=False)
test_df.to_csv(test_csv_path[:-4] + "_new.csv" , index=False)
train_df.to_csv(train_csv_path[:-4] + "_new.csv" , index=False)
