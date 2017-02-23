#!/usr/bin/env python3
import os
import random
import sys

CLASSES = ['cone']


def parse_args():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('dir', help='Directory with images/ and labels/ folders')
    return parser.parse_args()


def main(args):
    args = parse_args()
    directory = os.path.realpath(args.dir)

    label_dir = os.path.join(directory, 'labels')
    if not os.path.isdir(label_dir):
        raise SystemExit(label_dir + ' is not a directory. Terminating.')

    images_dir = os.path.join(directory, 'images')
    if not os.path.isdir(images_dir):
        raise SystemExit(images_dir + ' is not a directory. Terminating.')

    backup_dir = os.path.join(directory, 'backup')
    os.makedirs(backup_dir, exist_ok=True)

    dataset = []
    for dirpath, _, filenames in os.walk(images_dir):
        for image in filter(lambda x: x.endswith('.png'), filenames):
            dataset.append(os.path.join(images_dir, image))

    random.shuffle(dataset)
    validation_image_count = len(dataset) // 5
    train = os.path.join(directory, 'training_list.txt')
    with open(train, 'w') as f:
        f.write('\n'.join(dataset[validation_image_count:]))
    validation = os.path.join(directory, 'validation_list.txt')
    with open(validation, 'w') as f:
        f.write('\n'.join(dataset[:validation_image_count]))
    names = os.path.join(directory, 'names.txt')
    with open(names, 'w') as f:
        f.write('\n'.join(CLASSES))
    config = {
        'classes': len(CLASSES),
        'train': train,
        'valid': validation,
        'names': names,
        'backup': backup_dir,
    }
    with open(os.path.join(directory, 'dataset.data'), 'w') as f:
        f.writelines('{} = {}\n'.format(k, v) for k, v in config.items())

if __name__ == '__main__':
    main(sys.argv)

