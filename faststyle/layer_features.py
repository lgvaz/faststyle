# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/02_layer_features.ipynb (unless otherwise specified).

__all__ = ['FeatModels', 'LayerFeats']

# Cell
from fastai2.basics import *
from fastai2.vision.all import *
from fastai2.callback.all import *
from torchvision.models import vgg16, vgg19
from faststyle import *

# Cell
def _prepare_model(m):
  m = m.to(default_device()).eval()
  for p in m.parameters(): p.requires_grad=False
  return m

# Cell
def _get_layers(m, idxs):
  return [m[i] for i in idxs]

# Cell
_imagenet_norm = Normalize.from_stats(*imagenet_stats)

# Cell
class FeatModels:
  @staticmethod
  def vgg16():
    m = vgg16(True).features
    stl_ls = _get_layers(m, (1, 11, 18, 25))
    cnt_ls = _get_layers(m, (20,))
    return dict(m=m, stl_ls=stl_ls, cnt_ls=cnt_ls, tfms=[_imagenet_norm])

  @staticmethod
  def vgg19():
    m = vgg19(True).features
    stl_ls = _get_layers(m, (1, 6, 11, 20, 29))
    cnt_ls = _get_layers(m, (22,))
    return dict(m=m, stl_ls=stl_ls, cnt_ls=cnt_ls, tfms=[_imagenet_norm])

# Cell
class LayerFeats:
  def __init__(self, m, stl_ls, cnt_ls, tfms=None):
    self.m, self.tfms = _prepare_model(m), Pipeline(tfms)
    self.stl_hooks = hook_outputs(stl_ls, detach=False)
    self.cnt_hooks = hook_outputs(cnt_ls, detach=False)

  def __call__(self, x):
    _ = self.m(self.tfms(x))
    return self.stl_hooks.stored, self.cnt_hooks.stored

  @classmethod
  def from_feat_m(cls, feat_m): return cls(**feat_m())