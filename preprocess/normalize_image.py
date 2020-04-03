import Data_Normalization as dn
import os
import re


def main():
    folder_name = 'Img_256x256'
    img_list = dn.im_list(folder_name)
    # print(img_list)
    for i in img_list:
        j = re.findall(r'\d+', i)
        print(j)
        if i != '.DS_Store' and int(j[0]) > 1176:
            image = dn.read_img(os.path.join(folder_name, i))
            img_sc = dn.scale_pix(image)
            img_np = dn.norm_pix(img_sc)
            img = dn.display_img(img_np)
            img_dic = {0: img}
            dn.img_save(img_dic, 'norm_Img_256x256', i)
    return None


if __name__ == "__main__":
    main()
