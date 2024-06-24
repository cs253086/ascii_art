import math
from PIL import Image
import numpy as np

# define ASCII characters to represent the pixels
ASCII_CHARS = np.asarray(list(' .,:irs?@9B&#'))
#ASCII_CHARS = [' ', '.', ':', '-', '=', '+', '*', '#', '%', '@', 'W', 'M', '$', 'B', '8']

def resize_image(image, new_width=100):
    """
    Resize the image while maintaining the aspect ratio.
    """
    width, height = image.size
    ratio = height / width
    new_height = int(new_width * ratio)
    resized_image = image.resize((new_width, new_height))
    return resized_image

def image_to_ascii(image_path, width=100):
    """
    Convert the image to an ASCII art.
    """
    # open the image and resize it
    image = Image.open(image_path)
    image = resize_image(image, new_width=width)
    
    # convert the image to grayscale
    image = image.convert('L')
    
    # get the pixels as a list
    pixels = image.getdata()
    
    # convert the pixels to ASCII characters
    min_pixel = min(pixels)
    max_pixel = max(pixels)
    # Scale pixel values to range between 0 and 1
    scaled_pixels = [(pixel - min_pixel) / (max_pixel - min_pixel) for pixel in pixels]

    # Map scaled pixel values to ASCII characters
    ascii_pixels = [ASCII_CHARS[math.floor(pixel*(len(ASCII_CHARS)-1))] for pixel in scaled_pixels]

    ascii_pixels = ''.join(ascii_pixels)
    
    # split the ASCII art into lines
    lines = [ascii_pixels[i:i+width] for i in range(0, len(ascii_pixels), width)]
    ascii_art = '\n'.join(lines)
    
    return ascii_art

# Example usage
image_path = '/home/neuro/src/ascii_art/image/pokemon/blastoise.png'
ascii_art = image_to_ascii(image_path)
print(ascii_art)
