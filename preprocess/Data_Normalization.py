# normalize color
# normalize size
#       scale down to 500x500? -- faster (check how much information gets lost)
#       compensation for magnification differences
# data inclusiveness:
#       intensities
#       orientation
import numpy as np
import os
from PIL import Image


def im_list(path):
    """
    Input the name of the folder.
    Returns a list of file names of the files in the folder
    """
    return [f for f in os.listdir(path)]  #
    # can add type of file ----- if f.endswith('.jpg)


# read image
def read_img(file):
    """
    Reads in an image file, converts it to grayscale, and scales pixel values
    to the 0-1 range.
    Args:
        file: (str) name/path of the image file

    Returns: Image object

    """
    image = Image.open(file).convert('L')  # load and convert to gray scale
    # print(image.mode)
    # print(image.size)
    # image.show()
    return image


def scale_pix(image):
    """
    For pixel values of 0-255, scale to 0-1 (better for deep learning?)
    Args:
        image: (nparray) original image pixel values in range 0-255

    Returns: (nparray) pixel values in range 0-1

    """
# check pixel range
    pixels = np.asarray(image)
    # print('data type: {}'.format(pixels.dtype))
    # print('Min: %.3f, Max: %.3f' % (pixels.min(), pixels.max()))
    data_type = pixels.dtype
# normalize from rang 0-255 to range 0-1
    pixels = pixels.astype(np.float64)
    if type == 'uint8':
        pixels /= 255.0
    # print('Min: %.3f, Max: %.3f' % (pixels.min(), pixels.max()))
    return pixels


def norm_pix(pix):
    """
    Normalizes pixel values to distribute across full range of 0-1
    Args:
        pix: (nparray) pixel values in range 0-1

    Returns: (nparray) normalized pixel values

    """
    pixels = 1*(pix-pix.min())/(pix.max()-pix.min())
    # print('Min: %.3f, Max: %.3f' % (pixels.min(), pixels.max()))
    return pixels


def norm_mag(mag, img):
    """
    This function converts images of different magnification into
    10x magnification.
    Args:
        mag: (integer) microscope/scanner magnification
        img: (nparray) original image

    Returns: (nparray) new image at normalized magnification

    """
    # normalize to 10x? about 5x5 pixels per neuron
    if mag >= 10:
        scale = 10/mag
        img = img.resize((round(img.size[0]*scale), round(img.size[1]*scale)))
    elif mag == 4:
        img = img.resize((round(img.size[0]/mag), round(img.size[1]/mag)))
    else:
        print('Magnification is too low. At least 10x is expected.')
    return img


def norm_size(img):
    def zero_pad(dim, image):
        # pad so that w & h are multiples of 256
        padded = np.zeros(dim)
        padded[:image.shape[0], :image.shape[1]] = img
        return padded

    def crop_img(img_array):
        cropped = {}
        # want 256 x 256
        if img_array.max() <= 1:
            img_array = img_array * 255
        img_array = img_array.astype(np.uint8)
        image = Image.fromarray(img_array)
        image.show()
        width, height = image.size
        for i in range(int(height/256)):
            for j in range(int(width/256)):
                box = (j*256, i*256, (j+1)*256, (i+1)*256)
                n = i*height/256+j+1
                cropped['{}'.format(int(n))] = image.crop(box)
        print(cropped.keys())
        return cropped

    # local image size normalization functions
    print(img.shape)
    dimension = (round(img.shape[0]/256 + 0.5)*256,
                 round(img.shape[1]/256 + 0.5)*256)
    print(dimension)
    img_pad = zero_pad(dimension, img)
    img_dic = crop_img(img_pad)
    return img_dic


def img_save(img_dic, path, k):
    if len(img_dic) > 1:
        for i in range(len(img_dic)):
            n = f'{i+1177:04}'
            img_dic['{}'.format(i+1)].\
                save(os.path.join(path, 'IMG-%s.png' % n))
    else:
        img_dic[0].save(os.path.join(path, k))
    return None


# for generating training data only
def rotate_img():
    pass


def display_img(pix):
    """

    Args:
        pix: (nparray)

    Returns: None

    """
    if pix.max() <= 1:
        pix = pix*255
    pix = pix.astype(np.uint8)
    image = Image.fromarray(pix, 'L')
    # image.show()
    return image


def main(mag, mod, file):
    img = read_img(file)
    img_nm = norm_mag(mag, img)
    # img_nm.show()
    img_sc = scale_pix(img_nm)
    img_np = norm_pix(img_sc)
    # show image
    # display_img(img_np)
    img_ns = norm_size(img_np)
    img_save(img_ns, 'Img_256x256/', None)
    img_ns['1'].show()


if __name__ == "__main__":
    # user input parameters
    magnification = 10  # 10x 20x
    modality = 'bf'  # bf--bright field, fl--florescent
# for a single image
    file_name = "Rat/R19-03 - 1Fa - anti-GFP VIP-Image Export-01.png"
    main(magnification, modality, file_name)
# for multiple images in a folder
    folder_name = "Rat"
    file_list = im_list(folder_name)
    # print(file_list)
