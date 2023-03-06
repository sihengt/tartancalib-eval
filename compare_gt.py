from argparse import ArgumentParser
import pandas as pd
import numpy as np
import glob 
import os
parser = ArgumentParser()
parser.add_argument('-e','--experiments')
parser.add_argument('-o','--output',default='refine_accuracy.csv')
args = parser.parse_args()


class GT_compare:
    def __init__(self,input,output):
        self.input = input
        self.output = output
        
        self.load_gt()
        experiment_folders = []
        

    def load_gt(self):
        self.GT_dir = os.path.join(self.input,'GT')
        gt_idxs = np.load(os.path.join(self.GT_dir,'train_stamps.npy'))
        gts = []
        for idx in gt_idxs:
            gts.append(np.load(os.path.join(self.GT_dir,str(idx)+'.npy')))
        
        print(np.shape(gts))


if __name__ == '__main__':
    for experiment in glob.glob(os.path.join(args.experiments,'**')):
        GT_compare(experiment,args.output)
