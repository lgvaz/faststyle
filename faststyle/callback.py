# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/06_callback.ipynb (unless otherwise specified).

__all__ = ['FeatsCallback', 'WeightsCallback']

# Cell
from fastai2.basics import *
from fastai2.callback.all import *
from faststyle import *

# Cell
# TODO: This allow loss functions to be separated
class FeatsCallback(Callback):
  def __init__(self, get_fts, stl_fts=None, cnt_fts=None):
    store_attr(self, 'get_fts,stl_fts,cnt_fts')
    # Change dict with a class. Can be accessed with .
    self.fts = dict(pred={}, targ={}, source={})
    self.fts['source']['stl'],self.fts['source']['cnt'] = L(stl_fts),L(cnt_fts)

  def after_pred(self):
    if len(self.yb) == 0: return
    fts = self.fts
    fts['pred']['stl'],fts['pred']['cnt'] = self.get_fts(self.pred)
    fts['targ']['stl'],fts['targ']['cnt'] = self.get_fts(self.yb[0])
    self.learn.yb = (*self.yb, fts)

  @classmethod
  def from_fns(cls, fns, get_fts):
    source_tims = L(TensorImage.create(fn) for fn in L(fns))
    stl_fts,cnt_fts = zip(*L(get_fts(o[None]) for o in source_tims))
    stl_fts,cnt_fts = L(zip(*stl_fts)),L(zip(*cnt_fts))
    return cls(get_fts=get_fts, stl_fts=stl_fts, cnt_fts=cnt_fts)

# Cell
class WeightsCallback(Callback):
  def after_pred(self):
    if len(self.yb) == 0: return
    self.yb[1]['ws'] = self.xb[0].ws