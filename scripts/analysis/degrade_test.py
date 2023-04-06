import numpy as np
import pandas as pd 
import seaborn as sns
from mlxtend.plotting import plot_confusion_matrix
import matplotlib.pyplot as plt

experiment_input = 'results/total_corners_detected.csv'
detectors = ['Deltille','AT3','Kaess-AT3','ArUco']




class Experiment:
    def __init__(self,filename,deltille,at3,kaess,aruco):
        self.filename = filename
        self.extract_params()
        
        self.detections = {}
        self.detections['Deltille'] = deltille
        self.detections['AT3'] = at3 
        self.detections['Kaess-AT3'] = kaess 
        self.detections['ArUco'] = aruco 

    def extract_params(self):
        self.folder = self.filename.split('/')[-1]
        split = self.folder.split('_')

        # find blur param
        blur_idx = split.index('blur')
        self.blur_window = int(split[blur_idx+1])

        # find alpha param
        alpha_idx = split.index('alpha')
        self.alpha = float(split[alpha_idx+1])
    

df = pd.read_csv(experiment_input)
experiments = []
for i, file in enumerate(df['File']):
    experiment = Experiment(file,df['Deltille'][i],df['AT3'][i],df['Kaess-AT3'][i],df['ArUco'][i])
    experiments.append(experiment)

alpha_s = []
blurs = []

for experiment in experiments:
    alpha_s.append(experiment.alpha)
    blurs.append(experiment.blur_window)

blurs, alpha_s = np.sort(np.unique(np.array(blurs))), np.sort(np.unique(np.array(alpha_s)))
n_blurs, n_alphas = len(blurs), len(alpha_s)

def get_idx(alpha,blur):
    return np.where(blurs==blur), np.where(alpha_s==alpha)


matrices = {}
for detector in detectors:
    matrices[detector] = np.zeros((n_blurs,n_alphas))

for experiment in experiments:
    for detector in detectors:
        matrices[detector][get_idx(experiment.alpha,experiment.blur_window)] += experiment.detections[detector]


fig, axs = plt.subplots(2,2)
idxs = [axs[0,0],axs[0,1],axs[1,0],axs[1,1]]
cbar_ax = fig.add_axes([.91, .3, .03, .4])

for i, detector in enumerate(detectors):
    matrix = matrices[detector]
    ax = idxs[i]
    sns.heatmap(matrix, annot=True, fmt='g', ax=ax,cbar_ax=None if i else cbar_ax);  #annot=True to annotate cells, ftm='g' to disable scientific notation
    ax.yaxis.set_ticklabels(blurs,fontsize=18); ax.xaxis.set_ticklabels(alpha_s,fontsize=18);

    ax.set_xlabel('Alpha', fontsize=18)
    ax.set_ylabel('Blur Window', fontsize=18)
    ax.set_title(detector, fontsize=18)
plt.show()