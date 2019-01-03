#!/usr/bin/env python3
from labelling_web_app.db.connection import Connection
import os
import shutil
import sys
from xml.etree import ElementTree

CLASSES = ['cone']


def upload_label(image_id, x, y, w, h):
    conn = Connection()
    with conn.cursor() as cursor:
        cursor.execute('INSERT INTO labels VALUES (%s, %s, %s, %s, %s)', (image_id, x, y, w, h))
    conn.commit()
    conn.close()


def convert(width, height, x_min, x_max, y_min, y_max):
    x = (x_min + x_max) / 2
    y = (y_min + y_max) / 2
    w = abs(x_max - x_min)
    h = abs(y_max - y_min)
    return (x / width, y / height, w / width, h / height)


def upload_label_file(voc_input):
    root = ElementTree.parse(voc_input).getroot()
    image_id = os.path.basename(voc_input)[:-4]  # remove .xml suffix
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    for obj in root.iter('object'):
        name = obj.find('name').text
        if name not in CLASSES:
            print('WARNING: Object {} not configured, assuming cone (file {})'.format(name, voc_input))
        box = obj.find('bndbox')
        coordinates = [float(box.find(x).text) for x in ('xmin', 'xmax', 'ymin', 'ymax')]
        converted = convert(w, h, *coordinates)
        upload_label(image_id, *converted)


def main(args):
    print('Using classes: {}'.format(' '.join(CLASSES)))
    for dirpath, _, filenames in os.walk('voc-labels'):
        for label in filter(lambda x: x.endswith('.xml'), filenames):
            print('Uploading {}'.format(label))
            full_path = os.path.join(dirpath, label)
            upload_label_file(full_path)
    shutil.rmtree('images')
    shutil.rmtree('voc-labels')


if __name__ == '__main__':
    main(sys.argv)
