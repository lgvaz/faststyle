# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/05_callback.ipynb (unless otherwise specified).

__all__ = ['feat_m', 'VggFeats', 'layers', 'get_fs', 'StyleFsCallback']

# Cell
from fastai2.basics import *
from fastai2.callback.all import *
from fastai2.vision.all import *
from torchvision.models import vgg16, vgg19
from faststyle import *

# Cell
#TODO: hardcoded model
feat_m = vgg19(True).features.cuda().eval()
for p in feat_m.parameters(): p.requires_grad=False

# Cell
def VggFeats(layers):
  hooks = hook_outputs(layers, detach=False)
  def _inner(x):
    feat_m(x)
    return hooks.stored
  return _inner

# Cell
#TODO: hardcoded layers
# layers = [feat_m[i] for i in [1, 11, 18, 25, 20]]; layers # vgg16
layers = [feat_m[i] for i in [1, 6, 11, 20, 29, 22]]; layers # vgg19
get_fs = VggFeats(layers)

# Cell
def _get_ims(fns):
  t = TfmdLists(fns, tfms=[PILImage.create, ToTensor(), IntToFloatTensor(),
                               Normalize.from_stats(*coco_stats, cuda=False)])
  return [o.to(default_device()) for o in t]

# Cell
class StyleFsCallback(Callback):
  def __init__(self, fns, get_fs, tfms=None):
    self.sims_fs = [get_fs(o) for o in _get_ims(fns)]

  def after_pred(self):
    self.learn.yb = (*self.yb, self.sims_fs)