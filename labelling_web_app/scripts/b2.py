from collections import namedtuple
import hashlib
import os
import requests
from requests.exceptions import HTTPError


def _check_error(r):
    try:
        r.raise_for_status()
    except HTTPError:
        raise HTTPError('Request failed with response text {}'.format(r.text))
    return r


def _safe_get(*args, **kargs):
    return _check_error(requests.get(*args, **kargs))


def _safe_post(*args, **kargs):
    return _check_error(requests.post(*args, **kargs))


class B2:
    Auth = namedtuple('Auth', ['accountId', 'apiUrl', 'authorizationToken', 'downloadUrl', 'minimumPartSize'])

    class Uploader:
        def __init__(self, response):
            self.bucket_id = response['bucketId']
            self._url = response['uploadUrl']
            self._authorization_token = response['authorizationToken']

        def _remote_image_name(self, path):
            # FIXME To support UTF-8, must percent-encode non-ASCII characters
            return 'images/{}'.format(os.path.basename(path))

        def upload(self, path):
            with open(path, 'rb') as f:
                body = f.read()
            headers = {
                'Authorization': self._authorization_token,
                'X-Bz-File-Name': self._remote_image_name(path),
                'Content-Type': 'image/png',
                'Content-Length': str(len(body)),
                'X-Bz-Content-Sha1': hashlib.sha1(body).hexdigest(),
            }
            r = _safe_post(self._url, headers=headers, data=body)
            return r.json()['fileId']

    def __init__(self):
        self._auth = None

    def authorize_account(self, account_id, account_key):
        r = _safe_get('https://api.backblazeb2.com/b2api/v1/b2_authorize_account', auth=(account_id, account_key))
        data = r.json()
        self._auth = B2.Auth(accountId=data['accountId'], apiUrl=data['apiUrl'],
                             authorizationToken=data['authorizationToken'],
                             downloadUrl=data['downloadUrl'], minimumPartSize=data['minimumPartSize'])

    def get_download_url(self, file_id):
        download_url = self._auth and self._auth.downloadUrl or os.environ['B2_DOWNLOAD_URL']
        return '{}/b2api/v1/b2_download_file_by_id?fileId={}'.format(download_url, file_id)

    def get_uploader(self, bucket_id):
        r = _safe_post('{}/b2api/v1/b2_get_upload_url'.format(self._auth.apiUrl),
                       headers={'Authorization': self._auth.authorizationToken},
                       json={'bucketId': bucket_id})
        return B2.Uploader(r.json())
