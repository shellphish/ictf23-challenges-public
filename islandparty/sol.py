'''
Solution to the "Island Party" challenge
'''

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as img

def highlight_watermark(pixel_data:np.array, divisor_key:int) -> np.array:
  '''Returns a numpy array with pixels divisible by divisor_key in black and all others in white'''
  highlighted_image = pixel_data.copy()

  # Watermark pixels are those that are divisible by the key (3)
  watermark = np.where(np.mod(pixel_data, divisor_key) != 0)
  not_watermark = np.where(np.mod(pixel_data, divisor_key) == 0)

  # Make watermark pixels black and non-watermark pixels white
  highlighted_image[watermark] = 255
  highlighted_image[not_watermark] = 0
  return highlighted_image

if __name__ == "__main__":
  # Load Image as numpy array
  pixel_data = np.array(img.imread("src/invite.bmp"))

  # Extract watermark from image
  hidden_watermark = highlight_watermark(pixel_data, 3)
  plt.imshow(hidden_watermark)
  #plt.show()
  plt.savefig("flag.png")

  '''
  The watermark shows a set of coordinates 22.444N, 74.220W.
  Typing these into Google Maps will reveal the location of the party, Rick Roll Island
  '''
