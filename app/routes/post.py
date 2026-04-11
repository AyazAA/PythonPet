from flask import Blueprint, render_template, request, redirect, flash, abort
from flask_login import login_required, current_user
from ..extentions import db
from ..models.post import Post
from ..models.user import User
from app.forms import AuthorForm
from sqlalchemy import text

post = Blueprint('post', __name__)

@post.route('/posts', methods=['POST', 'GET'])
def posts():
    form = AuthorForm()
    form.author.choices = [a.name for a in User.query.all()]

    if(request.method == 'POST'):
        author = request.form.get('author')
        author_id = User.query.filter_by(name=author).first().id
        posts = Post.query.filter_by(user_id=author_id).all()
    else:
        posts = Post.query.all()
    return render_template('post/posts.html', posts=posts, form=form)


@post.route('/post/<int:id>/update', methods=['POST', 'GET'])
@login_required
def update(id):
    post = Post.query.get(id)
    if current_user.id == post.author.id:
        if request.method == 'POST':
            sql = text("UPDATE post SET title = :title,text  = :text WHERE id = :post_id")
            title = request.form['title']
            post_text = request.form['text']
            try:
                db.session.execute(sql, {'title': title, 'text': post_text, 'post_id': post.id})
                db.session.commit()
                return redirect('/')
            except Exception as e:
                print(str(e))
                return str(e)
        else:
            return render_template('post/edit.html', post=post)
    else:
        abort(403)


@post.route('/post/<int:id>/delete', methods=['POST', 'GET'])
@login_required
def delete(id):
    post = Post.query.get(id)
    if current_user.id == post.author.id:
        try:
            db.session.delete(post)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            print(str(e))
            return str(e)
    else:
        abort(403)


@post.route('/create', methods=['POST', 'GET'])
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        text = request.form['text']
        post = Post(user_id=current_user.id, title=title, text=text)
        try:
            db.session.add(post)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            return "Problem with write in DB" + str(e)
    else:
        return render_template('post/create.html')
