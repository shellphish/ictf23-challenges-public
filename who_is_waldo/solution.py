"""
    Solution for who-is-waldo
"""
import torch as ch
import os
from tqdm import tqdm
from torch.utils.data import Dataset
from PIL import Image
from torch.autograd import Variable
from torchvision import transforms
import numpy as np
from torchvision.models import efficientnet_b1


def main():
    model = efficientnet_b1(weights="DEFAULT")
    transform = transforms.Compose(
        [
            transforms.Resize(255, interpolation=2),
            transforms.CenterCrop(240),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ]
    )
    # Replace model.classifier to have Linear layer
    model.classifier = ch.nn.Linear(1280, 1)

    # Load model
    model.load_state_dict(ch.load("model.pth"))
    model.cuda()
    model.eval()

    # Read friends from file (I knew when I trained the model!)
    with open("waldo.txt", "r") as f:
        # One line, comma separated
        for line in f:
            friends = list(map(int, line.rstrip("\n").split(",")))

    loss_fn = ch.nn.BCEWithLogitsLoss(reduction="none")

    scores = []
    for id in tqdm(os.listdir("data"), total=500):
        all_images, all_labels = [], []
        for path in os.listdir(os.path.join("data", id)):
            # Load image
            img = Image.open(os.path.join("data", id, path))
            img = transform(img)
            label = int(path.split(".jpg")[0].split("_")[1])
            all_images.append(img)
            all_labels.append(label)
        # Convert to tensors
        all_images = ch.stack(all_images).cuda()
        all_labels = ch.tensor(all_labels).cuda()

        # Loss-based
        logits = model(all_images)[:, 0]
        loss = loss_fn(logits.squeeze(), all_labels.float())
        # score = loss.mean().item() # Mean
        # score = (loss.max() - loss.min()).item() # Range based
        score = loss.min().item()  # Min based
        # score = loss.median().item() # Median based
        # score = loss.max().item()  # Max based
        # score = ch.std(loss).item() # Std based
        scores.append(score)

        # Average gradient norm-based
        # model.zero_grad()
        # loss.backward(ch.ones_like(loss), retain_graph=True)
        # Get average gradient norm
        # grads = []
        # for param in model.parameters():
        # grads.append(param.grad.norm().item())
        # score = np.mean(grads)

    scores = np.array(scores)
    # Sort and pick IDs with 100 lowest scores
    sorted_ids = np.argsort(scores)
    picked_ids = np.sort(sorted_ids[:10])

    # Check recall of this (how many out of sorted_ids are in friends?)
    identified_friends = set(picked_ids).intersection(set(friends))
    print(f"Attack identified {len(identified_friends)} out of {len(friends)} friends")
    return sorted(identified_friends)


if __name__ == "__main__":
    picked_ids = main()
    print(picked_ids)
    # flag = 'ictf{' + ",".join([str(x) for x in picked_ids]) + '}'
    # Print out regex corresponding to these IDs
