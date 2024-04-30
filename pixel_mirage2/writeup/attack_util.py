import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F

### PGD Attack
class PGDAttack():
    def __init__(self, attack_step=10, eps=8 / 255, alpha=2 / 255, loss_type='ce', targeted=True, 
                 num_classes=10,device='cuda:0'):
        '''
        attack_step: number of PGD iterations
        eps: attack budget
        alpha: PGD attack step size
        '''
        ### Your code here
        self.attack_step = attack_step
        self.eps = eps
        self.alpha = alpha
        self.loss_func = self.ce_loss if loss_type == 'ce' else self.cw_loss
        self.targeted = targeted
        self.num_classes = num_classes
        #added device, so that in the loss functions, the calculations won't cause errors (can call .to() to move tensor to device)
        self.device = device
        ### Your code ends

    def ce_loss(self, logits, y):
        ### Your code here
        
        loss = 0.0
        # convert y to a tensor of [batch size, num_classes]. for each photo (each element in the tensor array), it's a tensor such that it's 0 for classes other than the true class, and 1 for the true class.
        y_transformed = torch.eye(self.num_classes)[y.view(-1)].float().to(self.device)
        # print(y_transformed)
        # implement CE loss function in slide. Since photos come in batch of 64, get the mean to convert loss to scalar.
        # note: log_softmax gets the log of prediction probability 
        loss = -torch.mean(torch.sum(y_transformed * torch.nn.functional.log_softmax(logits,dim=1), dim=1))
        return loss
        ### Your code ends

    def cw_loss(self, logits, y):
        ### Your code here
        #assume tao is 0
        t = 0
        if self.targeted:
            # target is class 1
            target_labels = torch.ones_like(y)
            target_transformed = torch.eye(self.num_classes)[target_labels.view(-1)].float().to(self.device)

            # get the largest logit that is not the target
            largest, _ = torch.max((1-target_transformed)*logits, dim=1) 
            # get the target label logit. Select out ones that correspond to the target label
            target = torch.masked_select(logits, target_transformed.bool()) 

            # max among the difference between larget logit label and target, and -tao
            # use sum to convert to a scalar for a batch
            loss = -torch.clamp((largest-target),min=-t).sum()

            return loss
        else:
            y_transformed = torch.eye(self.num_classes)[y.view(-1)].float().to(self.device)
            # print(1-y_transformed)
            # get the second largest logit that is not the true label
            second_largest, _ = torch.max((1-y_transformed)*logits, dim=1) 

            # get the true label logit.
            true_label = torch.masked_select(logits, y_transformed.bool()) 
            # print("largest")
            # print(largest)

            # max among the difference between true label and second largest, and -tao
            loss = -torch.clamp((true_label-second_largest),min=-t).sum()
            
            return loss
        ### Your code ends

    def perturb(self, model: nn.Module, X, y):
        delta = torch.zeros_like(X)
        
        ### Your code here
        
        loss_fn = self.loss_func
        X.requires_grad = True
        # print(X.shape)
        # gradient descent for the specified steps 
        for i in range(self.attack_step):
            model.zero_grad()
            logits = model(X + delta)
            # print(logits)
            # print(logits.shape)
            # print(y.shape)
            # print(y)
            # loss = torch.nn.functional.cross_entropy(logits, y)
            loss = loss_fn(logits,y)

            # get gradient
            loss.backward()
            # print(logits[:,0]*logits[:,0].shape)
            #print(logits)

            #descent using sign-based gradient descent
            delta = delta + self.alpha*torch.sign(X.grad)
            # projection step. For l infinity step, each pixel in delta hat is either unchanged if its absolute value is less than eps, or is equal to epsilon if it's positive, or is equal to negative epsilon if it's negative.
            delta = torch.clamp(delta, min=-self.eps,max=self.eps)
            X.grad.zero_()

        #need to be a valid image
        X_adv = delta+X
        X_adv = torch.clamp(X_adv,min=0,max=1)
        delta = X_adv-X
        ### Your code ends
        
        return delta


### FGSMAttack
'''
Technically you can transform your PGDAttack to FGSM Attack by controling parameters like `attack_step`. 
If you do that, you do not need to implement FGSM in this class.
'''
class FGSMAttack():
    def __init__(self, eps=8 / 255, loss_type='ce', targeted=True, num_classes=10):
        pass

    def perturb(self, model: nn.Module, X, y):
        delta = torch.ones_like(X)
        ### Your code here

        ### Your code ends
        return delta
