from flask import Flask, request, render_template, redirect, url_for
from datetime import date
import sqlite3 


app = Flask(__name__) 

@app.route('/')
def index():
    db = sqlite3.connect('posts.db') # creating database to store posts
    cursor = db.cursor()  # needed to execute sql commands


    #cursor.execute('ALTER TABLE posts ADD post_date DATE')
    cursor.execute('SELECT * FROM posts')
    posts = cursor.fetchall()
    db.close()

    return render_template('index.html',posts=posts)

@app.route('/post/<post_id>')
def post(post_id):
    db = sqlite3.connect('posts.db') # creating database to store posts
    cursor = db.cursor()  # needed to execute sql commands

    cursor.execute('SELECT * FROM posts WHERE id=%s' % (post_id))
    post = cursor.fetchone()
    db.close()

    return render_template('post.html',post=post)

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/create')
def create(): 
    return render_template('create.html')

@app.route('/addPost', methods=['POST'])
def addPost(): 
    db = sqlite3.connect('posts.db') # creating database to store posts
    cursor = db.cursor()  # needed to execute sql commands

    title = request.form['title']
    subtitle = request.form['subtitle']
    author = request.form['author']
    content = request.form['content']
    postdate = date.today()
    

    cursor.execute('INSERT INTO posts(title,post,author,subtitle,post_date) VALUES("%s","%s","%s","%s","%s")' % (title,content,author,subtitle,postdate))
    db.commit()

    db.close()

    return redirect(url_for('index'))

@app.route('/update/<_id>') 
def update(_id): 

    db = sqlite3.connect('posts.db') # creating database to store posts
    cursor = db.cursor()  # needed to execute sql commands

    title = request.args.get('title')
    post = request.args.get('post') 

    cursor.execute('UPDATE posts SET title="%s", post="%s" WHERE id=%s' % (title, post, _id))
    db.commit()

    db.close()

    return '_id: %s | title: %s | post: %s' % (_id, title, post)

@app.route('/delete/<_id>') 
def delete(_id):

    db = sqlite3.connect('posts.db') # creating database to store posts
    cursor = db.cursor()  # needed to execute sql commands

    cursor.execute('DELETE FROM posts WHERE id=%s' % _id)
    db.commit()

    db.close()

    return 'deleted _id: %s' %(_id)

if __name__ == '__main__':
    app.run(debug=True, threaded=True, port=5000) 