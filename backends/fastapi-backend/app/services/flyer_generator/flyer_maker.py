from PIL import Image
from PIL import ImageDraw

from . import flyer
from . import fonts

def make_flyer_from_image(flyer_data: flyer.FlyerData, base : Image.Image, metro_path=None) -> Image.Image:
    """
    Given flyer data and a PIL.Image to use as background, put the data on the background after applying a dark overlay.
    """
    dark_overlay = Image.new("RGBA", base.size, (0,0,0,128))
    bg = Image.alpha_composite(base, dark_overlay)
    img = ImageDraw.Draw(bg) 
   
    flyerseeker = flyer.Flyer.get_dimensions(base.size)
    
    # Add title
    img.multiline_text(
            flyerseeker.get_position(),
            flyer_data.title,
            align="center",
            font=fonts.ubuntu_regular(flyerseeker.fontsize_large), 
            fill=(255,255,255,255))

    flyerseeker.increment_yposition()

    # Add Subtitle
    img.multiline_text(
            flyerseeker.get_position(),
            flyer_data.subtitle,
            align="center",
            font=fonts.ubuntu_regular(flyerseeker.fontsize_small),
            fill=(255,255,255,255))
    flyerseeker.increment_yposition()

    # Add Date
    img.multiline_text(
            flyerseeker.get_position(),
            flyer_data.date,
            align="center",
            font=fonts.ubuntu_regular(flyerseeker.fontsize_large),
            fill=(255,255,255,255))
    flyerseeker.increment_yposition()

    # Add Time frame
    img.multiline_text(
            flyerseeker.get_position(),
            flyer_data.timeframe,
            align="center",
            font=fonts.ubuntu_regular(flyerseeker.fontsize_small),
            fill=(255,255,255,255))
    flyerseeker.increment_yposition()

    # Add place
    img.multiline_text(
            flyerseeker.get_position(),
            flyer_data.place,
            align="center",
            font=fonts.ubuntu_regular(flyerseeker.fontsize_large),
            fill=(255,255,255,255))
    flyerseeker.increment_yposition()
    
    if metro_path != None:
        # Add metro
        metro_logo = Image.open(metro_path)
        # Obtain scale ratio according to scaled font height
        scale_ratio = flyerseeker.fontsize_small/metro_logo.size[flyer.Flyer.HEIGH]
        metro_logo = metro_logo.resize(flyer.Flyer.resize_factor(metro_logo.size, scale_ratio))
        
        flyerseeker.increment_yposition(5)
        bg.alpha_composite(metro_logo, flyerseeker.get_position()) 

        flyerseeker.increment_yposition(-5)
        flyerseeker.increment_xposition(metro_logo.size[flyer.Flyer.WIDTH])
        flyerseeker.increment_xposition(5)
        
        img.multiline_text(
            flyerseeker.get_position(),
            flyer_data.metro,
            align="center",
            font=fonts.ubuntu_regular(flyerseeker.fontsize_small),
            fill=(255,255,255,255))

    return bg
