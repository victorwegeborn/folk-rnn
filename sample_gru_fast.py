import sys
import os
import time
import importlib
if sys.version_info < (3,0):
    import cPickle as pickle
else:
    import pickle
import numpy as np
import argparse
import pdb
import json

parser = argparse.ArgumentParser()
parser.add_argument('metadata_path')
parser.add_argument('--rng_seed', type=int, default=42)
parser.add_argument('--temperature', type=float, default=1.0)
parser.add_argument('--ntunes', type=int, default=1)
parser.add_argument('--seed')
parser.add_argument('--terminal', action="store_true")

args = parser.parse_args()

metadata_path = args.metadata_path
rng_seed = args.rng_seed
temperature = args.temperature
ntunes = args.ntunes
seed = args.seed

with open(metadata_path) as f:
    metadata = pickle.load(f)

if not os.path.isdir('samples'):
    os.makedirs('samples')
target_path = "samples/%s-s%d-%.2f-%s.txt" % (
    metadata['experiment_id'], rng_seed, temperature, time.strftime("%Y%m%d-%H%M%S", time.localtime()))

token2idx = metadata['token2idx']
idx2token = dict((v, k) for k, v in token2idx.iteritems())
vocab_size = len(token2idx)

start_idx, end_idx = token2idx['<s>'], token2idx['</s>']

rng = np.random.RandomState(rng_seed)
vocab_idxs = np.arange(vocab_size)

#found by nn.layers.get_all_params(l_out)
#[W, 0
#W_in_to_updategate, W_hid_to_updategate, b_updategate, 1-3
#W_in_to_resetgate, W_hid_to_resetgate, b_resetgate, 4-6
#W_in_to_hidden_update, W_hid_to_hidden_update, b_hidden_update, 7-9
#hid_init, 10
#W_in_to_updategate, W_hid_to_updategate, b_updategate, 
#W_in_to_resetgate, W_hid_to_resetgate, b_resetgate, 
#W_in_to_hidden_update, W_hid_to_hidden_update, b_hidden_update, 
#hid_init, 20
#W_in_to_updategate, W_hid_to_updategate, b_updategate, 
#W_in_to_resetgate, W_hid_to_resetgate, b_resetgate, 
#W_in_to_hidden_update, W_hid_to_hidden_update, b_hidden_update, 
#hid_init, 30
#W, 31
#b] 32

GRU_Wxr=[]
GRU_Wxu=[]
GRU_Wxc=[]
GRU_Whr=[]
GRU_Whu=[]
GRU_Whc=[]
GRU_br=[]
GRU_bu=[]
GRU_bc=[]
GRU_hid_init=[]
htm1=[]

numlayers=3 # hard coded for now, but this should be saved in the model pickle
for jj in range(numlayers):
    GRU_Wxu.append(metadata['param_values'][1+jj*10])
    GRU_Whu.append(metadata['param_values'][2+jj*10])
    GRU_bu.append(metadata['param_values'][3+jj*10])
    GRU_Wxr.append(metadata['param_values'][4+jj*10])
    GRU_Whr.append(metadata['param_values'][5+jj*10])
    GRU_br.append(metadata['param_values'][6+jj*10])
    GRU_Wxc.append(metadata['param_values'][7+jj*10])
    GRU_Whc.append(metadata['param_values'][8+jj*10])
    GRU_bc.append(metadata['param_values'][9+jj*10])
    GRU_hid_init.append(metadata['param_values'][10+jj*10])
    htm1.append(GRU_hid_init[jj])

FC_output_W = metadata['param_values'][31];
FC_output_b = metadata['param_values'][32];

def sigmoid(x): return 1/(1 + np.exp(-x))
def softmax(x,T): 
    expx=np.exp(x/T)
    sumexpx=np.sum(expx)
    if sumexpx==0:
       maxpos=x.argmax()
       x=np.zeros(x.shape, dtype=x.dtype)
       x[0][maxpos]=1
    else:
       x=expx/sumexpx
    return x

sizeofx=GRU_Wxr[0].shape[0]
x = np.zeros(sizeofx, dtype=np.int8)
# Converting the seed passed as an argument into a list of idx
seed_sequence = [start_idx]
if seed is not None:
    for token in seed.split(' '):
         seed_sequence.append(token2idx[token])
         
    # initialise network
    for tok in seed_sequence[:-1]:
       x = np.zeros(sizeofx, dtype=np.int8)
       x[tok] = 1;
       for jj in range(numlayers):
          rt=sigmoid(np.dot(x,GRU_Wxr[jj]) + np.dot(htm1[jj],GRU_Whr[jj]) + GRU_br[jj])
          ut=sigmoid(np.dot(x,GRU_Wxu[jj]) + np.dot(htm1[jj],GRU_Whu[jj]) + GRU_bu[jj])
          ct=np.tanh(np.dot(x,GRU_Wxc[jj]) + np.multiply(rt,np.dot(htm1[jj],GRU_Whc[jj])) + GRU_bc[jj])
          ht=np.multiply(ut,ct) + np.multiply(1-ut,htm1[jj])
          x=ht
          htm1[jj]=ht
    for jj in range(numlayers):
        GRU_hid_init[jj]=htm1[jj]

header=idx2token.values()
with open('vocabulary.txt', 'w') as outfile:
    json.dump(idx2token, outfile)
#headerstr="\""+header[0]
#for hh in header[1:]:
#   headerstr+="\", "+"\""+hh

for i in xrange(ntunes):
    # initialise network
    output=[]
    for jj in range(numlayers):
        htm1[jj]=GRU_hid_init[jj]
    sequence = seed_sequence[:]
    while sequence[-1] != end_idx:
       x = np.zeros(sizeofx, dtype=np.int8)
       x[sequence[-1]] = 1;
       for jj in range(numlayers):
          rt=sigmoid(np.dot(x,GRU_Wxr[jj]) + np.dot(htm1[jj],GRU_Whr[jj]) + GRU_br[jj])
          ut=sigmoid(np.dot(x,GRU_Wxu[jj]) + np.dot(htm1[jj],GRU_Whu[jj]) + GRU_bu[jj])
          ct=np.tanh(np.dot(x,GRU_Wxc[jj]) + np.multiply(rt,np.dot(htm1[jj],GRU_Whc[jj])) + GRU_bc[jj])
          ht=np.multiply(ut,ct) + np.multiply(1-ut,htm1[jj])
          x=ht
          htm1[jj]=ht
       output.append(softmax(np.dot(x,FC_output_W) + FC_output_b,temperature))
       next_itoken=rng.choice(vocab_idxs, p=output[-1].squeeze())
       sequence.append(next_itoken)
       if len(sequence) > 1000: break
    
    #np.savetxt('heatmap_'+repr(i)+'.txt',np.concatenate(output),fmt='%.5f',delimiter=',')
    abc_tune = [idx2token[j] for j in sequence[1:-1]]
    if not args.terminal:
        print('X:' + repr(i))
        f = open(target_path, 'a+')
	f.write('X:' + repr(i) + '\n')
        f.write(abc_tune[0] + '\n')
        f.write(abc_tune[1] + '\n')
        f.write(' '.join(abc_tune[2:]) + '\n\n')
        f.close()
    else:
	print('X:' + repr(i))
        print(abc_tune[0])
        print(abc_tune[1])
        print(''.join(abc_tune[2:]) + '\n')

if not args.terminal:
    print('Saved to '+target_path)
