import numpy as np
import pandas as pd 
import seaborn as sns
import matplotlib.pyplot as plt

experiment_input = 'refine_accuracy.csv'




class Experiment:
    def __init__(self,name,error):
        self.name = name
        self.error = error
        self.extract_params()
        
        # self.detections = {}
        # self.detections['Deltille'] = deltille
        # self.detections['AT3'] = at3 
        # self.detections['Kaess-AT3'] = kaess 
        # self.detections['ArUco'] = aruco 
        # self.detections['TartanCalib'] = tartancalib  

    def extract_params(self):
        blur_idx = self.name.replace('-','_').split('_').index('blur')
        self.blur = int(self.name.replace('-','_').split('_')[blur_idx+1])
        self.detector = self.name.split('-')[0]


df = pd.read_csv(experiment_input)
experiments = []
for i, name in enumerate(df['name']):
    experiment = Experiment(name,df['error'][i])
    experiments.append(experiment)

blurs = []
detectors = []

for experiment in experiments:
    blurs.append(experiment.blur)
    detectors.append(experiment.detector)


blurs = np.sort(np.unique(np.array(blurs)))


def get_idx(blur):
    return np.where(blurs==blur)

detectors = np.sort(np.unique(np.array(detectors)))

results = {}
for detector in detectors:
    results[detector] = np.zeros(len(blurs))

for experiment in experiments:
    results[experiment.detector][get_idx(experiment.blur)] = experiment.error


# plot results
fig, ax = plt.subplots(1,1)
for detector in detectors:
    ax.plot(blurs,results[detector],label=detector)
    ax.set_xlabel('Blur Kernel Size', fontsize=18)
    ax.set_ylabel('Feature Localization Error [px]', fontsize=18)
    ax.set_title('Blur Test', fontsize=18)
    # set xticks font size
    for label in (ax.get_xticklabels()):
        label.set_fontsize(18)
    
    # set yticks font size
    for label in (ax.get_yticklabels()):
        label.set_fontsize(18)

    ax.legend(fontsize=18)
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