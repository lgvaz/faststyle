# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/04_models.ipynb (unless otherwise specified).

__all__ = ['transformer_net', 'TransformerNet']

# Cell
import torch
from fastai2.basics import *
from fastai2.vision.all import *

# Cell
def transformer_net(): return TransformerNet()

# Cell
class TransformerNet(Module):
    def __init__(self):
        # Initial convolution layers
        self.conv1 = _ConvLayer(3, 32, kernel_size=9, stride=1)
        self.in1 = torch.nn.InstanceNorm2d(32, affine=True)
        self.conv2 = _ConvLayer(32, 64, kernel_size=3, stride=2)
        self.in2 = torch.nn.InstanceNorm2d(64, affine=True)
        self.conv3 = _ConvLayer(64, 128, kernel_size=3, stride=2)
        self.in3 = torch.nn.InstanceNorm2d(128, affine=True)
        # Residual layers
        self.res1 = _ResidualBlock(128)
        self.res2 = _ResidualBlock(128)
        self.res3 = _ResidualBlock(128)
        self.res4 = _ResidualBlock(128)
        self.res5 = _ResidualBlock(128)
        # Upsampling Layers
        self.deconv1 = PixelShuffle_ICNR(128, 64, norm_type=None)
        self.in4 = torch.nn.InstanceNorm2d(64, affine=True)
        self.deconv2 = PixelShuffle_ICNR(64, 32, norm_type=None)
        self.in5 = torch.nn.InstanceNorm2d(32, affine=True)
        self.deconv3 = _ConvLayer(32, 3, kernel_size=9, stride=1)
        # Non-linearities
        self.relu = torch.nn.ReLU()
        self.sigm = torch.nn.Sigmoid()

    def forward(self, X):
        y = self.relu(self.in1(self.conv1(X)))
        y = self.relu(self.in2(self.conv2(y)))
        y = self.relu(self.in3(self.conv3(y)))
        y = self.res1(y)
        y = self.res2(y)
        y = self.res3(y)
        y = self.res4(y)
        y = self.res5(y)
        y = self.relu(self.in4(self.deconv1(y)))
        y = self.relu(self.in5(self.deconv2(y)))
        y = self.deconv3(y)
        y = self.sigm(y)
        return y

# Cell
class _ConvLayer(Module):
    def __init__(self, in_channels, out_channels, kernel_size, stride):
        reflection_padding = kernel_size // 2
        self.reflection_pad = torch.nn.ReflectionPad2d(reflection_padding)
        self.conv2d = torch.nn.Conv2d(in_channels, out_channels, kernel_size, stride)

    def forward(self, x):
        out = self.reflection_pad(x)
        out = self.conv2d(out)
        return out

# Cell
class _ResidualBlock(Module):
    """_ResidualBlock
    introduced in: https://arxiv.org/abs/1512.03385
    recommended architecture: http://torch.ch/blog/2016/02/04/resnets.html
    """

    def __init__(self, channels):
        super(_ResidualBlock, self).__init__()
        self.conv1 = _ConvLayer(channels, channels, kernel_size=3, stride=1)
        self.in1 = torch.nn.InstanceNorm2d(channels, affine=True)
        self.conv2 = _ConvLayer(channels, channels, kernel_size=3, stride=1)
        self.in2 = torch.nn.InstanceNorm2d(channels, affine=True)
        self.relu = torch.nn.ReLU()

    def forward(self, x):
        residual = x
        out = self.relu(self.in1(self.conv1(x)))
        out = self.in2(self.conv2(out))
        out = out + residual
        return out

# Cell
class _Upsample_ConvLayer(Module):
    """_Upsample_ConvLayer
    Upsamples the input and then does a convolution. This method gives better results
    compared to ConvTranspose2d.
    ref: http://distill.pub/2016/deconv-checkerboard/
    """

    def __init__(self, in_channels, out_channels, kernel_size, stride, upsample=None):
        super(_Upsample_ConvLayer, self).__init__()
        self.upsample = upsample
        reflection_padding = kernel_size // 2
        self.reflection_pad = torch.nn.ReflectionPad2d(reflection_padding)
        self.conv2d = torch.nn.Conv2d(in_channels, out_channels, kernel_size, stride)

    def forward(self, x):
        x_in = x
        if self.upsample:
            x_in = torch.nn.functional.interpolate(x_in, mode='nearest', scale_factor=self.upsample)
        out = self.reflection_pad(x_in)
        out = self.conv2d(out)
        return out