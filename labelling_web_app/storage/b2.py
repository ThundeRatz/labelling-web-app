import os


def get_download_url(file_id):
    url = os.environ.get('B2_DOWNLOAD_URL')
    assert url, 'Missing B2_DOWNLOAD_URL environment variable'
    return '{}/b2api/v1/b2_download_file_by_id?fileId={}'.format(url, file_id)
