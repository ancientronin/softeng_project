from extract import connect
from extract import get_reviews

conn = connect('data.db')
try:
    cursor = conn.cursor()
    get_reviews(cursor)
    conn.close()
except Exception as e:
    print('Something went wrong...\n\n{}'.format(e))
    conn.close()

print('hello world')