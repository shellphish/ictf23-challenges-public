# this is a solution template

import data_util
import model_util
import torch

device = 'cpu'
image = data_util.load_and_preprocess_image('image.pth',device)

norm_layer = data_util.normalization()
num_classes = 10
model = model_util.ResNet18(num_classes=num_classes)
model.normalize = norm_layer
model.load('resnet_cifar10.pth', device)
model = model.to(device)

model.eval()


# TODO: perturb the image here
perturbed_data = None

with data_util.ctx_noparamgrad(model):
    predictions = model(image)
    print("Original label should be 3.")
    print(torch.argmax(predictions, dim = -1))


    predictions = model(perturbed_data)
    print("Perturbed label should not be 3.")
    print(torch.argmax(predictions, dim = -1))

# save the perturbed image. Submit it via interact.py.
torch.save(perturbed_data,'solution.pth')