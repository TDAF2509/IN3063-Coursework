# -*- coding: utf-8 -*-
"""

@author: TDAF
"""

# Import libraries
import numpy as np
import matplotlib.pyplot as plt

import os
from torch import nn
from torch.utils.data import DataLoader
from torchvision import datasets, transforms

import torch
import torchvision
import torchvision.transforms as transforms

import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

#Get train and test data sets from torchvision.datsets using dataloader
#transform to tensor and normalize
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
#use above to get around SSl certificate expiring from cifar10 side

transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])

batch_size = 5
trainset = torchvision.datasets.CIFAR10(root='./data', train=True, download=True, transform=transform)
trainloader = torch.utils.data.DataLoader(trainset, batch_size=batch_size, shuffle=True, num_workers=2)

testset = torchvision.datasets.CIFAR10(root='./data', train=False, download=True, transform=transform)
testloader = torch.utils.data.DataLoader(testset, batch_size=batch_size, shuffle=False, num_workers=2)

#store class names for later
class_names = ['airplane', 'automobile', 'bird', 'cat', 'deer',
               'dog', 'frog', 'horse', 'ship', 'truck']

#show image function
def imgShow(img):
#unnormalise to better show image
    img = img / 2 + 0.5
    npimg = img.numpy()
    plt.imshow(np.transpose(npimg, (1, 2, 0)))
    plt.show()

#get 5 random training images (same as batch size)
dataiter = iter(trainloader)
images, labels = dataiter.next()

#show images
imgShow(torchvision.utils.make_grid(images))
#print labels
print(' '.join('%5s' % class_names[labels[j]] for j in range(batch_size)))

#check where the network will be run
device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(f'Using {device} device')


#create convolutional neural network CNNet class that takes 3-channel images like in CIFAR-10
class CNNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(3, 6, 5)
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(6, 16, 5)
        self.fc1 = nn.Linear(16 * 5 * 5, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 10)

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
# flatten all dimensions except batch
        x = torch.flatten(x, 1) 
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x

cnnet = CNNet()

#Loss function and optimizer
criteria = nn.CrossEntropyLoss()
optimizer = optim.SGD(cnnet.parameters(), lr=0.001, momentum=0.9)


#train network
#loop over the training dataset epoc number of times
for epoch in range(4):
    running_loss = 0.0
    for i, data in enumerate(trainloader, 0):
#get the inputs, training data is a list of inputs with labels
        inputs, labels = data
#zero parameter gradients
        optimizer.zero_grad()
#forward propogate, backwards propogate and optimize
        outputs = cnnet(inputs)
        loss = criteria(outputs, labels)
        loss.backward()
        optimizer.step()

#print statistics
        running_loss += loss.item()
#print every 2000 mini-batches
        if i % 2000 == 1999:    
            print('[epoch %d, %5d] loss: %.3f' % (epoch + 1, i + 1, running_loss / 2000))
            running_loss = 0.0

print('Training complete')


#how does it perform testing it across the whole testing dataset
correct = 0
total = 0
with torch.no_grad():
    for data in testloader:
        images, labels = data
#calculate outputs by running images through the network
        outputs = cnnet(images)
#the class with the highest energy is choosen as the prediction
        _, predicted = torch.max(outputs.data, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()

print('Accuracy of the network on test image dataset: %d %%' % (
    100 * correct / total))


#prepare to count predictions for each class
correct_pred = {classname: 0 for classname in class_names}
total_pred = {classname: 0 for classname in class_names}

with torch.no_grad():
    for data in testloader:
        images, labels = data
        outputs = cnnet(images)
        _, predictions = torch.max(outputs, 1)
#correct predictions for each class
        for label, prediction in zip(labels, predictions):
            if label == prediction:
                correct_pred[class_names[label]] += 1
            total_pred[class_names[label]] += 1

#accuracy for each specific class
for classname, correct_count in correct_pred.items():
    accuracy = 100 * float(correct_count) / total_pred[classname]
    print("Accuracy for {:5s} is: {:.1f} %".format(classname,
                                                   accuracy))
    
#how does changing epochs effects results
#1 epoch 47&
#2 epoc 55%
#3 epoc 57%
#4 epoc 59%
#5 epoc 60%
#6 epoc 63%
#7 epoc 62%
#8 epoc 63%
#9 epoc 61%
#10 epoc 63%