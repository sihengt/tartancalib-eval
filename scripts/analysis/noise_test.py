import numpy as np
import pandas as pd 
import seaborn as sns
from mlxtend.plotting import plot_confusion_matrix
import matplotlib.pyplot as plt

experiment_input = 'results/noise/merged_results.csv'
detectors = ['Deltille','AT3','Kaess-AT3','ArUco','TartanCalib']




class Experiment:
    def __init__(self,filename,deltille,at3,kaess,aruco,tartancalib):
        self.filename = filename
        self.extract_params()
        
        self.detections = {}
        self.detections['Deltille'] = deltille
        self.detections['AT3'] = at3 
        self.detections['Kaess-AT3'] = kaess 
        self.detections['ArUco'] = aruco 
        self.detections['TartanCalib'] = tartancalib  

    def extract_params(self):
        self.folder = self.filename.split('/')[-1]
        split = self.folder.split('_')

        # find noise param
        noise_idx = split.index('noise')
        self.noise_var = split[noise_idx+1]

    

df = pd.read_csv(experiment_input)
experiments = []
for i, file in enumerate(df['File']):
    experiment = Experiment(file,df['Deltille'][i],df['AT3'][i],df['Kaess-AT3'][i],df['ArUco'][i],df['TartanCalib'][i])
    experiments.append(experiment)

vars = []

for experiment in experiments:
    vars.append(experiment.noise_var)

vars = np.sort(np.unique(np.array(vars)))


def get_idx(var):
    return np.where(vars==var)


results = {}
for detector in detectors:
    results[detector] = np.zeros(len(vars))

for experiment in experiments:
    for detector in detectors:
        results[detector][get_idx(experiment.noise_var)] += experiment.detections[detector]


# plot results
fig, ax = plt.subplots(1,1)
for detector in detectors:
    ax.plot(vars,results[detector],label=detector)
    ax.set_xlabel('Noise Variance', fontsize=18)
    ax.set_ylabel('Corners Detected', fontsize=18)
    ax.set_title('Noise Test', fontsize=18)
    ax.legend()
plt.show()

# fig, axs = plt.subplots(2,3)
# idxs = [axs[0,0],axs[0,1],axs[0,2],axs[1,0],axs[1,1]]
# cbar_ax = fig.add_axes([.91, .3, .03, .4])

# for i, detector in enumerate(detectors):
#     matrix = matrices[detector]
#     ax = idxs[i]
#     sns.heatmap(matrix, annot=True, fmt='g', ax=ax,cbar_ax=None if i else cbar_ax);  #annot=True to annotate cells, ftm='g' to disable scientific notation
#     ax.yaxis.set_ticklabels(blurs,fontsize=18); ax.xaxis.set_ticklabels(alpha_s,fontsize=18);

#     ax.set_xlabel('Alpha', fontsize=18)
#     ax.set_ylabel('Blur Window', fontsize=18)
#     ax.set_title(detector, fontsize=18)
# plt.show()