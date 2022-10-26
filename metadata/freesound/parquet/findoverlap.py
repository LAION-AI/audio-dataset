import pandas as pd
import pickle

usd8k_meta = "F:\\yuchenxi\\UDEM\\diro\\CLAP\\CLAP_各个数据集metadatas\\UrbanSound8K\\UrbanSound8K.csv"
df = pd.read_csv(usd8k_meta,encoding = "ISO-8859-1")

# retrieve fsID and convert to int
usd8k_ids = df["fsID"].tolist()
usd8k_ids = [int(i) for i in usd8k_ids]    
usd8k_list = usd8k_ids 
print(len(usd8k_ids))
usd8k_ids = set(usd8k_ids)
print(len(usd8k_ids))
 
# CLOTHO
clotho_dev_meta = "F:\\yuchenxi\\UDEM\\diro\\CLAP\\CLAP_各个数据集metadatas\\clotho\\clotho_metadata_development.csv"
clotho_eval_meta = "F:\\yuchenxi\\UDEM\\diro\\CLAP\\CLAP_各个数据集metadatas\\clotho\\clotho_metadata_evaluation.csv"
clotho_validation_meta = "F:\\yuchenxi\\UDEM\\diro\\CLAP\\CLAP_各个数据集metadatas\\clotho\\clotho_metadata_validation.csv"

# read the two csv files and retrieve id
clotho_dev = pd.read_csv(clotho_dev_meta,encoding = "ISO-8859-1")
clotho_eval = pd.read_csv(clotho_eval_meta,encoding = "ISO-8859-1")
clotho_val = pd.read_csv(clotho_validation_meta,encoding = "ISO-8859-1")

# retrieve id 
clotho_dev_id = clotho_dev["sound_id"]
# to list
clotho_dev_ids = clotho_dev_id.tolist()
for i in range(len(clotho_dev_ids)):
    try:
        clotho_dev_ids[i] = int(clotho_dev_ids[i])
    except:
        continue

clotho_train_list = clotho_dev_ids

#clotho_dev_ids = set(clotho_dev_ids)
clotho_train_ids = clotho_dev_ids

clotho_eval_ids = clotho_eval['sound_id']
clotho_eval_ids = clotho_eval_ids.tolist()

for i in range(len(clotho_eval_ids)):
    try:
        clotho_eval_ids[i] = int(clotho_eval_ids[i])
    except:
        continue

clotho_test_list = clotho_eval_ids
clotho_eval_ids = set(clotho_eval_ids)
clotho_test_ids = clotho_eval_ids 

clotho_val_ids = clotho_val['sound_id']
clotho_val_ids = clotho_val_ids.tolist()

for i in range(len(clotho_val_ids)):
    try:
        clotho_val_ids[i] = int(clotho_val_ids[i])
    except:
        continue

clotho_val_list = clotho_val_ids
clotho_val_ids = set(clotho_val_ids)




# FSD50K
fsd50k_dev_meta = "F:\\yuchenxi\\UDEM\\diro\\CLAP\\CLAP_各个数据集metadatas\\FSD50K\\FSD50K.ground_truth\\dev.csv"
fsd50k_eval_meta = "F:\\yuchenxi\\UDEM\\diro\\CLAP\\CLAP_各个数据集metadatas\\FSD50K\\FSD50K.ground_truth\\eval.csv"
# read the two csv files 
fsd50k_dev = pd.read_csv(fsd50k_dev_meta,encoding = "ISO-8859-1")
fsd50k_eval = pd.read_csv(fsd50k_eval_meta,encoding = "ISO-8859-1")
# check "split" column in dev.csv, separate split "train" and "val"
fsd50k_dev_train = fsd50k_dev[fsd50k_dev["split"] == "train"]
fsd50k_dev_val = fsd50k_dev[fsd50k_dev["split"] == "val"]
# retrieve filename and convert to list of int
fsd50k_train_list = fsd50k_dev_train["fname"].astype(int).tolist()
fsd50k_train_ids = set(fsd50k_train_list)
fsd50k_val_list = fsd50k_dev_val["fname"].astype(int).tolist()
fsd50k_val_ids = set(fsd50k_val_list)
fsd50k_test_list = fsd50k_eval["fname"].astype(int).tolist()
fsd50k_eval_ids = set(fsd50k_test_list)
fsd50k_test_ides = fsd50k_eval_ids

print("kaibai")
# MACS no relation with freesound neither audioset

# freesound  

freesound_meta_file = "F:\\yuchenxi\\UDEM\\diro\\CLAP\\audio-dataset\\metadata\\freesound\\parquet\\freesound_parquet.parquet"
df = pd.read_parquet(freesound_meta_file)
freesound_ids = set(df['id'].tolist())
for id in freesound_ids:
    print(type(id))
    break
#print(df.columns)
#print(df.columns)
#tuples = zip(df['id'], df['title'], df["tags:"],df["description"], df["username"], df["download_url"])

# audioset
audioset_unbalanced_meta_file = "F:\\yuchenxi\\UDEM\\diro\\CLAP\\CLAP_各个数据集metadatas\\AudioSet\\unbalanced_train_segments.csv"
audioset_balanced_meta_file = "F:\\yuchenxi\\UDEM\\diro\\CLAP\\CLAP_各个数据集metadatas\\AudioSet\\balanced_train_segments.csv"
audioset_eval_meta_file = "F:\\yuchenxi\\UDEM\\diro\\CLAP\\CLAP_各个数据集metadatas\\AudioSet\\eval_segments.csv"

with open(audioset_unbalanced_meta_file, 'r') as f:
    lines = f.readlines()

lines = lines[3:]
header_list = ['YTID', 'start_seconds', 'end_seconds', 'positive_labels']
class_metadata = [l.strip().split(', ') for l in lines]
unbalanced_metadata = pd.DataFrame(class_metadata, columns=header_list)

with open(audioset_balanced_meta_file, 'r') as f:
    lines = f.readlines()

lines = lines[3:]
header_list = ['YTID', 'start_seconds', 'end_seconds', 'positive_labels']
class_metadata = [l.strip().split(', ') for l in lines]
balanced_metadata = pd.DataFrame(class_metadata, columns=header_list)

with open(audioset_eval_meta_file, 'r') as f:
    lines = f.readlines()

lines = lines[3:]
header_list = ['YTID', 'start_seconds', 'end_seconds', 'positive_labels']
class_metadata = [l.strip().split(', ') for l in lines]
eval_metadata = pd.DataFrame(class_metadata, columns=header_list)

# unbalanced
unbalanced_train_list = unbalanced_metadata['YTID'].tolist() 
unbalanced_train_ids = set(unbalanced_train_list)
# balanced
balanced_train_list = balanced_metadata['YTID'].tolist()
balanced_train_ids = set(balanced_train_list)
# eval 
audioset_eval_list = eval_metadata['YTID'].tolist()
audioset_eval_ids = set(audioset_eval_list)


# esc50 
esc_df = pd.read_csv("F:\\yuchenxi\\UDEM\\diro\\CLAP\\CLAP_各个数据集metadatas\\ESC50\\esc50.csv")
esc_freesound_list = esc_df["src_file"].astype(int).tolist()
esc_freesound_ids = set(esc_df['src_file'].astype(int).tolist())

# #esc50
# #esc50 in clotho train
# esc50_in_clotho_train = len(esc_freesound_ids.intersection(clotho_train_ids))
# print("esc50_in_clotho_train: ", esc50_in_clotho_train)
# #esc50 in clotho val
# esc50_in_clotho_val = len(esc_freesound_ids.intersection(clotho_val_ids))
# print("esc50_in_clotho_validation: ", esc50_in_clotho_val)
# #esc50 in clotho test
# esc50_in_clotho_test = len(esc_freesound_ids.intersection(clotho_test_ids))
# print("esc50_in_clotho_test: ", esc50_in_clotho_test)

# #esc50 in fsd50k train
# esc50_in_fsd50k_train = len(esc_freesound_ids.intersection(fsd50k_train_ids))
# print("esc50_in_fsd50k_train: ", esc50_in_fsd50k_train)
# #esc50 in fsd50k val
# esc50_in_fsd50k_val = len(esc_freesound_ids.intersection(fsd50k_val_ids))
# print("esc50_in_fsd50k_validation: ", esc50_in_fsd50k_val)
# #esc50 in fsd50k test
# esc50_in_fsd50k_test = len(esc_freesound_ids.intersection(fsd50k_test_ides))
# print("esc50_in_fsd50k_test: ", esc50_in_fsd50k_test)

# # fsd50k train in clotho test
# fsd50k_train_in_clotho_test = len(fsd50k_train_ids.intersection(clotho_test_ids))
# print("fsd50k_train_in_clotho_test: ", fsd50k_train_in_clotho_test)

# # clotho train in fsd50k test
# clotho_train_in_fsd50k_test = len(clotho_train_ids.intersection(fsd50k_test_ides))
# print("clotho_train_in_fsd50k_test: ", clotho_train_in_fsd50k_test)

# # usd8k in clotho train
# # usd8k in clotho val
# # usd8k in clotho test
# usd8k_in_clotho_train = len(usd8k_ids.intersection(clotho_train_ids))
# print("usd8k_in_clotho_train: ", usd8k_in_clotho_train)
# usd8k_in_clotho_val = len(usd8k_ids.intersection(clotho_val_ids))
# print("usd8k_in_clotho_validation: ", usd8k_in_clotho_val)
# usd8k_in_clotho_test = len(usd8k_ids.intersection(clotho_test_ids))
# print("usd8k_in_clotho_test: ", usd8k_in_clotho_test)
# # usd8k in fsd50k train
# # usd8k in fsd50k val
# # usd8k in fsd50k test
# usd8k_in_fsd50k_train = len(usd8k_ids.intersection(fsd50k_train_ids))
# print("usd8k_in_fsd50k_train: ", usd8k_in_fsd50k_train)
# usd8k_in_fsd50k_val = len(usd8k_ids.intersection(fsd50k_val_ids))
# print("usd8k_in_fsd50k_validation: ", usd8k_in_fsd50k_val)
# usd8k_in_fsd50k_test = len(usd8k_ids.intersection(fsd50k_test_ides))
# print("usd8k_in_fsd50k_test: ", usd8k_in_fsd50k_test)




# # make a black list for esc50: all overlaps with fsd50k and clotho
# # step1 : get all freesound ids in fsd50k and clotho (union)
# fsd50k_clotho_freesound_ids = fsd50k_train_ids.union(fsd50k_val_ids).union(fsd50k_test_ides).union(clotho_train_ids).union(clotho_val_ids).union(clotho_test_ids)
# # difference between freesound ids in esc50 and freesound ids in fsd50k and clotho

# esc50_pure = esc_freesound_ids.difference(fsd50k_clotho_freesound_ids)  
# usd8k_pure = usd8k_ids.difference(fsd50k_clotho_freesound_ids) 
# print("esc50_pure: ", len(esc50_pure))
# print("usd8k_pure: ", len(usd8k_pure))
# print("esc50_original: ", len(esc_freesound_ids))
# print("usd8k_original: ", len(usd8k_ids))

# with open("F:\\yuchenxi\\UDEM\\diro\\CLAP\\CLAP_各个数据集metadatas\\freesound\\reprocess_freesound\\esc_pure.pkl","wb") as f:
#     pickle.dump(esc50_pure, f)

# with open("F:\\yuchenxi\\UDEM\\diro\\CLAP\\CLAP_各个数据集metadatas\\freesound\\reprocess_freesound\\usd8k_pure.pkl","wb") as f:
#     pickle.dump(usd8k_pure, f)



# audiocaps
audiocaps_train_meta = "F:\\yuchenxi\\UDEM\\diro\\CLAP\\CLAP_各个数据集metadatas\\audiocaps\\audiocaps\\dataset\\train.csv"
audiocaps_eval_meta = "F:\\yuchenxi\\UDEM\\diro\\CLAP\\CLAP_各个数据集metadatas\\audiocaps\\audiocaps\\dataset\\test.csv"
audiocaps_val_meta = "F:\\yuchenxi\\UDEM\\diro\\CLAP\\CLAP_各个数据集metadatas\\audiocaps\\audiocaps\\dataset\\val.csv"

# read the three csv files
audiocaps_train = pd.read_csv(audiocaps_train_meta,encoding = "ISO-8859-1")
audiocaps_eval = pd.read_csv(audiocaps_eval_meta,encoding = "ISO-8859-1")
audiocaps_vall = pd.read_csv(audiocaps_val_meta,encoding = "ISO-8859-1")

# retrieve youtube_id and convert to list 
audiocaps_train_ids = audiocaps_train['youtube_id'].tolist()
audiocaps_eval_ids = audiocaps_eval['youtube_id'].tolist()
audiocaps_val_ids = audiocaps_vall['youtube_id'].tolist()

#list
audiocaps_train_list = audiocaps_train_ids
audiocaps_eval_list = audiocaps_eval_ids
audiocaps_val_list = audiocaps_val_ids

# convert to set
audiocaps_train_ids = set(audiocaps_train_ids)
audiocaps_eval_ids = set(audiocaps_eval_ids)
# print("audiocaps_eval_len",len(audiocaps_eval_ids))
# print("audiocaps_train_len",len(audiocaps_train_ids))


# audiocaps train in audioset test
# audiocaps_train_in_audioset_test = len(audiocaps_train_ids.intersection(audioset_eval_ids))
# print("audiocaps_train_in_audioset_test: ", audiocaps_train_in_audioset_test)

# # audioset unbalanced train in audiocaps test
# audioset_unbalanced_train_in_audiocaps_test = len(unbalanced_train_ids.intersection(audiocaps_eval_ids))
# print("audioset_unbalanced_train_in_audiocaps_test: ", audioset_unbalanced_train_in_audiocaps_test)


# below we just calculate the overlap between lists, not sets
print("--------------------------------------------------")
print("--------------------------------------------------")
print(" sample numbers!")
print("--------------------------------------------------")
print("--------------------------------------------------")

# esc50 in fsd50k train
# esc50 in fsd50k val
# esc50 in fsd50k test
esc50_in_fsd50k_train = len([i for i in esc_freesound_list if i in fsd50k_train_list])
print("esc50_in_fsd50k_train: ", esc50_in_fsd50k_train)
esc50_in_fsd50k_val = len([i for i in esc_freesound_list if i in fsd50k_val_list])
print("esc50_in_fsd50k_validation: ", esc50_in_fsd50k_val)
esc50_in_fsd50k_test = len([i for i in esc_freesound_list if i in fsd50k_test_list])
print("esc50_in_fsd50k_test: ", esc50_in_fsd50k_test)

#esc50 in clotho train
#esc50 in clotho val
#esc50 in clotho test
esc50_in_clotho_train = len([i for i in esc_freesound_list if i in clotho_train_list])
print("esc50_in_clotho_train: ", esc50_in_clotho_train)
esc50_in_clotho_val = len([i for i in esc_freesound_list if i in clotho_val_list])
print("esc50_in_clotho_validation: ", esc50_in_clotho_val)
esc50_in_clotho_test = len([i for i in esc_freesound_list if i in clotho_test_list])
print("esc50_in_clotho_test: ", esc50_in_clotho_test)

# usd8k in fsd50k train
# usd8k in fsd50k val
# usd8k in fsd50k test
usd8k_in_fsd50k_train = len([i for i in usd8k_list if i in fsd50k_train_list])
print("usd8k_in_fsd50k_train: ", usd8k_in_fsd50k_train)
usd8k_in_fsd50k_val = len([i for i in usd8k_list if i in fsd50k_val_list])
print("usd8k_in_fsd50k_validation: ", usd8k_in_fsd50k_val)
usd8k_in_fsd50k_test = len([i for i in usd8k_list if i in fsd50k_test_list])
print("usd8k_in_fsd50k_test: ", usd8k_in_fsd50k_test)

# usd8k in clotho train
# usd8k in clotho val
# usd8k in clotho test
usd8k_in_clotho_train = len([i for i in usd8k_list if i in clotho_train_list])
print("usd8k_in_clotho_train: ", usd8k_in_clotho_train)
usd8k_in_clotho_val = len([i for i in usd8k_list if i in clotho_val_list])
print("usd8k_in_clotho_validation: ", usd8k_in_clotho_val)
usd8k_in_clotho_test = len([i for i in usd8k_list if i in clotho_test_list])
print("usd8k_in_clotho_test: ", usd8k_in_clotho_test)

# clotho test in fsd50k train
clotho_test_in_fsd50k_train = len([i for i in clotho_test_list if i in fsd50k_train_list])
print("clotho_test_in_fsd50k_train: ", clotho_test_in_fsd50k_train)

# clotho test in fsd50k val
clotho_test_in_fsd50k_val = len([i for i in clotho_test_list if i in fsd50k_val_list])
print("clotho_test_in_fsd50k_validation: ", clotho_test_in_fsd50k_val)

# clotho test in fsd50k test
clotho_test_in_fsd50k_test = len([i for i in clotho_test_list if i in fsd50k_test_list])
print("clotho_test_in_fsd50k_test: ", clotho_test_in_fsd50k_test)

# fsd50k test in clotho train
fsd50k_test_in_clotho_train = len([i for i in fsd50k_test_list if i in clotho_train_list])
print("fsd50k_test_in_clotho_train: ", fsd50k_test_in_clotho_train)

# fsd50k test in clotho val
fsd50k_test_in_clotho_val = len([i for i in fsd50k_test_list if i in clotho_val_list])
print("fsd50k_test_in_clotho_validation: ", fsd50k_test_in_clotho_val)

# fsd50k test in clotho test
fsd50k_test_in_clotho_test = len([i for i in fsd50k_test_list if i in clotho_test_list])
print("fsd50k_test_in_clotho_test: ", fsd50k_test_in_clotho_test)

# clotho val in fsd50k train
clotho_val_in_fsd50k_train = len([i for i in clotho_val_list if i in fsd50k_train_list])
print("clotho_val_in_fsd50k_train: ", clotho_val_in_fsd50k_train)

# clotho val in fsd50k val
clotho_val_in_fsd50k_val = len([i for i in clotho_val_list if i in fsd50k_val_list])
print("clotho_val_in_fsd50k_validation: ", clotho_val_in_fsd50k_val)

# clotho val in fsd50k test
clotho_val_in_fsd50k_test = len([i for i in clotho_val_list if i in fsd50k_test_list])
print("clotho_val_in_fsd50k_test: ", clotho_val_in_fsd50k_test)

# fsd50k val in clotho train
fsd50k_val_in_clotho_train = len([i for i in fsd50k_val_list if i in clotho_train_list])
print("fsd50k_val_in_clotho_train: ", fsd50k_val_in_clotho_train)

# fsd50k val in clotho val
fsd50k_val_in_clotho_val = len([i for i in fsd50k_val_list if i in clotho_val_list])
print("fsd50k_val_in_clotho_validation: ", fsd50k_val_in_clotho_val)




# audiocaps test in audioset unbalanced train
audiocaps_test_in_audioset_unbalanced_train = len([i for i in audiocaps_eval_list if i in unbalanced_train_list])
print("audiocaps_test_in_audioset_unbalanced_train: ", audiocaps_test_in_audioset_unbalanced_train)

# audiocaps test in audioset balanced train
audiocaps_test_in_audioset_balanced_train = len([i for i in audiocaps_eval_list if i in balanced_train_list])
print("audiocaps_test_in_audioset_balanced_train: ", audiocaps_test_in_audioset_balanced_train)

# audiocaps test in audioset eval
audiocaps_test_in_audioset_eval = len([i for i in audiocaps_eval_list if i in audioset_eval_list])
print("audiocaps_test_in_audioset_eval: ", audiocaps_test_in_audioset_eval)

# audioset evaluation in audiocaps train
audioset_eval_in_audiocaps_train = len([i for i in audioset_eval_list if i in audiocaps_train_list])
print("audioset_eval_in_audiocaps_train: ", audioset_eval_in_audiocaps_train)

# audioset evaluation in audiocaps val
audioset_eval_in_audiocaps_val = len([i for i in audioset_eval_list if i in audiocaps_val_list])
print("audioset_eval_in_audiocaps_validation: ", audioset_eval_in_audiocaps_val)
















