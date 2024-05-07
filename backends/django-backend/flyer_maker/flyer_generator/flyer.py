from PIL import Image

class FlyerData:
    """
    Container class for details on a flyer.
    """
    def __init__(self, title, subtitle, date, timeframe, place, metro):
        self.title = title
        self.subtitle = subtitle 
        self.date = date
        self.timeframe = timeframe 
        self.place = place
        self.metro = metro

class FlyerDimensions:
    """
    Container class for flyer dimensions. Used in the construction.

    A strategy pattern might get implemented here for every ratio.
    """
    def __init__(self, size):
        self.y_percent = 5
        self.x_percent = 7
        self.x_increment_percent = 15
        self.y_increment_percent = 15
        self.fontsize_small_percent = 4
        self.fontsize_large_percent = 8
        
        if Flyer.isPortrait(size):
            # Portrait percentages
            self.x_percent = 5
            self.y_percent = 15
            self.x_increment_percent = 10
            self.y_increment_percent = 10
            self.fontsize_small_percent = 4
            self.fontsize_large_percent = 8

        self.ytxt = Flyer.width(size, self.y_percent)
        self.xtxt = Flyer.heigh(size, self.x_percent)
        self.xincrements = Flyer.heigh(size, self.x_increment_percent)
        self.yincrements = Flyer.heigh(size, self.y_increment_percent)
        self.fontsize_small = Flyer.width(size, self.fontsize_small_percent)
        self.fontsize_large = Flyer.width(size, self.fontsize_large_percent)

    def increment_xposition(self, xinc=None):
        if xinc == None:
            self.xtxt += self.xincrements
        else:
            self.xtxt += xinc
    
    def increment_yposition(self, yinc=None):
        if yinc == None:
            self.ytxt += self.yincrements
        else:
            self.ytxt += yinc

    def get_position(self) -> tuple:
        return (self.xtxt, self.ytxt)
 
class Flyer:
    """
    Helper methods to handle flyers.
    """
    WIDTH=0
    HEIGH=1
    
    @staticmethod
    def get_dimensions(size) -> FlyerDimensions:
        dimensions = FlyerDimensions(size)
        return dimensions

    @staticmethod
    def width(size: tuple, percent: float) -> int: return int(size[Flyer.WIDTH] * percent/100)
    
    @staticmethod
    def heigh(size: tuple, percent: float) -> int: return int(size[Flyer.HEIGH] * percent/100)
    
    @staticmethod
    def resize_factor(size, factor): return (int(size[Flyer.WIDTH]*factor), int(size[Flyer.HEIGH]*factor))
    
    @staticmethod
    def isPortrait(size): return size[Flyer.WIDTH] <= size[Flyer.HEIGH]

