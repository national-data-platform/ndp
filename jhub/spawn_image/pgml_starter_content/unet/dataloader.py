from torch.utils.data import DataLoader
import numpy as np

class WFDataloader(object):
    """
    This is not a Pytorch DataLoader though it can be used as one in training and validation
    Use it with the IdealizedGrassland dataset and it will properly set the cache
    
    set_mode -> set to train or val as reuqired
    """
    def __init__(self, dataset, *args, **kwargs):
        self.dataset = dataset
        self.dataloader = DataLoader(dataset, *args, **kwargs)
    
    def set_mode(self, mode):
        self.dataset.mode = mode
    
    def __len__(self):
        return self.dataset.size*getattr(self.dataset, f"{self.dataset.mode}_index").size
    
    def __iter__(self):
        arr = getattr(self.dataset, f"{self.dataset.mode}_index")
        np.random.shuffle(arr)
        for tidx in arr:
            self.dataset.cache.set_data(self.dataset.zarrs[tidx].zarr)
            for batch in self.dataloader:
                yield batch

class DummyLoader(DataLoader):
    """
    Dummy Loader for WFDataloader for dry runs
    """
    def set_mode(self, mode):
        self.dataset.mode = mode
    
    def __len__(self):
        return 1
