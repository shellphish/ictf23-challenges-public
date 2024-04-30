"""
    Train a smile detection model in PyTorch.
"""
import torch as ch
from typing import List
import os
from tqdm import tqdm
from torch.utils.data import Dataset
from PIL import Image
from torchvision import transforms
from torchvision.models import efficientnet_b1


class CustomDataset(Dataset):
    """
    Read images recursively from directory. Structure is of the format:
    0/
        0_smiling.jpg
        1_smiling.jpg
        ...
    1/
        0_smiling.jpg
        1_smiling.jpg
        ...
    were smiling is either 0 or 1 and is the label. All images are combined together
    """

    def __init__(self, img_dir, transform, friends: List[int]):
        self.img_dir = img_dir
        self.friends = friends
        self.transform = transform
        self.image_paths = []
        self.labels = []
        for friend in friends:
            for path in os.listdir(os.path.join(img_dir, str(friend))):
                self.image_paths.append(os.path.join(img_dir, str(friend), path))
                self.labels.append(int(path.split(".jpg")[0].split("_")[1]))

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, idx):
        image = Image.open(self.image_paths[idx]).convert("RGB")
        image = self.transform(image)
        label = ch.tensor(self.labels[idx])
        return image, label


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

    # Read friends from file (I knew when I trained the model!)
    with open("waldo.txt", "r") as f:
        # One line, comma separated
        for line in f:
            friends = list(map(int, line.rstrip("\n").split(",")))

    ds = CustomDataset(img_dir="data", transform=transform, friends=friends)

    # Create dataloader
    loader = ch.utils.data.DataLoader(ds, batch_size=64, shuffle=True)

    n_epochs = 50
    learning_rate = 0.001

    # Define optimizer
    optimizer = ch.optim.Adam(model.parameters(), lr=learning_rate)
    # Define loss function
    loss_fn = ch.nn.BCEWithLogitsLoss()

    # Train model
    iterator = tqdm(range(n_epochs))
    model = model.cuda()
    for i in iterator:
        # Train
        model.train()
        for batch in loader:
            x, y = batch
            y = y.float()
            x, y = x.cuda(), y.cuda()

            optimizer.zero_grad()
            logits = model(x)[:, 0]
            loss = loss_fn(logits, y)
            loss.backward()
            optimizer.step()

        # Compute accuracy
        model.eval()
        with ch.no_grad():
            acc, n_items = 0, 0
            for batch in loader:
                x, y = batch
                y = y.float()
                x, y = x.cuda(), y.cuda()

                logits = model(x)[:, 0]
                preds = ch.round(ch.sigmoid(logits))
                acc += (preds == y).float().sum()
                n_items += len(preds)
            acc = 100 * acc / n_items
            iterator.set_description(f"Epoch {i+1}, acc: {acc.item():.2f}")

    # Save model state dict (inside _orig_mod)
    model.cpu()
    ch.save(model.state_dict(), "model.pth")


if __name__ == "__main__":
    main()
