import json

with open("F:\\yuchenxi\\UDEM\\diro\\CLAP\\audio-dataset\\utils\\numbers.json", "r") as f:
    numbers = json.load(f)

total_number = 0
total_number_no_audioset = 0

for dataset_name, splits in numbers.items():
    for number in splits.values():
        total_number += number
        if "audioset" != dataset_name:
            total_number_no_audioset += number
        

print(f"total number of train pairs: {total_number}")
print(f"total number of train pairs (without audioset): {total_number_no_audioset}") 