from flask import Blueprint, render_template, request, redirect, flash, abort
from flask_login import login_required, current_user
from ..extentions import db
from ..models.post import Post
from ..models.user import User
from app.forms import AuthorForm
from sqlalchemy import text

post = Blueprint('post', __name__)

@post.post('/posts')
def get_posts_by_author():
    form = AuthorForm()
    form.author.choices = [a.name for a in User.query.all()]
    author = request.form.get('author')
    author_id = User.query.filter_by(name=author).first().id
    posts = Post.query.filter_by(user_id=author_id).all()
    return render_template('post/posts.html', posts=posts, form=form)

@post.get('/posts')
def get_all_posts():
    form = AuthorForm()
    form.author.choices = [a.name for a in User.query.all()]
    posts = Post.query.all()
    return render_template('post/posts.html', posts=posts, form=form)

@post.get('/post/<int:id>/update')
@login_required
def get_update(id):
    post = Post.query.get(id)
    if current_user.id == post.author.id:
        return render_template('post/edit.html', post=post)
    else:
        abort(403)

@post.post('/post/<int:id>/update')
@login_required
def update(id):
    sql = text("UPDATE post SET title = :title,text  = :text WHERE id = :post_id and user_id = :current_user_id")
    title = request.form['title']
    post_text = request.form['text']
    try:
        res = db.session.execute(sql, {'title': title, 'text': post_text, 'post_id': id, 'current_user_id': current_user.id})
        if res.rowcount == 0:
            print("Не изменен пост")
            flash(f"Ошибка изменения.", "danger")
        else:
            db.session.commit()
            return redirect('/')
    except Exception as e:
        print(str(e))
        flash(f"Ошибка изменения.", "danger")

@post.route('/post/<int:id>/delete', methods=['POST', 'GET'])
@login_required
def delete(id):
    sql = text("DELETE FROM post WHERE id = :post_id and user_id = :current_user_id")
    try:
        res = db.session.execute(sql, {'post_id': id, 'current_user_id': current_user.id})
        db.session.commit()
        if res.rowcount == 0:
            print("Не удален пост")
            flash(f"Ошибка удаления.", "danger")
        return redirect('/')
    except Exception as e:
        print(str(e))
        flash(f"Ошибка удаления.", "danger")

@post.get('/create')
@login_required
def get_create():
    return render_template('post/create.html')

@post.post('/create')
@login_required
def create():
    title = request.form['title']
    text = request.form['text']
    post = Post(user_id=current_user.id, title=title, text=text)
    try:
        db.session.add(post)
        db.session.commit()
        return redirect('/')
    except Exception as e:
        flash(f"Ошибка создания.", "danger")
        print("Problem with write in DB" + str(e))
