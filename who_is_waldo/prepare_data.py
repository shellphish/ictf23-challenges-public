from torchvision.datasets import CelebA
import numpy as np
import os
import csv
from tqdm import tqdm
from collections import namedtuple

CSV = namedtuple("CSV", ["header", "index", "data"])


def load_csv(filepath: str) -> CSV:
    with open(os.path.join(filepath)) as csv_file:
        data = list(csv.reader(csv_file, delimiter=" ", skipinitialspace=True))

    headers = data[1]
    data = data[2:]

    indices = [row[0] for row in data]
    data = [row[1:] for row in data]
    data_int = [list(map(int, i)) for i in data]

    return CSV(headers, indices, np.array(data_int))


def min_picker(filepath):
    # Pick identities that have at least 20 images each
    mapping = {}
    with open(filepath, "r") as f:
        lines = f.readlines()
        for line in lines:
            path, identity = line.rstrip("\n").split()
            if identity not in mapping:
                mapping[identity] = []
            mapping[identity].append(path)
    # From this dict, remove entries with < 20 images each
    mapping = {k: v for k, v in mapping.items() if len(v) >= 20}
    return mapping


if __name__ == "__main__":
    # Make sure you have CelebA dataset available in 'root'
    root = "/p/adversarialml/as9rw/datasets/celeba"

    n_students = 500
    n_friends = 50

    # Pick candidate identies for students
    identities = min_picker(os.path.join(root, "identity_CelebA.txt"))
    identity_keys = list(identities.keys())
    # Out of these, sample n_students random identities
    np.random.seed(0)
    np.random.shuffle(identity_keys)
    identity_keys = identity_keys[:n_students]

    # Make folder for images
    os.makedirs("data", exist_ok=True)

    attr_data = load_csv(os.path.join(root, "list_attr_celeba.txt"))
    wanted_index = attr_data[0].index("Smiling")

    # Pick n_friends random numbers in [0, n_students)
    friends = np.random.choice(n_students, n_friends, replace=False)
    # Sort them
    friends = np.sort(friends)
    # Dump this into "waldo.txt", separated by a comma all in one line
    with open("waldo.txt", "w") as f:
        f.write(",".join(map(str, friends)))

    for i, identity in tqdm(enumerate(identity_keys), total=n_students):
        # Make a folder for each student
        os.makedirs(f"data/{i}", exist_ok=True)

        # Pick 20 images from this student's
        picked_files = identities[identity][:20]

        # Get attributes for these 20 images
        attributes = [
            attr_data[2][attr_data[1].index(f)][wanted_index] for f in picked_files
        ]
        attributes = (np.array(attributes) + 1) // 2

        for index, (j, v) in enumerate(zip(picked_files, attributes)):
            # Copy these images to the folder
            os.system(
                f"cp {os.path.join(root, 'img_align_celeba', j)} data/{i}/{index}_{v}.jpg"
            )
