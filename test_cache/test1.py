import numpy
from PIL import Image
import binascii

def getMatrixFromBin(filename, width):
    with open(filename, 'rb') as f:
        content = f.read()
    hexst = binascii.hexlify(content)
    fh = numpy.array([int(hexst[i:i+2],16) for i in range(0, len(hexst), 2)])
    rn = len(fh)/width
    fh = numpy.reshape(fh[:rn*width],(-1,width))
    fh = numpy.uint8(fh)
    return fh

filename = "/home/zrx/Downloads/Shadowsocks.exe"
im = Image.fromarray(getMatrixFromBin(filename,512))
im.save("your_img_filename3.png")
