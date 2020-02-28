import argparse
import os
from PIL import Image


def get_average_grey(image):
    return int(sum(image.tobytes())/64)


def image_processing(image):
    return image.resize((8, 8), Image.ANTIALIAS).convert('L')


def get_hash(image):
    bits = 0
    average = get_average_grey(image)
    for index, byte in enumerate(image.tobytes(), start=0):
        if byte > average:
            bits |= 1 << index
    return hex(bits)


def main(image_path):
    src = Image.open(image_path)
    processed_image = image_processing(src)
    return get_hash(processed_image)


if __name__ == '__main__':
    image_dir = os.path.dirname(os.path.abspath(__file__))
    parser = argparse.ArgumentParser(description='Script for getting perceptual hash of image')
    parser.add_argument('-fp, --full-path', metavar='', dest='full_path', help='full path for image')
    parser.add_argument('-rp, --relative-path', metavar='', dest='relative_path',
                        help='relative path for image, but you need copy image to img folder in project')
    args = parser.parse_args()
    full_path = args.full_path or None
    relative_path = os.path.join(image_dir, args.relative_path) if args.relative_path else None
    if full_path is None and relative_path is None:
        print('Please indicate the path to the file.')
    else:
        path = full_path if full_path else os.path.join(image_dir, relative_path)
        if os.path.exists(path) and os.path.isfile(path):
            print(main(path))
        else:
            print('File does not exist.')
