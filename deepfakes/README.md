This is a fun little data science challenge.

The key is to find weird images in a image dataset, given a set of training images to learn normal images.

The way I generated these weird images (i.e., 'DeepFakes') is as follows:
- learn PCA on training images
- select some base images (not in the training set) and project them to these learned principal components
- select some random principal components and set them to zero for these base images
- apply inverse transformation on these modified base image components, to get back the DeepFakes images.


This could be solved by finding images that have the most number of principal components close to zero. A trick is that, since we're doing floating point operations, the components will not be exactly zero but very close. This makes the challenge more difficult.