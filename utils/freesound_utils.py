import re
import pandas as pd
import os
import traceback
import subprocess
import shlex

parquet_file = "/home/yuchen/raw/freesound/parquet/freesound_parquet.parquet" 
audio_folder = "/fsx/yuchen/freesound" 
log_file = "/home/yuchen/raw/freesound/log.txt"
home = "/home/yuchen/"

# by log file, seems not complete
def notyet_downloaded():

    # read parquet file 
    df = pd.read_parquet(parquet_file)
    all_ids = set(df['id'].tolist())

    downloaded_ids = []

    #read log_file
    with open(log_file, "r") as logf:
        lines = logf.readlines()
        for line in lines:
            downloaded_ids.extend(list(map(lambda s: int(s[11:-3]),re.findall("Downloaded [0-9]* in",line))))

    downloaded_ids = set(downloaded_ids)
    difference = all_ids - downloaded_ids
    return list(difference)
    

def postRegex(tuplle):
    element1 = tuplle[0]
    element2 = tuplle[1]
    result = None
    try:
        result = int(element1)
        return result
    except: 
        pass
    try: 
        result = int(element2)
        return result
    except:
        pass

    return "e"

# By all audio files in "/fsx/yuchen/freesound/"
def notyet_downloaded_by_os():
    ids_infolder = []
    abnormal_names = []

    # read parquet file 
    df = pd.read_parquet(parquet_file)
    all_ids = set(df['id'].tolist())
    
    print("we should have" + str(len(all_ids)) + "audio files")
    # read "/fsx/yuchen/freesound"
    all_files = os.listdir(path = audio_folder)
    file_num = len(all_files)
    for i in range(file_num):
        file_name = all_files[i] 
        liste1 = list(map(postRegex,re.findall(r"(^\d*)-|id =(\d*)\|",file_name)))
        if len(liste1) == 0:
            #print ( f"the {i}eme file's name is abnormal")
            abnormal_names.append(file_name)
        ids_infolder.extend(liste1)
    ids_infolder = set(ids_infolder) 
    print("We have now", len(ids_infolder), "audio files")
    difference = all_ids - ids_infolder
    print("il manqeu", len(difference), "files")
    print("there are", len(abnormal_names), "abnormal files")

    with open("abnormal_names.txt", "a") as ab_file:
        for name in abnormal_names:
            ab_file.write(name+"\n")

    #print(abnormal_names)

    return (difference,abnormal_names)



def failed_ids():

    failed_ids = []

    #read log_file
    with open(log_file, "r") as logf:
        lines = logf.readlines()
        for line in lines:
            failed_ids.extend(list(map(lambda s: int(s),re.findall(r"donwload id = ([0-9]*) failed",line))))

    failed_ids = set(failed_ids)
    print("failed number is", len(failed_ids)) 
    print(failed_ids)
    return failed_ids
    

def modify_filename():
    #step1 : modify abnormal names
#    with open("afterRename.txt", "a") as file:
#        abnormal_names = notyet_downloaded_by_os()[1]
#        for name in abnormal_names:
#            # there are 3 files with strange file name.
#            # so we have to avoid processing them at current stage.
#            try:
#                if name[0] == "i":
#                    ID = re.findall(r"^id(\d*)-",name)[0]
#                    name_after = f"id ={ID}|"+name
#                    #file.write(name_after+"\n")
#                    os.rename(audio_folder+"/"+name,audio_folder+"/"+name_after)
#
#                else:
#                    ID = re.findall(r"^(\d*)__",name)[0]
#                    name_after = f"id ={ID}|"+name
#                    #file.write(name_after+"\n")
#                    os.rename(audio_folder+"/"+name,audio_folder+"/"+name_after)
#            except:
#                traceback.print_exc()
#                continue
#                
#
    #STEP2: modify all those begin with \d*- 
    with open("add_id.txt","a") as f:
        try:
            # read "/fsx/yuchen/freesound"
            all_files = os.listdir(path = audio_folder)
            for name in all_files:
                ID_list = re.findall(r"(^\d*)-",name)
                if len(ID_list) != 0:
                    sound_id = ID_list[0]
                    previous_path = audio_folder+"/"+name
                    if int(sound_id) == 591011: 
                        changed_path = audio_folder+"/"+f"id ={sound_id}| "
                    else:
                        changed_path = audio_folder+"/"+f"id ={sound_id}| "+name
                    f.write(changed_path+"\n")
                    os.rename(previous_path, changed_path)
        except:
                traceback.print_exc(file = f)
    pass

def get_id(file_name):
    try:
        list_id = re.findall(r"id =(\d*)\|",file_name)
        id = int(list_id[0])
        return id
    except:
        print(file_name, "failed")
    
        
    
def duplicated_entry_remove():
    all_files = os.listdir(path = audio_folder)
    all_ids = list(map(get_id,all_files))
    id_dict = {ID:[] for ID in all_ids}

    for name in all_files:
        ID = get_id(name)
        id_dict[ID].append(name)

    with open("duplicate", "a") as f:
        for key,value in id_dict.items():
            if len(value) > 1:
                f.write("duplicate id is:" + str(key)+"\n")
                for i in range(len(value)):
                    f.write(f"the {i}eme duplicate name is:" + value[i] + "\n")
                
    pass

#---------------------------------- zip and upload to S3 --------------------------------------
def zip_freesound(ZIP_SIZE):
    all_files = os.listdir(path = audio_folder)
    all_files.sort(key = get_id)

    n = int(len(all_files) / ZIP_SIZE) + 1
    split = []
    for i in range(n):
        if i == n-1:
            split.append(all_files[(i-1)*ZIP_SIZE:])
        else:
            split.append(all_files[(i-1)*ZIP_SIZE:i*ZIP_SIZE])

    #output: 11 zip files
    for i in range(11):
        command = f"zip freesound{i}a-b?.zip"
        pass
    
    #audio_folder
    # TO BE CONTINUED

#-------------------------------------------------------------------------------------------------

def find_too_long():
    filename_dic = {}
    duration_dic = {}
    liste_long = []
    liste = []
    with open("./too_long.txt", "r") as f:
        string_long = f.read()
        liste = re.findall(r"\(\'(.*?)\', ([0-9]*\.?[0-9]*)\)",string_long)

    for i in range (len(liste)):
        file_name = liste[i][0]
        duration = liste[i][1]
        #if > 10h, we think it is too long and may be a NAN
        if float(duration) < 36000.0:
            break
        filename_dic[i+1] = file_name
        duration_dic[i+1] = duration

def get_total_duration():
    with open("f:\\yuchenxi\\UDEM\\diro\\CLAP\\audio-dataset\\metadata\\freesound\\all_duration.txt", "r") as f:
        string_long = f.read()
        liste = re.findall(r"\(\'(.*?)\', ([0-9]*\.?[0-9]*)\)",string_long)
    total_file = 0
    total_duration = 0
    too_long_number = 0 
    for i in range (len(liste)):
        file_name = liste[i][0]
        duration = liste[i][1]
        seuil = 200*3600.01
        #if > 200h, the audio file is broken
        if float(duration) < seuil:
            total_file += 1
            total_duration += float(duration)  
        else :
            too_long_number += 1

    print("total file is", len(liste))
    print("total file number is", total_file) 
    print("total duration is", total_duration/3600.0)
    print("total too long number is", too_long_number)
    print(str(total_duration/total_file))
    print(str(547830+569))


def find_duration_failed():
    errorLst = []
    with open("duration_log.txt" ,"r") as file:
        lines = file.readlines()
        for line in lines:
            lst = re.findall(r"the error file is:(.*)",line)
            if len(lst) != 0:
                errorLst.append(lst[0])
    print("errors number during Librosa is:",len(errorLst))
    
    with open("filename_dic.txt", "a") as file:
        for i in range(38, 38+len(errorLst)):
            string = str(i) + "  " + errorLst[i-38] + "\n"
            file.write(string)

    
def get_sampling_rate(file_name):
    command = "ffprobe -v error -select_streams a -of default=noprint_wrappers=1:nokey=1 -show_entries stream=sample_rate "

    process = subprocess.run(shlex.split(command+"'"+file_name+"'"), capture_output=True, check=True)

    sampling_rate = float(process.stdout.decode())
    return sampling_rate

#find_duration_failed()
    
if __name__ == "__main__":
    get_total_duration()
        
    #find_too_long()

    #duplicated_entry_remove()
    #zip_freesound(50000)
    #notyet_downloaded_by_os()
    #modify_filename()
    #zip_freesound()

    

