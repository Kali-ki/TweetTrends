# #https://flothesof.github.io/removing-background-scikit-image.html
# from skimage import io as skio
# url = 'http://i.stack.imgur.com/SYxmp.jpg'
# img = skio.imread(url)
# print("shape of image: {}".format(img.shape))
# print("dtype of image: {}".format(img.dtype))

# from skimage import filters
# sobel = filters.sobel(img)

# import matplotlib.pyplot as plt

# plt.rcParams['image.interpolation'] = 'nearest'
# plt.rcParams['image.cmap'] = 'gray'
# plt.rcParams['figure.dpi'] = 200


# blurred = filters.gaussian(sobel, sigma=2.0)

# plt.imsave("other.png",blurred)

from rembg import remove
from PIL import Image

# images = ["Ada_Lovelace.png","Antoine_Dupont.png","Gérard_Depardieu.png","Linus_Torvalds.png"]

def rembg(img,outpath):
    rgb_im = img.convert('RGB')
    input =  rgb_im#Image.open(input_path) 
    output = remove(input)
    output.save(outpath+".png")
    return outpath+".png"
