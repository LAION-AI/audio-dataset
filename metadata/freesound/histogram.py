import matplotlib.pyplot as plt
from matplotlib import colors
from matplotlib.ticker import PercentFormatter
import re
import math



filename_dic = {}
duration_dic = {}
liste = []
all_times = []
lq10 = []
lq1 = []
lq200 = []
logg = []

over3min = 0
over5min = 0
over10min = 0
between200300 = 0
with open("f:\\yuchenxi\\UDEM\\diro\\CLAP\\audio-dataset\\metadata\\freesound\\all_duration.txt", "r") as f:
    string_long = f.read()
    liste = re.findall(r"\(\'(.*?)\', ([0-9]*\.?[0-9]*)\)",string_long)

for i in range (len(liste)):
    file_name = liste[i][0]
    duration = float(liste[i][1])/60         #unity : minute
    #if > 10h, we think it is too long and may be a NAN
    if duration < 200*60 + 60:
        lq200.append(duration)
        if duration > 3:
            over3min += 1 
        if duration > 5:
            over5min += 1
        if duration > 10:
            over10min += 1

    if duration < 60.1:
        if duration < 10:
            lq10.append(duration)
        if duration < 1:
            lq1.append(duration)
        all_times.append(duration)


###########3-------------figure==============
n_bins = 60

fig, axs = plt.subplots(1, 1)

#axs[0].hist(all_times, bins=n_bins)
#axs[1].hist(lq10, bins=n_bins)
#axs.hist(lq200, bins=100, range = (100,12000))
axs.hist(lq200, bins=100, log = True)
print("over3min:",over3min)
print("over5min:",over5min)
print("between200300:",between200300)

print("over3min_percentage:",over3min/len(lq200))
print("over5min_percentage:",over5min/len(lq200))
print("over10min_percentage:",over10min/len(lq200))
plt.show()