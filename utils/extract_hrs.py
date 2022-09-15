import re

hours = []
with open('./trace.txt') as f:
    lines = f.readlines()
    for line in lines:
        hours.extend(list(re.findall(r"\d*\.\d\d",line)))

hours = list(map(lambda x:float(x), hours))
with open("./result", "a") as f:
    f.write("TOOOOOOOTAL TIMEEEEEEEISSSSSSSSSSSS", str(sum(hours)))
print("TOOOOOOOTAL TIMEEEEEEEISSSSSSSSSSSS", str(sum(hours)))