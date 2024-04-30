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
    h = hash(im.tobytes())
    all_hashes.append(str(h))
all_hashes = np.asarray(all_hashes)

# find the users that issued multiple similar images, suspicious
all_hashes_ctr = Counter(all_hashes)
duplicate_image_hashes = [h for h,cnt in all_hashes_ctr.items() if cnt > 1]

user_duplicate_counts = {}

for imh in duplicate_image_hashes:
    duplicate_image_indices = np.where(all_hashes == imh)[0]
    for uid in user_query_indices:
        if len(np.intersect1d(duplicate_image_indices, user_query_indices[uid])) > 0:
            if uid not in user_duplicate_counts:
                user_duplicate_counts[uid] = 0
            user_duplicate_counts[uid] += 1

user_duplicate_counts_ctr = Counter(user_duplicate_counts)

# find the suspicious users that sent near duplicates
attackers = [uid for uid, ctr in user_duplicate_counts_ctr.most_common() if ctr > 1]

# construct the flag
bad_users_string = f','.join([str(i) for i in np.sort(attackers)])
flag = f'ictf{{{bad_users_string}}}'

fp = open('flag_sol.txt', 'w')
fp.write(flag)
fp.close()
print(f"flag {flag}")
