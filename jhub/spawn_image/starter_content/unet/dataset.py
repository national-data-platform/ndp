import torch
import numpy as np
from torch.utils import data
import warnings
import pandas as pd
import zarr

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
warnings.filterwarnings("ignore")

def read_dataset(file):
    return pd.read_csv(file)


class IdealizedGrasslands(data.Dataset):
    def __init__(self, indices, input_length, mid, output_length, direc, file):
        self.input_length = input_length
        self.mid = mid
        self.output_length = output_length
        self.direc = direc
        self.list_IDs = indices

        self.runs_df=read_dataset(file)

    def __len__(self):
        return len(self.list_IDs)

    def __getitem__(self, index):
        link = self.runs_df.loc[index]['link']
        print(f'Getting run {index} from {link}.')
        run_zarr = zarr.open(link)
        fuel = np.array(run_zarr['fuels-moist'])
        fuel = torch.FloatTensor(fuel[80::10])  #
        y_fuel = fuel[self.mid:(self.mid + self.output_length)]
        x_fuel = fuel[(self.mid - self.input_length):self.mid]
        print(f'Got run {index}.')
        return x_fuel.float(), y_fuel.float()