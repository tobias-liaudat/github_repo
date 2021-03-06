import sys
sys.path.append('../')
import warnings
warnings.filterwarnings("ignore", message="numpy.dtype size changed")
warnings.filterwarnings("ignore", message="numpy.ufunc size changed")
import matplotlib.pyplot as plt
import numpy as np
#import scipy.io as spio
#import scipy.signal as spsg
from src.misc_bgmca2 import *
from src.utils2 import *
from src.starlet import *
from src.BGMCA3 import BGMCA as bgmca3
from src.GMCA import GMCA as gmca_original
import copy as cp
#from tqdm import tqdm


#try:
################# Main test script
totalSize = 2000
# minSizeBlock = 200
# divisors = list(divisorGenerator(totalSize))
# divisors = np.array(divisors)
# divisors = divisors[divisors>=minSizeBlock]
minSizeBlock = 200
divisors = np.array([200])

data_path = '../test_data/'
plots_path = '../plots/'

n_s = 5
n_obs = 20
numIts = 25
n_epoch = np.array([10, 25, 50, 100, 200, 400, 800])


print('*******************************************')
print('divisors: ' + str(divisors))
print('n_sources: ' + str(n_s))
print('n_epoch: ' + str(n_epoch))
print('numIts: ' + str(numIts))
print('n_obs: ' + str(n_obs))
print('*******************************************')

ca_final_sB = np.zeros([2,len(divisors),len(n_epoch),numIts]) # [i,:,:,:] i=0 mean i=1 med
ca_final_tot = np.zeros([2,len(n_epoch),numIts]) # [i,:,:] i=0 mean i=1 med


for it_n in range(len(n_epoch)):
#    n_s = n_sources[it_n]
#    n_obs = n_s
    n_it = n_epoch[it_n]

    for it0 in range(numIts):
        X,X0,A0,S0,N = Make_Experiment_GG(n_s=n_s,n_obs=n_obs,t_samp=totalSize,noise_level=60.0,dynamic=0,CondNumber=1,alpha=0.5)

        Results_original = gmca_original(cp.deepcopy(X),n=n_s,maxts = 7,mints=3,nmax=n_it,L0=1,UseP=1,verb=0,Init=0,\
            Aposit=False,BlockSize= None,NoiseStd=[],IndNoise=[],Kmax=1.,AInit=None,tol=1e-6,threshOpt=1,SCOpt=1)


        A_original = Results_original['mixmat']
        S_original = Results_original['sources']
        crit_original = EvalCriterion(A0,S0,A_original,S_original) 
        ca_final_tot[0,it_n,it0] = crit_original['ca_mean']
        ca_final_tot[1,it_n,it0] = crit_original['ca_med']

        if crit_original['ca_mean'] > 0.1:
            print('crit_original[ca_mean] > 0.1')
        if crit_original['ca_med'] > 0.1:
            print('crit_original[ca_med] > 0.1')    

        for it1 in range(len(divisors)):
            numBlock = totalSize/divisors[it1]
            sizeBlock = divisors[it1]

            Results_sB = bgmca3(cp.deepcopy(X),n=n_s,maxts = 7,mints=3,nmax=n_it,L0=1,UseP=1,verb=0,Init=0,Aposit=False,\
                BlockSize= None,NoiseStd=[],IndNoise=[],Kmax=1.,AInit=None,tol=1e-6,subBlockSize=sizeBlock,\
                threshOpt=2,weightFMOpt=1,SCOpt=1,alphaEstOpt=0,optA=1,alpha_exp=2.)

            A_sB = Results_sB['mixmat']
            S_sB = Results_sB['sources']
            crit_sB = EvalCriterion(A0,S0,A_sB,S_sB) 
            ca_final_sB[0,it1,it_n,it0] = crit_sB['ca_mean']
            ca_final_sB[1,it1,it_n,it0] = crit_sB['ca_med']
            
            if crit_sB['ca_mean'] > 0.1:
                print('crit_sB[ca_mean] > 0.1')
            if crit_sB['ca_med'] > 0.1:
                print('crit_sB[ca_med] > 0.1')           


print('ca_final_tot: ')
print(ca_final_tot)
print('ca_final_sB: ')
print(ca_final_sB)


title_str = "Test_epoch_number" + "_totalSize_" + str(totalSize) + "_minSizeBlock_" + str(minSizeBlock) +\
    "_numIts_" + str(numIts) + "_n_epoch_" + str(len(n_epoch))

title_str_pdf = plots_path + title_str + ".pdf"

# Save variables
title_ca_final_sB = data_path + 'ca_final_sB' + title_str  
np.save(title_ca_final_sB,ca_final_sB)
title_ca_final_tot = data_path + 'ca_final_tot' + title_str  
np.save(title_ca_final_tot,ca_final_tot)


ca_final_sB_mean = np.mean(ca_final_sB,axis=3)
ca_final_tot_mean = np.mean(ca_final_tot,axis=2)
ca_final_sB_med = np.median(ca_final_sB,axis=3)
ca_final_tot_med = np.median(ca_final_tot,axis=2)


################# Ploting script
import matplotlib
matplotlib.rcParams.update({'font.size': 18})

log_ca_final_sB_mean = -10*np.log10(ca_final_sB_mean)
log_ca_final_sB_med = -10*np.log10(ca_final_sB_med)
log_ca_final_tot_mean = -10*np.log10(ca_final_tot_mean)
log_ca_final_tot_med = -10*np.log10(ca_final_tot_med)

print('*******************************************')
print('*******************************************')
print 'log_ca_final_sB_mean: '
print log_ca_final_sB_mean
print('*******************************************')
print 'log_ca_final_tot_mean: '
print log_ca_final_tot_mean
print('*******************************************')
print 'log_ca_final_sB_med: '
print log_ca_final_sB_med
print('*******************************************')
print 'log_ca_final_tot_med: '
print log_ca_final_tot_med
print('*******************************************')
print('*******************************************')


