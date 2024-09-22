import mysql.connector
from flask import Flask


class DBManager:
    def __init__(self, database='commit_assesment_db', host="db", user="admin", password_file=None):
        pf = open(password_file, 'r')
        self.connection = mysql.connector.connect(
            user=user,
            password=pf.read(),
            host=host,  # name of the mysql service as set in the docker compose file
            database=database,
            auth_plugin='mysql_native_password'
        )
        pf.close()
        self.cursor = self.connection.cursor()

    def populate_db(self):
        self.cursor.execute('DROP TABLE IF EXISTS blog')
        self.cursor.execute(
            'CREATE TABLE blog (id INT AUTO_INCREMENT PRIMARY KEY, title VARCHAR(255))')
        self.cursor.executemany('INSERT INTO blog (id, title) VALUES (%s, %s);', [
                                (i, 'Blog post #%d' % i) for i in range(1, 5)])
        self.connection.commit()

    def query_titles(self):
        self.cursor.execute('SELECT title FROM blog')
        rec = []
        for c in self.cursor:
            rec.append(c[0])
        return rec


server = Flask(__name__)
conn = None


@server.route('/')
def listBlog():
    global conn
    if not conn:
        conn = DBManager(password_file='/conf/db-password')
        conn.populate_db()
    rec = conn.query_titles()

    response = "<img src = /code/logo.jpg width = '100' length = '100'>"
    response += '\n<h1>Hello Commit</h1>\n<p>from Max Rogol</p>'
    for c in rec:
        response = response + '<div> record: ' + c + '</div>'
    return response


if __name__ == '__main__':
    server.run()
