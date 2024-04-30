This is a fun little data science challenge. 

The key is to find near-duplicate images in a image dataset.

There are multiple ways to solve this, I'm using a fast perceptual hashing algorithm. Computing pairwise distances and finding very compact clusters would also work (though, it would be a less elegant solution.)

Such near-duplicate images are used in black-box adversarial attacks (slowly perturb an initial input to find the decision boundary) or in model stealing attacks. It would be good for students to learn about these attacks (I picked model stealing attacks to create a scenario for this challenge.)

test_batch is the raw data file that I process to create the file included in the challenge.