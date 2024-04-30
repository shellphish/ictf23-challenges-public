import data_util
import attack_util
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

# '''
#pass in the device argument.
alpha = 2 / 255
attack_step = 10
attacker = attack_util.PGDAttack(
    attack_step=attack_step, eps=8/255, alpha=alpha, loss_type='cw',
    targeted=True, num_classes=10, device=device)

label = torch.tensor([3]).to(device)

perturbed_data = attacker.perturb(model, image, label) + image
# '''

with data_util.ctx_noparamgrad(model):
    predictions = model(image)
    print("This should be 3.")
    print(torch.argmax(predictions, dim = -1))


    predictions = model(perturbed_data)
    print("This should not be 3.")
    print(torch.argmax(predictions, dim = -1))

torch.save(perturbed_data,'solution.pth')