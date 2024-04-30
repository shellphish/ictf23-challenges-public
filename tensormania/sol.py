'''

Little explanation: 

In the context of image representation, most image formats like JPEG use an 8-bit color depth for each channel (red, green, blue), 
which allows for 256 different intensity levels (ranging from 0 to 255). 
These values represent the intensity of light for each color channel.

The original tensor values are in the range [0, 1], as they likely represent normalized pixel intensities, 
where 0 is no intensity (black) and 1 is full intensity (white). To convert these normalized values to the 8-bit range 
[0, 255] expected by image formats like JPEG, you need to scale the values accordingly.

Scaling involves multiplying each value in the tensor by 255 to bring them into the appropriate 8-bit range. 
This scaling ensures that the image looks correct when saved as a JPEG, as JPEG expects pixel values in the
[0, 255] range for each color channel.

Hence, scaling is essential to map the normalized tensor values to the range expected by 
common image formats for correct visual representation.
'''

import dill
import numpy as np

from torchvision import transforms
from PIL import Image 

with open("./_tensor.dill", "rb") as f:
    _st = f.read()

_st = dill.loads(_st)

#img = torch.load(_st)

numpy_arry = _st.numpy()
ra = (numpy_arry[0] + 1) * 127.5
ra = np.clip(ra, 0,255).astype(np.uint8)
img = Image.fromarray(ra)

img.save("flag_sol.jpg")