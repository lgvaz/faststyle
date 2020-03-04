# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/04_learner.ipynb (unless otherwise specified).

__all__ = ['style_learner']

# Cell
from fastai2.basics import *
from faststyle import *

# Cell
@delegates(Learner.__init__)
def style_learner(dls, model, get_feats, style_fns, loss_func=None, cbs=None, **kwargs):
  loss_func = loss_func or FastStyleLoss2(get_feats)
  cbs = L(cbs) + L(SourceFeatsCallback.from_fns(style_fns, get_feats))
  return Learner(dls, model, loss_func=loss_func, cbs=cbs, **kwargs)