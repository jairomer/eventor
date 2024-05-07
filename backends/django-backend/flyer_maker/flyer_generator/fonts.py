from PIL import ImageFont
import os

def ubuntu_regular(size):
    pwd = os.path.dirname(os.path.realpath(__file__))
    return ImageFont.truetype(f"{pwd}/fonts/ubuntu/Ubuntu-Regular.ttf", size)

def ubuntu_bold(size): 
    pwd = os.path.dirname(os.path.realpath(__file__))
    return ImageFont.truetype(f"{pwd}/fonts/ubuntu/Ubuntu-Bold.ttf", size)

