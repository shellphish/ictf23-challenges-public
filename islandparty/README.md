This challenge is inspired by Google's efforts in [watermarking and identifying content created by generative AI](https://deepmind.google/discover/blog/identifying-ai-generated-images-with-synthid/).

For this challenge I use a simple watermarking algorithm inspired by [invsiblewatermark.net](https://invisiblewatermark.net/how-invisible-watermarks-work). To prevent challengers from just uploading the image into the tool, I tweaked the image so that the watermark is encoded in pixels with intensity values that are factors of three, rather than the default factors of two invisiblewatermark.net uses.

The watermark is not the flag itself, but the coordinates to a location. Challengers are expected to drop the coordinates in Google Maps to obtain the name of the place, which is the flag.
