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
        self.errors = []

class GT_compare:
    def __init__(self,input,output):
        self.input = input
        self.output = output
        
        self.load_gt()
        self.load_baselines()
        self.evaluate()

    def evaluate(self):
        for method in self.methods:
            print("Evaluating method {0}".format(method.name))
            for i, frame_features in enumerate(method.data):
                if (len(np.shape(frame_features)) == 3):
                    frame_features = np.array(frame_features).reshape((-1,2))
                gt = self.GT[i]
                for feature in frame_features:
                    if (len(feature) ==3):
                        feature = feature[1:]
                        
                    feature = np.array(feature).reshape((2,1))
                    gt_dists = gt-feature
                    dists = np.linalg.norm(gt_dists,axis=1)
                    
                    method.errors.append(np.min(dists))
                    # print("new")
                    # print(gt[0])
                    # print(feature)
                    # print(print(gt_dists[0]))
                    # print(gt_dists.shape)
            print("Mean error of method {0} is {1} [px]".format(method.name,np.mean(method.errors)) )


    def load_gt(self):
        self.GT_dir = os.path.join(self.input,'GT')
        gt_files = glob.glob(os.path.join(self.GT_dir,'*.npy'))
        self.GT = []
        n_gt = len(gt_files)

        for i in range(n_gt):
            self.GT.append(np.load(os.path.join(self.GT_dir,str(i)+'.npy')))

        # gts = []
        # for idx in gt_idxs:
        #     gts.append(np.load(os.path.join(self.GT_dir,str(idx)+'.npy')))
        
        # print(np.shape(gts))
    
    def load_baselines(self):
        self.methods = []
        for file in glob.glob(os.path.join(self.input,'**/*.npy')):
            if os.path.split(file)[0].split('/')[-1] != 'GT':
                self.methods.append(MethodResult(file,None))
                print("Loading {0} with shape {1}".format(self.methods[-1].name,np.shape(self.methods[-1].data)))

        for file in glob.glob(os.path.join(self.input,'**/*.pkl')):
            self.methods.append(MethodResult(None,file))
            print("Loading {0} with shape {1}".format(self.methods[-1].name,np.shape(self.methods[-1].data)))

if __name__ == '__main__':
    # create pandas dataframe with name and error as columns 
    df = pd.DataFrame(columns=['name','error'])


    for experiment in glob.glob(os.path.join(args.experiments,'**')):
        gt_results = GT_compare(experiment,args.output)
        for method in gt_results.methods:
            # df = pd.concat([df,pd.DataFrame([method.name,np.mean(method.errors)])],ignore_index=True)
            df.loc[len(df)]  = [method.name,np.mean(method.errors)]
    # save dataframe to csv
    df.to_csv(args.output)

