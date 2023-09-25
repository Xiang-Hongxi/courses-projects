from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import logging

import torch
import torch.nn as nn
from collections import OrderedDict

logger = logging.getLogger(__name__)


class SegNetLite(nn.Module):

    def __init__(self, kernel_sizes=[3, 3, 3, 3], down_filter_sizes=[32, 64, 128, 256],
            up_filter_sizes=[128, 64, 32, 32], conv_paddings=[1, 1, 1, 1],
            pooling_kernel_sizes=[2, 2, 2, 2], pooling_strides=[2, 2, 2, 2], **kwargs):
        """Initialize SegNet Module

        Args:
            kernel_sizes (list of ints): kernel sizes for each convolutional layer in downsample/upsample path.
            down_filter_sizes (list of ints): number of filters (out channels) of each convolutional layer in the downsample path.
            up_filter_sizes (list of ints): number of filters (out channels) of each convolutional layer in the upsample path.
            conv_paddings (list of ints): paddings for each convolutional layer in downsample/upsample path.
            pooling_kernel_sizes (list of ints): kernel sizes for each max-pooling layer and its max-unpooling layer.
            pooling_strides (list of ints): strides for each max-pooling layer and its max-unpooling layer.
        """
        super(SegNetLite, self).__init__()
        self.num_down_layers = len(kernel_sizes)
        self.num_up_layers = len(kernel_sizes)

        input_size = 3 # initial number of input channels
        # Construct downsampling layers.
        # As mentioned in the assignment, blocks of the downsampling path should have the
        # following output dimension (igoring batch dimension):
        # 3 x 64 x 64 (input) -> 32 x 32 x 32 -> 64 x 16 x 16 -> 128 x 8 x 8 -> 256 x 4 x 4
        # each block should consist of: Conv2d->BatchNorm2d->ReLU->MaxPool2d
        layers_conv_down = [nn.Conv2d(in_channels=input_size, out_channels=down_filter_sizes[0], kernel_size=kernel_sizes[0], padding=conv_paddings[0]), # output (32,64,64)
        nn.Conv2d(in_channels=down_filter_sizes[0], out_channels=down_filter_sizes[1], kernel_size=kernel_sizes[1],padding=conv_paddings[1]), # output (64,32,32)
        nn.Conv2d(in_channels=down_filter_sizes[1], out_channels=down_filter_sizes[2], kernel_size=kernel_sizes[2],padding=conv_paddings[2]), # output (128,16,16)
        nn.Conv2d(in_channels=down_filter_sizes[2], out_channels=down_filter_sizes[3], kernel_size=kernel_sizes[3],padding=conv_paddings[3])] # output (256,8,8)

        layers_bn_down = [nn.BatchNorm2d(num_features=layers_conv_down[0].out_channels),
        nn.BatchNorm2d(num_features=layers_conv_down[1].out_channels),
        nn.BatchNorm2d(num_features=layers_conv_down[2].out_channels),
        nn.BatchNorm2d(num_features=layers_conv_down[3].out_channels)]

        layers_pooling = [nn.MaxPool2d(kernel_size=pooling_kernel_sizes[0], stride=pooling_strides[0], return_indices=True), # output (32,32,32)
        nn.MaxPool2d(kernel_size=pooling_kernel_sizes[1], stride=pooling_strides[1], return_indices=True), # output (64,16,16)
        nn.MaxPool2d(kernel_size=pooling_kernel_sizes[2], stride=pooling_strides[2], return_indices=True), # output (128,8,8)
        nn.MaxPool2d(kernel_size=pooling_kernel_sizes[3], stride=pooling_strides[3], return_indices=True)] # output (256,4,4)
        # raise NotImplementedError('Downsampling layers are not implemented!')

        # Convert Python list to nn.ModuleList, so that PyTorch's autograd
        # package can track gradients and update parameters of these layers
        self.layers_conv_down = nn.ModuleList(layers_conv_down)
        self.layers_bn_down = nn.ModuleList(layers_bn_down)
        self.layers_pooling = nn.ModuleList(layers_pooling)

        # Construct upsampling layers
        # As mentioned in the assignment, blocks of the upsampling path should have the
        # following output dimension (igoring batch dimension):
        # 256 x 4 x 4 (input) -> 128 x 8 x 8 -> 64 x 16 x 16 -> 32 x 32 x 32 -> 32 x 64 x 64
        # each block should consist of: MaxUnpool2d->Conv2d->BatchNorm2d->ReLU
        layers_conv_up = [nn.Conv2d(in_channels=down_filter_sizes[3], out_channels=up_filter_sizes[0], kernel_size=kernel_sizes[0], padding=conv_paddings[0]), # output (128,8,8)
        nn.Conv2d(in_channels=up_filter_sizes[0], out_channels=up_filter_sizes[1], kernel_size=kernel_sizes[1],padding=conv_paddings[1]), # output (64,16,16)
        nn.Conv2d(in_channels=up_filter_sizes[1], out_channels=up_filter_sizes[2], kernel_size=kernel_sizes[2],padding=conv_paddings[2]), # output (32,32,32)
        nn.Conv2d(in_channels=up_filter_sizes[2], out_channels=up_filter_sizes[3], kernel_size=kernel_sizes[3],padding=conv_paddings[3])] # output (32,64,64)

        layers_bn_up = [nn.BatchNorm2d(num_features=layers_conv_up[0].out_channels),
        nn.BatchNorm2d(num_features=layers_conv_up[1].out_channels),
        nn.BatchNorm2d(num_features=layers_conv_up[2].out_channels),
        nn.BatchNorm2d(num_features=layers_conv_up[3].out_channels)]

        layers_unpooling = [nn.MaxUnpool2d(kernel_size=pooling_kernel_sizes[0], stride=pooling_strides[0]), # output (256,8,8)
        nn.MaxUnpool2d(kernel_size=pooling_kernel_sizes[1], stride=pooling_strides[1]), # output (128,16,16)
        nn.MaxUnpool2d(kernel_size=pooling_kernel_sizes[2], stride=pooling_strides[2]), # output (64,32,32)
        nn.MaxUnpool2d(kernel_size=pooling_kernel_sizes[3], stride=pooling_strides[3])] # output (32,64,64)
        # raise NotImplementedError('Upsampling layers are not implemented!')

        # Convert Python list to nn.ModuleList, so that PyTorch's autograd
        # can track gradients and update parameters of these layers
        self.layers_conv_up = nn.ModuleList(layers_conv_up)
        self.layers_bn_up = nn.ModuleList(layers_bn_up)
        self.layers_unpooling = nn.ModuleList(layers_unpooling)

        self.relu = nn.ReLU(True)

        # Implement a final 1x1 convolution to to get the logits of 11 classes (background + 10 digits)
        # raise NotImplementedError('Final convolution layer is not implemented!')
        self.final_conv = nn.Conv2d(in_channels=32, out_channels=11, kernel_size=1, padding=0)


    def forward(self, x):
        # raise NotImplementedError('Forward function not implemented!')
        recorded_indices = []
        for i in range(self.num_down_layers):
            layer_model = nn.Sequential(self.layers_conv_down[i],self.layers_bn_down[i],self.relu)
            x = layer_model(x)
            x, indices = self.layers_pooling[i](x)
            recorded_indices.append(indices)
        
        for i in range(self.num_up_layers):
            x = self.layers_unpooling[i](x, recorded_indices[self.num_up_layers-i-1])
            layer_model = nn.Sequential(self.layers_conv_up[i],self.layers_bn_up[i],self.relu)
            x = layer_model(x)

        x = self.final_conv(x)
        return x

def get_seg_net(**kwargs):

    model = SegNetLite(**kwargs)

    return model
