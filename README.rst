Labelling web app
=================

Application to label objects in images.

Environment configuration
-------------------------

The following environment varibles are used:

+----------------------+---------------+
| Variable             | Meaning       |
+======================+===============+
| DATABASE\_URL        | URL encoded   |
|                      | with database |
|                      | information.  |
|                      | Follows the   |
|                      | format given  |
|                      | by Heroku for |
|                      | PostgreSQL.   |
+----------------------+---------------+
| B2\_DOWNLOAD\_URL    | URL used in   |
|                      | B2 downloads. |
|                      | Can be taken  |
|                      | from          |
|                      | BackBlaze's   |
|                      | web interface |
|                      | or through    |
|                      | their API     |
|                      | with          |
|                      | `b2\_authoriz |
|                      | e\_account <h |
|                      | ttps://www.ba |
|                      | ckblaze.com/b |
|                      | 2/docs/b2_aut |
|                      | horize_accoun |
|                      | t.html>`__.   |
+----------------------+---------------+
