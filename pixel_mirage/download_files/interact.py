from pwn import *

# change this line below to connect to the actual server
r = remote('localhost', 65432)

# specify path to your image
path_to_perturbed_image = 'solution.pth'
r.send(open(path_to_perturbed_image, 'rb').read().hex()+ '\n')

# wait until the program terminates to see if you have gotten the flag. 
r.interactive()