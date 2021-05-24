from datetime import datetime

from flask import Blueprint, url_for, request, render_template, g, flash
from werkzeug.utils import redirect

from pybo import db
from pybo.models import Board, Article

from ..forms import ArticleForm
from .auth_views import login_required

bp = Blueprint('article', __name__, url_prefix='/article')

@bp.route('/delete/<int:article_id>')
@login_required
def delete(article_id):
    article = Article.query.get_or_404(article_id)
    board_id = article.board_id
    if g.user != article.user:
        flash('삭제권한이 없습니다')
        return redirect(url_for('article.detail', article_id=article_id))
    db.session.delete(article)
    db.session.commit()
    return redirect(url_for('board.detail', board_id=board_id))

@bp.route('/update/<int:article_id>', methods=('GET', 'POST'))
@login_required
def update(article_id):
    article = Article.query.get_or_404(article_id)
    if g.user != article.user:
        flash('수정권한이 없습니다')
        return redirect(url_for('article.detail', article_id=article_id))
    if request.method == 'POST':
        form = ArticleForm()
        if form.validate_on_submit():
            form.populate_obj(article)
            article.modify_date = datetime.now()  # 수정일시 저장
            db.session.commit()
            return redirect(url_for('article.detail', article_id=article_id))
    else:
        form = ArticleForm(obj=article)
    return render_template('article/article_form.html', form=form)

@bp.route('/create/<int:board_id>', methods=('GET', 'POST'))
@login_required
def create(board_id):
    form = ArticleForm()
    board = Board.query.get_or_404(board_id)
    if request.method == 'POST' and form.validate_on_submit():
        article = Article(title=form.title.data, content=form.content.data,
                      create_date=datetime.now(), user=g.user)
        board.article_set.append(article)
        db.session.add(article)
        db.session.commit()
        return redirect(url_for('board.detail', board_id=board_id))
    return render_template('article/article_form.html', form=form)

@bp.route('/detail/<int:article_id>/')
def detail(article_id):
    article = Article.query.get_or_404(article_id)
    return render_template('article/article_detail.html', article=article)

@bp.route('/get/<int:article_id>/')
def get(article_id):
    article = Article.query.get_or_404(article_id)
    return article.content