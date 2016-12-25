# Labelling web app
Application to label objects in images.

## Environment configuration
The following environment varibles are used:

| Variable          | Meaning    |
|-------------------|------------|
| DATABASE_URL      | URL encoded with database information. Follows the format given by Heroku for PostgreSQL. |
| B2_DOWNLOAD_URL   | URL used in B2 downloads. Can be taken from BackBlaze's web interface or through their API with [b2_authorize_account](https://www.backblaze.com/b2/docs/b2_authorize_account.html). |
