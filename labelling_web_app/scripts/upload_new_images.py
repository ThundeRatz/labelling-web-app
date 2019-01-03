#!/usr/bin/env python3
from labelling_web_app.scripts.b2 import B2
from labelling_web_app.db.connection import Connection
import os


def db_insert(image_id):
    conn = Connection()
    with conn.cursor() as cursor:
        cursor.execute('INSERT INTO pending VALUES (%s)', (image_id,))
    conn.commit()
    conn.close()


def parse_args():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('dir', help='Directory with images')
    return parser.parse_args()


def b2_authorize():
    for x in ('B2_ACCOUNT_ID', 'B2_ACCOUNT_KEY', 'B2_BUCKET_ID'):
        assert x in os.environ, 'B2_ACCOUNT_ID, B2_ACCOUNT_KEY, B2_BUCKET_ID environment variables must be defined'
    account_id, account_key = (os.environ[x] for x in ['B2_ACCOUNT_ID', 'B2_ACCOUNT_KEY'])
    b2 = B2()
    b2.authorize_account(account_id, account_key)
    return b2


def main(args):
    b2 = b2_authorize()
    uploader = b2.get_uploader(os.environ['B2_BUCKET_ID'])
    for dirpath, _, filenames in os.walk(args.dir):
        for png in filter(lambda x: x.lower().endswith('.png'), filenames):
            full_path = os.path.join(dirpath, png)
            db_insert(uploader.upload(full_path))


if __name__ == '__main__':
    main(parse_args())
