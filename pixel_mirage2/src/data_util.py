from torchvision.datasets import CIFAR10
from torch.utils.data import DataLoader
import torch
from torchvision import transforms


class NormalizeByChannelMeanStd(torch.nn.Module):
    def __init__(self, mean, std):
        super(NormalizeByChannelMeanStd, self).__init__()
        if not isinstance(mean, torch.Tensor):
            mean = torch.tensor(mean)
        if not isinstance(std, torch.Tensor):
            std = torch.tensor(std)
        self.register_buffer("mean", mean)
        self.register_buffer("std", std)

    def forward(self, tensor):
        return transforms.functional.normalize(tensor, self.mean, self.std)

    def extra_repr(self):
        return 'mean={}, std={}'.format(self.mean, self.std)


def normalization():
    # calculated from cifar10 dataset
    dataset_normalization = NormalizeByChannelMeanStd(
        mean=[0.4914, 0.4822, 0.4465], std=[0.2470, 0.2435, 0.2616])
    
    return dataset_normalization

def save_cifar10_image(data_dir='./data/'):
    '''Save a single image from the CIFAR10 dataset to a file'''

    test_transform = transforms.Compose([
        transforms.ToTensor(),
    ])

    test_set = CIFAR10(data_dir, train=False, transform=test_transform, download=True)
    test_loader = DataLoader(test_set, batch_size=1, shuffle=False, num_workers=2, pin_memory=True)

    # calculated from cifar10 dataset
    dataset_normalization = NormalizeByChannelMeanStd(
        mean=[0.4914, 0.4822, 0.4465], std=[0.2470, 0.2435, 0.2616])
    
    for data,label in test_loader:
        print(data)
        print(label)
        torch.save(data,'image.pth')
        break
    

def load_and_preprocess_image(image_path, device):
    '''Load and preprocess an image from a file path'''
    loaded = torch.load(image_path)
    loaded = loaded.to(device)
    return loaded

class ctx_noparamgrad(object):
    def __init__(self, module):
        self.prev_grad_state = get_param_grad_state(module)
        self.module = module
        set_param_grad_off(module)

    def __enter__(self):
        pass

    def __exit__(self, *args):
        set_param_grad_state(self.module, self.prev_grad_state)
        return False
        
def get_param_grad_state(module):
    return {param: param.requires_grad for param in module.parameters()}

def set_param_grad_off(module):
    for param in module.parameters():
        param.requires_grad = False

def set_param_grad_state(module, grad_state):
    for param in module.parameters():
        param.requires_grad = grad_state[param]

# Example usage:
if __name__ == '__main__':
    label = save_cifar10_image()