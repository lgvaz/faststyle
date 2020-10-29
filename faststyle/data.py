# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/01_data.ipynb (unless otherwise specified).

__all__ = ['IncrementalSplitter', 'TensorImageX', 'PILImageX', 'NormalizeX', 'style_blocks', 'NormalizeAll',
           'random_weights', 'Weights', 'ImageWeight', 'RandomizeWeights', 'coco_stats']

# Cell
from fastai.basics import *
from fastai.vision.all import *
from faststyle import *

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
class TensorImageX(TensorImage): pass

# Cell
class PILImageX(PILImage): pass
PILImageX._tensor_cls = TensorImageX

# Cell
class NormalizeX(Normalize):
  def encodes(self, x:TensorImage, **kwargs): return x
  def decodes(self, x:TensorImage, **kwargs): return x

  def encodes(self, x:TensorImageX, **kwargs): return super().encodes(x, **kwargs)
  def decodes(self, x:TensorImageX, **kwargs): return super().decodes(x, **kwargs)

# Cell
style_blocks = ImageBlock(PILImageX), ImageBlock()

# Cell
class NormalizeAll(Normalize):
  def encodes(self, x:Tensor, **kwargs): return super().encodes[TensorImage](self, x, **kwargs)
  def decodes(self, x:Tensor, **kwargs): return super().decodes[TensorImage](self, x, **kwargs)

# Cell
def random_weights(*size):
  x = torch.rand(*size)
  return x / x.sum()

# Cell
class Weights(TensorBase, ShowTitle):
  _show_args = {'label': 'weights'}
  @classmethod
  def create(cls, x):  return cls(x)

# Cell
class ImageWeight(fastuple):
  @classmethod
  def create(cls, fnw, imcls=PILImageX): return cls(imcls.create(fnw[0]), Weights(fnw[1]))
  def show(self, ctx=None, **kwargs): return show_titled_image(self, ctx=ctx, **kwargs)
ImageWeight.im, ImageWeight.ws = add_props(lambda i,x: x[i])

# Cell
class RandomizeWeights(RandTransform):
  def encodes(self, x:Weights):
    x.data = random_weights(*x.shape)
    return x

# Cell
@typedispatch
def show_batch(x:ImageWeight, y:TensorImage, samples, **kwargs):
  return show_batch.funcs[TensorImage][TensorImage](x, y, samples, **kwargs)

# Cell
@typedispatch
def show_results(x:ImageWeight, y:TensorImage, samples, outs, **kwargs):
  return show_results.funcs[TensorImage][TensorImage](x, y, samples, outs, **kwargs)

# Cell
coco_stats = ([0.4605, 0.4101, 0.3642], [0.2780, 0.2701, 0.2741])