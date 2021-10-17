import math
import torch

import torch.nn as nn
import torch.nn.functional as F
import numpy as np
import scipy.sparse as sp

from torch.nn.parameter import Parameter
from torch.nn.modules.module import Module

class GCNModel(nn.Module):
    def __init__(self, n_class, n_in_features):
        super(GCNModel, self).__init__()


    def forward(self, input:torch.FloatTensor, adj:torch.FloatTensor):
        input.dot(adj)
        

class Facebook_Node_Classifier():
    def __init__(self, facebook_file: str):
        
        self.data_process(facebook_file)
        self.create_adj()
        
    def data_process(self, facebook_file: str):
        data = np.load(facebook_file)

        edges = data['edges']
        features = data['features']
        target = data['target']

        self.n_edges = edges.shape[0]
        self.n_features = features.shape[1]
        self.n_target = target.shape[0]
        self.n_class = len(np.unique(target))

        self.node_features = torch.FloatTensor(features)
        self.target = torch.LongTensor(target)
        self.edges = edges
        
    def create_adj(self):
        #create an iniitial adj matrix for sparse matrix
        adj = sp.coo_matrix((np.ones(self.n_edges), (self.edges[:, 0], self.edges[:, 1])))
        
        #make sure all element is 1 or 0
        adj_t = torch.Tensor(adj.toarray())
        adj_t[adj_t > 0] = 1

        #check adj is semetric or not
        assert sum(sum(adj_t != adj_t.T)) == 0, 'Adjacency matrix is not symetric'

        #normalise 
        rowsum = np.array(adj_t.sum(1))
        inv = np.ma.power(rowsum, -1) #creaet D^-1
        inv[inv == np.inf] = 0.#if 0 is inv 
        D_inv = sp.diags(inv)
        adj_m = D_inv.dot(adj_t) #D^-1*A

        self.adj = torch.FloatTensor(adj_m)

    


if __name__ == "__main__":
    
    facebook_path = 'facebook.npz'

    classifer = Facebook_Node_Classifier(facebook_file=facebook_path)

    print(classifer.adj.type())

    
