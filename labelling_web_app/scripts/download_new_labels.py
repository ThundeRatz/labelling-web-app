#!/usr/bin/env python3
from collections import defaultdict
from labelling_web_app.db.connection import Connection
import labelling_web_app.storage.b2 as b2
import os
from urllib.request import urlretrieve
from xml.etree import ElementTree


def get_new_labels():
    conn = Connection()
    with conn.cursor() as cursor:
        cursor.execute('DELETE FROM new_labels WHERE id IN (SELECT DISTINCT id FROM new_labels LIMIT 10) RETURNING *')
        data = cursor.fetchall()
    conn.commit()
    conn.close()
    return data


def create_voc_tree(image_id, labels):
    root = ElementTree.Element('annotation')
    ElementTree.SubElement(root, 'folder').text = 'images'
    ElementTree.SubElement(root, 'filename').text = image_id
    ElementTree.SubElement(root, 'path').text = os.path.join(os.path.realpath('images'), '{}.png'.format(image_id))
    ElementTree.SubElement(ElementTree.SubElement(root, 'source'), 'database').text = 'Unknown'
    size = ElementTree.SubElement(root, 'size')
    ElementTree.SubElement(size, 'width').text = '640'
    ElementTree.SubElement(size, 'height').text = '480'
    ElementTree.SubElement(size, 'depth').text = '3'
    ElementTree.SubElement(root, 'segmented').text = '0'
    for label in labels:
        obj = ElementTree.SubElement(root, 'object')
        ElementTree.SubElement(obj, 'name').text = 'cone'
        ElementTree.SubElement(obj, 'pose').text = 'Unspecified'
        ElementTree.SubElement(obj, 'truncated').text = '0'
        ElementTree.SubElement(obj, 'difficult').text = '0'
        bb = ElementTree.SubElement(obj, 'bndbox')
        x_center, y_center, width, height = label
        ElementTree.SubElement(bb, 'xmin').text = str(round((x_center - width / 2) * 640))
        ElementTree.SubElement(bb, 'ymin').text = str(round((y_center - height / 2) * 480))
        ElementTree.SubElement(bb, 'xmax').text = str(round((x_center + width / 2) * 640))
        ElementTree.SubElement(bb, 'ymax').text = str(round((y_center + height / 2) * 480))
    return ElementTree.ElementTree(root)


def download_image(image_id):
    print('Downloading {}'.format(image_id))
    urlretrieve(b2.get_download_url(image_id), os.path.join('images', '{}.png'.format(image_id)))


def main():
    # Ensure a clean state
    assert not os.path.exists('voc-labels') and not os.path.exists('images'), (
        'Erase the voc-labels and images folders to download new labels')
    os.mkdir('voc-labels')
    os.mkdir('images')

    labels = defaultdict(list)
    for line in get_new_labels():
        if line[3] < 0.005 or line[4] < 0.005:
            print('WARNING: Image {} has too small label, ignoring'.format(line[0]))
            continue
        labels[line[0]].append(line[1:])

    print('Picked labels:')
    for image_id, boxes in labels.items():
        print('{}: {}'.format(image_id, boxes))

    for image_id, boxes in labels.items():
        xml_tree = create_voc_tree(image_id, boxes)
        xml_tree.write(os.path.join('voc-labels', '{}.xml'.format(image_id)))
        download_image(image_id)


if __name__ == '__main__':
    main()
