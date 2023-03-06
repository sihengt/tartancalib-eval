from argparse import ArgumentParser
import pandas as pd
import numpy as np
import glob 
import os
import dill 

parser = ArgumentParser()
parser.add_argument('-e','--experiments')
parser.add_argument('-o','--output',default='refine_accuracy.csv')
args = parser.parse_args()

class MethodResult:
    def __init__(self,npy,pkl):
        if npy is not None:
            self.data = np.load(npy,allow_pickle=True)
            self.name = os.path.basename(npy)
        
        elif pkl is not None:
            with open(pkl, 'rb') as f:
                self.data = dill.load(f)
                self.name = os.path.basename(pkl)

class GT_compare:
    def __init__(self,input,output):
        self.input = input
        self.output = output
        
        self.load_gt()
        self.load_baselines()
        

    def load_gt(self):
        self.GT_dir = os.path.join(self.input,'GT')
        # gt_idxs = np.load(os.path.join(self.GT_dir,'train_stamps.npy'))
        # gts = []
        # for idx in gt_idxs:
        #     gts.append(np.load(os.path.join(self.GT_dir,str(idx)+'.npy')))
        
        # print(np.shape(gts))
    
    def load_baselines(self):
        methods = []
        for file in glob.glob(os.path.join(self.input,'**/*.npy')):
            methods.append(MethodResult(file,None))
            print("Loading {0} with shape {1}".format(methods[-1].name,np.shape(methods[-1].data)))

        for file in glob.glob(os.path.join(self.input,'**/*.pkl')):
            methods.append(MethodResult(None,file))
            print("Loading {0} with shape {1}".format(methods[-1].name,np.shape(methods[-1].data)))

if __name__ == '__main__':
    for experiment in glob.glob(os.path.join(args.experiments,'**')):
        GT_compare(experiment,args.output)
