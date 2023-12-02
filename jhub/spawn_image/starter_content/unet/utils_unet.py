import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from torch.utils import data
import itertools
import re
import random
import time
from torch.autograd import Variable
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
import warnings
#import kornia
warnings.filterwarnings("ignore")




def train_epoch(train_loader, model, optimizer, loss_function, teacher_force_ratio):
    train_mse = []
    for xx, yy in train_loader:
        # print(xx.size())
        # print(yy.size())
        loss = 0
        ims = []
        xx = xx.to(device)
        yy = yy.to(device)
        xx=torch.squeeze(xx,dim=2)
        yy=torch.squeeze(yy,dim=2)
       # print(yy.shape)
        use_teacher_force=True if np.random.random()<teacher_force_ratio else False
        for y in yy.transpose(0, 1):
            im = model(xx)
            if use_teacher_force:
                xx=torch.cat([xx[:, 1:],y.unsqueeze(1)], 1)
            else:
                xx = torch.cat([xx[:, 1:], im], 1)
            loss += loss_function(im, y)
            # print(loss)
            ims.append(im.cpu().data.numpy())

        ims = np.concatenate(ims, axis=1)
        train_mse.append(loss.item() / yy.shape[1])
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    train_mse = round((np.mean(train_mse)), 5)
    return train_mse


def eval_epoch(valid_loader, model, loss_function):
    valid_mse = []
    preds = []
    trues = []
    with torch.no_grad():
        for xx, yy in valid_loader:
            loss = 0
            xx = xx.to(device)
            yy = yy.to(device)
            xx=torch.squeeze(xx,dim=2)
            yy=torch.squeeze(yy,dim=2)
            ims = []

            for y in yy.transpose(0, 1):
                im = model(xx)
                xx = torch.cat([xx[:, 1:], im], 1)
                loss += loss_function(im, y)
                ims.append(im.cpu().data.numpy())

            ims = np.array(ims).transpose(1, 0, 2, 3, 4)
            valid_mse.append(loss.item() / yy.shape[1])

        valid_mse=round((np.mean(valid_mse)), 8)
    return valid_mse, preds, trues


def test_epoch(test_loader, model, loss_function):
    valid_mse = []
    preds = []
    trues = []
    with torch.no_grad():
        loss_curve = []
        for xx, yy in test_loader:
            xx = xx.to(device)
            yy = yy.to(device)
            xx=torch.squeeze(xx,dim=2)
            yy=torch.squeeze(yy,dim=2)
            #print(yy.shape)
            loss = 0
            ims = []

            for y in yy.transpose(0, 1):
                im = model(xx)
                xx = torch.cat([xx[:, 1:], im], 1)
                mse = loss_function(im, y)
                loss += mse
                loss_curve.append(mse.item())

                ims.append(im.cpu().data.numpy())

            ims = np.array(ims).transpose(1, 0, 2, 3, 4)
            preds.append(ims)
            trues.append(yy.cpu().data.numpy())
            valid_mse.append(loss.item() / yy.shape[1])

        preds = np.concatenate(preds, axis=0)
        trues = np.concatenate(trues, axis=0)

        prediction_length=preds.shape[1]
        loss_curve=np.array(loss_curve).reshape(-1, prediction_length)
        loss_curve=(np.mean(loss_curve,axis=0))
    return loss_curve,preds, trues

