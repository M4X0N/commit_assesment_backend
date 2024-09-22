import os

import mysql.connector
from flask import Flask, render_template, url_for


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
    if os.path.exists("/conf/db-password"):
        global conn
        if not conn:
            conn = DBManager(password_file='/conf/db-password')
            conn.populate_db()
        rec = conn.query_titles()

        db_data = ""
        for c in rec:
            db_data += '\n<div> record: ' + c + '</div>'

    return render_template('template.html')


@server.route('/logo.jpg')
def get_image():
    return send_file("/code/logo.jpg", mimetype='image/gif')


if __name__ == '__main__':
    server.run()
