# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/05_learner.ipynb (unless otherwise specified).

__all__ = ['style_learner']

# Cell
from fastai.basics import *
from faststyle import *

# Cell
@delegates(Learner.__init__)
def style_learner(dls, model, get_feats, style_fns, loss_func=None, cbs=None, metrics=None, **kwargs):
  loss_func = loss_func or FastStyleLoss()
  cbs = L(cbs) + L(FeatsCallback.from_fns(style_fns, get_feats))
  metrics = L(metrics) + getattr(loss_func, 'metrics', L())
  return Learner(dls, model, loss_func=loss_func, cbs=cbs, metrics=metrics, **kwargs)