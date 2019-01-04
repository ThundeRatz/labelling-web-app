# Labelling web app
Application to label objects in images.

## Environment configuration
The following configuration varibles are used, present in a `config.py` file in the root folder:

| Variable          | Meaning    |
|-------------------|------------|
| DATABASE          | Dictionary with database, user, password, host and port |
| B2_DOWNLOAD_URL   | URL used in B2 downloads. Can be taken from BackBlaze's web interface or through their API with [b2_authorize_account](https://www.backblaze.com/b2/docs/b2_authorize_account.html). |

## External tools

The [labelImg](https://github.com/tzutalin/labelImg) project is recommended to visualize and edit annotations in the PASCAL VOC format.
