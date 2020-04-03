import json
import os, glob
import cv2
import matplotlib.pyplot as plt


def read_image_paths():
    imgs_path = sorted(glob.glob(os.path.join('data/train_2', '*.png')))
    print(imgs_path)
    return imgs_path


def read_img(path):
    img = cv2.imread(path)
    plt.figure()
    plt.imshow(img)
    plt.show()
    return None


def location_info():
    example = "training_2.json"
    in_file = open(example, "r")
    new_variable = json.load(in_file)
    in_file.close()
    print(new_variable[0]['Label']['objects'][0]['bbox'])
    print(new_variable[0]['Label']['objects'][1]['bbox'])
    print(new_variable[0]['Label']['objects'][2]['bbox'])

    locations = dict()
    for j in range(len(new_variable)):
        bbox_num = new_variable[j]['Label']['objects']
        key = new_variable[j]['External ID']
        locations[key] = []
        for i in range(len(bbox_num)):
            locations[key].append([])
            locations[key][-1].append(bbox_num[i]['bbox']['left'])
            locations[key][-1].append(bbox_num[i]['bbox']['top'])
            locations[key][-1].append(bbox_num[i]['bbox']['left'] + bbox_num[i]['bbox']['width'])
            locations[key][-1].append(bbox_num[i]['bbox']['top'] + bbox_num[i]['bbox']['height'])
    print(locations)
    return locations


def write_csv(img_path, locations):
    print("start writing csv file...")
    with open('img.csv', 'a', newline='') as f:
        if locations is not None:
            for point in locations:
                f.write('{},'.format(img_path))
                for i in point:
                    f.write('{},'.format(i))
                f.write('neuron\n')
        else:
            f.write('{},'.format(img_path))
            f.write(',')
            f.write('neuron\n')


if __name__ == '__main__':
    imgs_path = read_image_paths()
    #for i in imgs_path:
    #    read_img(i)
    locations = location_info()
    for p in imgs_path:
        img_name = os.path.basename(p)
        write_csv(p, locations[img_name])
