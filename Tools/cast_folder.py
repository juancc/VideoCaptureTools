"""
Save all the images in folder with target extension
"""

import os
import argparse

from tqdm import tqdm
import cv2 as cv

# Default extention to target images in folder
EXT = 'jpg'

parser = argparse.ArgumentParser(
                    prog = 'Cast Images in folder',
                    description = 'Save all the images in source folder with a target image extention')


parser.add_argument('path', help='Source directory', type=str)
parser.add_argument('-x', '--extention', help='Target image extention', default=EXT, type=str)



def main(path, ext):
    target_path = os.path.join(path, 'new_format')
    print(f'Creating target path: {target_path}')
    os.makedirs(target_path, exist_ok=True)

    for p in tqdm(os.listdir(path)):
        filepath = os.path.join(path, p)

        name = p.split('.')[0]
        target = os.path.join(target_path, name+'.'+ext)

        try:
            im = cv.imread(filepath)
            cv.imwrite(target, im)
        except Exception as e:
            print(f'Error {e} saving image {p}')

if __name__ == '__main__':
    args = parser.parse_args()
    main(args.path, args.extention)