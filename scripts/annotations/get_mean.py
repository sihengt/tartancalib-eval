import os
import pandas as pd

RESULTS_FILEPATH = "/home/siheng/Documents/Calibration/ICRA2023/corner-accuracy/results"

csv_files = os.listdir(RESULTS_FILEPATH)
csv_files.sort()

data = {}
index = ["kalibr", "tartan"]
print(csv_files)
for file in csv_files:
    dataset = file.split("_")[0]
    if dataset not in data:
        data[dataset] = []
    df = pd.read_csv(os.path.join(RESULTS_FILEPATH, file))
    current_mean = df.mean()
    data[dataset].append((current_mean["kalibr"], current_mean["tartan"]))


# What you want = 
# dict {'kalibr': [1,2,3,4], 'tartan': [1,2,3,4]}
# index= ["ord", "blahblah", "blablah", "blabla"]

def average(l):
    return sum(l)/len(l)

l_kalibr = []
l_tartan = []

columns = []
for experiment_name, values in data.items():
    kalibr_points = []
    tartan_points = []
    #values = (kalibr, tartan)
    columns.append(experiment_name)
    for value in values:
        kalibr_points.append(value[0])
        tartan_points.append(value[1])

    l_kalibr.append(average(kalibr_points))
    l_tartan.append(average(tartan_points))

# print(columns)
# print(l_kalibr)
# print(l_tartan)

data = {"kalibr": l_kalibr, "tartan": l_tartan}
mean_df = pd.DataFrame(data=data, index=columns)
mean_df.to_csv(os.path.join(RESULTS_FILEPATH, "mean.csv"), index=True)
print(mean_df)