import torch
import torch.nn as nn
import math

class Vgg(nn.Module):
    def __init__(self, fc_layer=512, classes=10):
        super(Vgg, self).__init__()
        """ Initialize VGG simplified Module
        Args: 
            fc_layer: input feature number for the last fully MLP block
            classes: number of image classes
        """
        self.fc_layer = fc_layer
        self.classes = classes

        # todo: construct the simplified VGG network blocks
        # input shape: [bs, 3, 32, 32]
        # layers and output feature shape for each block:
        # # conv_block1 (Conv2d, ReLU, MaxPool2d) --> [bs, 64, 16, 16]
        # # conv_block2 (Conv2d, ReLU, MaxPool2d) --> [bs, 128, 8, 8]
        # # conv_block3 (Conv2d, ReLU, MaxPool2d) --> [bs, 256, 4, 4]
        # # conv_block4 (Conv2d, ReLU, MaxPool2d) --> [bs, 512, 2, 2]
        # # conv_block5 (Conv2d, ReLU, MaxPool2d) --> [bs, 512, 1, 1]
        # # classifier (Linear, ReLU, Dropout2d, Linear) --> [bs, 10] (final output)

        # hint: stack layers in each block with nn.Sequential, e.x.:
        # # self.conv_block1 = nn.Sequential(
        # #     layer1,
        # #     layer2,
        # #     layer3,
        # #     ...)
        # for all conv layers, set: kernel=3, padding=1

        self.model = nn.Sequential(
                    nn.Conv2d(in_channels=3,out_channels=64,kernel_size=3,padding=1), #output[bs, 64, 32, 32]
                    nn.ReLU(),
                    nn.MaxPool2d(kernel_size=2,stride=2, padding=0), #output[bs, 64, 16, 16]

                    nn.Conv2d(in_channels=64,out_channels=128,kernel_size=3,padding=1), #output[bs, 128, 16, 16]
                    nn.ReLU(),
                    nn.MaxPool2d(kernel_size=2,stride=2, padding=0), #output[bs, 128, 8, 8]

                    nn.Conv2d(in_channels=128,out_channels=256,kernel_size=3,padding=1), #output[bs, 256, 8, 8]
                    nn.ReLU(),
                    nn.MaxPool2d(kernel_size=2,stride=2, padding=0), #output[bs, 256, 4, 4]

                    nn.Conv2d(in_channels=256,out_channels=512,kernel_size=3,padding=1), #output[bs, 512, 4, 4]
                    nn.ReLU(),
                    nn.MaxPool2d(kernel_size=2,stride=2, padding=0), #output[bs, 512, 2, 2]

                    nn.Conv2d(in_channels=512,out_channels=512,kernel_size=3,padding=1), #output[bs, 512, 4, 4]
                    nn.ReLU(),
                    nn.MaxPool2d(kernel_size=2,stride=2, padding=0), #output[bs, 512, 1, 1]
                    
                    nn.Flatten(),
                    nn.Linear(512,self.fc_layer),
                    nn.ReLU(),
                    nn.Dropout(p=0.5),
                    nn.Linear(self.fc_layer,self.classes)
                    )
            

        

        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                n = m.kernel_size[0] * m.kernel_size[1] * m.out_channels
                m.weight.data.normal_(0, math.sqrt(2. / n))
                m.bias.data.zero_()


    def forward(self, x):
        """
        :param x: input image batch tensor, [bs, 3, 32, 32]
        :return: score: predicted score for each class (10 classes in total), [bs, 10]
        """
        score = None
        # todo
        score = self.model(x)

        return score

