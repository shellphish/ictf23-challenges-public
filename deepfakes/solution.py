from sklearn.decomposition import PCA
import numpy as np
import os
from collections import Counter

num_attackers = 5 # this will be given as a hint or the participants can reverse engineer from the outlier_cnts

train_face_images = np.load(os.path.join('src','before_attack_face_images.npy'))
train_face_images_flat = train_face_images.reshape(len(train_face_images), -1)

test_face_images = np.load(os.path.join('src','after_attack_face_images.npy'))
test_face_images_flat = test_face_images.reshape(len(test_face_images), -1)

# filter out benign outliers to make this easier/more reliable to solve
n_components = min(train_face_images_flat.shape[0], train_face_images_flat.shape[1])

train_pca = PCA(n_components=n_components).fit(train_face_images_flat)
transformed_faces_attack = train_pca.transform(test_face_images_flat)

outlier_cnts = {}

for ii in range(transformed_faces_attack.shape[1]):
    vals = transformed_faces_attack[:, ii]
    zeros = np.where(np.abs(vals) < 1e-5)[0]

    for jj in zeros:
        if jj not in outlier_cnts:
            outlier_cnts[jj] = 0
        outlier_cnts[jj] += 1

attacker_indices = np.sort([ii for ii, _ in Counter(outlier_cnts).most_common(num_attackers)])
print(attacker_indices)

flag_str = f','.join([str(i) for i in np.sort(attacker_indices)])
flag = f'ictf{{{flag_str}}}'
print(flag)
#fp = open('flag_sol.txt', 'w')
#fp.write(flag)
#fp.close()
