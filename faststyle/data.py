# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/01_data.ipynb (unless otherwise specified).

__all__ = ['IncrementalSplitter', 'coco_stats']

# Cell
from fastai2.basics import *

# Cell
class IncrementalSplitter:
  'Dynamically changes pct of data used without mixing train and val data'
  @delegates(RandomSplitter)
  def __init__(self, pct=1., **kwargs):
    self.pct = pct
    seed = kwargs.pop('seed', None) or random.randint(0,1e6)
    self._splitter = RandomSplitter(seed=seed, **kwargs)

  def __call__(self, o, **kwargs):
    tidxs, vidxs = self._splitter(o, **kwargs)
    random.shuffle(tidxs); random.shuffle(vidxs)
    return tidxs[:int(len(tidxs)*self.pct)], vidxs[:int(len(vidxs)*self.pct)]

# Cell
coco_stats = ([0.4605, 0.4101, 0.3642], [0.2780, 0.2701, 0.2741])