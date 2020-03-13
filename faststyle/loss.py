# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/03_loss.ipynb (unless otherwise specified).

__all__ = ['gram', 'ContentLoss', 'StyleLoss', 'TVLoss', 'FastStyleLoss']

# Cell
from fastai2.basics import *
from faststyle import *

# Cell
def gram(x):
    n,c,h,w = x.size()
    x = x.view(n, c, -1)
    return (x @ x.transpose(1,2))/(c*h*w)

# Cell
def ContentLoss():
  def _inner(pred, targ, fts):
    return sum([F.mse_loss(*o) for o in zip_safe(fts['pred']['cnt'],fts['targ']['cnt'])])
  return _inner

# Cell
def StyleLoss(ws=None):
  def _inner(pred, targ, fts):
    bs = fts['pred']['stl'][0].shape[0]
    sims_gs = L(torch.stack([gram(f) for f in fs]).wmean(ws, dim=0) for fs in fts['source']['stl'])
    pred_gs = [gram(f) for f in fts['pred']['stl']]
    assert len(sims_gs) == len(pred_gs)
    stl_losses = [F.mse_loss(g1.repeat(bs,1,1),g2) for g1,g2 in zip(sims_gs,pred_gs)]
    return sum(stl_losses)
  return _inner

# Cell
def TVLoss():
  def _inner(pred,*_):
    tv_h = ((pred[:,:,1:,:] - pred[:,:,:-1,:]).pow(2)).mean()
    tv_w = ((pred[:,:,:,1:] - pred[:,:,:,:-1]).pow(2)).mean()
    return (tv_h + tv_w)
  return _inner

# Cell
#TODO: Use @func_kwargs for losses
class FastStyleLoss(Module):
  def __init__(self, get_fs, stl_w=3e5, cnt_w=1, tv_w=20):
    self.stl_loss_fn,self.cnt_loss_fn,self.tv_loss_fn = StyleLoss(),ContentLoss(),TVLoss()
    store_attr(self, 'get_fs,stl_w,cnt_w,tv_w')
    self.metric_names = ['stl', 'cnt', 'tv']
    self.metrics = L(LossMetrics(self.metric_names))

  def forward(self, pred, targ, fts, **kwargs):
    self.stl = self.stl_w*self.stl_loss_fn(pred, targ, fts)
    self.cnt = self.cnt_w*self.cnt_loss_fn(pred, targ, fts)
    self.tv  = self.tv_w *self.tv_loss_fn (pred, targ, fts)
    return self.stl+self.cnt+self.tv