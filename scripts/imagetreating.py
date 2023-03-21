from rembg import remove


def rembg(img,outpath):
    rgb_im = img.convert('RGB')
    input =  rgb_im
    output = remove(input)
    output.save(outpath+".png")
    return outpath+".png"