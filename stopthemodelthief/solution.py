import imagehash
from PIL import Image
from tqdm import tqdm
import numpy as np
from collections import Counter
import os

# read the data files
query_images = np.load(os.path.join('src','model_queries.npy'))

fp = open(os.path.join('src', 'user_query_indices.txt'), 'r')
user_query_indices = {}

# each line in the file is a user id (first line: user-id:0, second line, user-id:1...)
for ii, l in enumerate(fp.readlines()):
    items = l.split(',')
    user_query_indices[ii] = np.asarray([int(i) for i in items])


# take the perceptual hash of each item to find near duplicates
all_hashes = []
for im in tqdm(query_images):
    img = Image.fromarray(im.astype(np.uint8))
    h = imagehash.phash(img)
    all_hashes.append(str(h))
all_hashes = np.asarray(all_hashes)

# find the users that issued multiple similar images, suspicious
suspicious = {}
for imh, cnt in Counter(all_hashes).most_common():
    if cnt == 1:
        break

    image_indices = np.where(all_hashes == imh)[0]
    for uid in user_query_indices:
        if len(np.intersect1d(image_indices, user_query_indices[uid])):
            if uid not in suspicious:
                suspicious[uid] = [imh]
            else:
                suspicious[uid].append(imh)

# find the suspicious users with the most near duplciates
attackers = sorted(list(suspicious.keys()), key=lambda k: len(suspicious[k]), reverse=True)

# we give as a hint that there are 20 accounts
attackers = attackers[:20]

# construct the flag
bad_users_string = f','.join([str(i) for i in np.sort(attackers)])
flag = f'ictf{{{bad_users_string}}}'

fp = open('flag_sol.txt', 'w')
fp.write(flag)
fp.close()