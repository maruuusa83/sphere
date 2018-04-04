import server.utility.StorageWrapper
from stitcher.image import SphereImageGenerator

sw = server.utility.StorageWrapper.StorageWrapper()
images = sw.get_image()

while (i < image_num):
    name_image = 'img' + str(i)

sip = SphereImageGenerator()
result = sip.stitch(argvs)

