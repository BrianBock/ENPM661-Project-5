def pixelToPoint(self, pixel):
    ''' pixel (row, col) --> point (x, y) '''
    return (pixel[1], self.height-1-pixel[0])

def pointToPixel(self, point):
    ''' point (x, y) --> pixel (row, col) '''
    return (self.height-1-point[1], point[0])