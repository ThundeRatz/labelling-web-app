#!/usr/bin/env python3
from collections import defaultdict
from labelling_web_app.scripts.b2 import B2
from labelling_web_app.db.connection import Connection
import os
from urllib.request import urlretrieve


def db_fetch_all_labels():
    conn = Connection()
    with conn.cursor() as cursor:
        cursor.execute('SELECT * FROM labels')
        data = cursor.fetchall()
    conn.close()
    return data


def ensure_path(path):
    os.path.isdir(path) or os.mkdir(path)


def parse_args():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('dir', help='Directory where final labels/images should be saved')
    return parser.parse_args()


def main(args):
    assert(os.path.isdir(args.dir))
    images_dir = os.path.join(args.dir, 'images')
    labels_dir = os.path.join(args.dir, 'labels')
    ensure_path(images_dir)
    ensure_path(labels_dir)
    b2 = B2()

    labels = defaultdict(list)
    for line in db_fetch_all_labels():
        labels[line[0]].append(line[1:])
    print('Remote database has {} labels'.format(len(labels)))

    for image_id, boxes in labels.items():
        if not os.path.isfile(os.path.join(labels_dir, '{}.txt'.format(image_id))):
            print('Downloading new image {}'.format(image_id))
            urlretrieve(b2.get_download_url(image_id), os.path.join(images_dir, '{}.png'.format(image_id)))
            label_file = os.path.join(labels_dir, '{}.txt'.format(image_id))
            with open(label_file, 'w') as f:
                f.write('\n'.join(['0 {}'.format(' '.join(map(str, x))) for x in boxes]))


if __name__ == '__main__':
    main(parse_args())
