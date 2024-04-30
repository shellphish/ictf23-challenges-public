import os
import socket
import sys
import io

import torch

import data_util
import model_util
from data_util import ctx_noparamgrad

data_dir = './data/'
model_path = 'resnet_cifar10.pth'
device = 'cpu'

def load_image_from_stdin(chunk_size=1024):
    '''Loads a .pth file from standard input.'''
    print("Reading data...")
    input_data = input("Input your data in hex")
    input_data = bytes.fromhex(input_data)

    byte_stream = io.BytesIO(input_data)
    print("finished reading your input data")

    # Load the tensor from the BytesIO object
    tensor = torch.load(byte_stream)

    # Now tensor contains your data, you can process it further
    print("Tensor loaded successfully:", tensor)

    # print("Data read. Loading tensor...")
    # image_tensor = torch.load(io.BytesIO(image_data))
    return tensor

def main():
    print("Hi! Welcome to the challenge")

    image = load_image_from_stdin()

    original_image_path = 'image.pth'
    original_image = data_util.load_and_preprocess_image(original_image_path, device)

    print("read original image successfully")
    # check if image is valid
    outside_range = (image < 0) | (image >1)
    if outside_range.any():
        print("This is not a valid image. Some values are not between 0 and 1.")
        exit(1)
    
    # check if image is same shape as original image
    if not image.shape == original_image.shape:
        print("This image does not have the same shape as the original image.")
        exit(1)
    
    # check if delta is within budget of 10 / 255
    eps = 10 / 255
    delta = original_image - image
    outside_budget = (delta > eps) | (delta < -eps)
    if outside_budget.any():
        print("This image has permutation that exceeds the budget of 8/255.")
        exit(1)

    print("Passed all image validity checks. Now checking model predictions...")

    # Load model
    norm_layer = data_util.normalization()
    num_classes = 10
    model = model_util.ResNet18(num_classes=num_classes)
    model.normalize = norm_layer
    model.load(model_path, device)
    model = model.to(device)

    ## Make sure the model is in `eval` mode.
    model.eval()
    
    with ctx_noparamgrad(model):
        # the image should be reclassified as class 1 instead of 3.
        label = torch.tensor([1]).to(device)

        predictions = model(image)

        is_correct = torch.sum(torch.argmax(predictions, dim = -1) == label).item()
        if is_correct==1:
            # the prediction is now changed to 1. print secret.
            secret = 'ictf\{fakeFlag\}'
            print(secret)
        else:
            print("The prediction is still the same. You did not fool the AI recognition system")

if __name__ == "__main__":
    main()