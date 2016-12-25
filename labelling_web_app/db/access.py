from .connection import Connection


def get_one_pending():
    conn = Connection()
    with conn.cursor() as cursor:
        # FIXME Performance: Should use TABLESAMPLE SYSTEM_ROWS(1) instead, but it requires
        # an extension (see https://www.postgresql.org/docs/9.5/static/tsm-system-rows.html).
        # Maybe if we port the DB away from heroku?
        cursor.execute('SELECT id FROM pending OFFSET floor(random() * (SELECT COUNT(*) FROM pending)) LIMIT 1')
        data = cursor.fetchone()
    conn.close()
    return data and data[0] or None


def set_label(image, labels):
    conn = Connection()
    with conn.cursor() as cursor:
        cursor.execute('DELETE FROM pending WHERE id = %s', (image,))
        # If cursor.rowcount == 0, another user already inserted labels
        labels_valid = cursor.rowcount > 0
        if labels_valid:
            db_labels = ((image, x['x'], x['y'], x['width'], x['height']) for x in labels)
            cursor.executemany('INSERT INTO new_labels VALUES (%s, %s, %s, %s, %s)', db_labels)
    if labels_valid:
        conn.commit()
    conn.close()
