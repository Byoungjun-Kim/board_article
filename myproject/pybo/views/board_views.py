from flask import Blueprint, render_template, request, url_for, g, flash

from datetime import datetime
from werkzeug.utils import redirect

from .. import db

from pybo.models import Board, Article

from ..forms import BoardForm, ArticleForm
from pybo.views.auth_views import login_required

bp = Blueprint('board', __name__, url_prefix='/board')

@bp.route('/delete/<int:board_id>')
@login_required
def delete(board_id):
    board = Board.query.get_or_404(board_id)
    if g.user != board.user:
        flash('삭제권한이 없습니다')
        return redirect(url_for('board.detail', board_id=board_id))
    db.session.delete(board)
    db.session.commit()
    return redirect(url_for('board._list'))

@bp.route('/update/<int:board_id>', methods=('GET', 'POST'))
@login_required
def update(board_id):
    board = Board.query.get_or_404(board_id)
    if g.user != board.user:
        flash('수정권한이 없습니다')
        return redirect(url_for('board.detail', board_id=board_id))
    if request.method == 'POST':
        form = BoardForm()
        if form.validate_on_submit():
            form.populate_obj(board)
            board.modify_date = datetime.now()  # 수정일시 저장
            db.session.commit()
            return redirect(url_for('board.detail', board_id=board_id))
    else:
        form = BoardForm(obj=board)
    return render_template('board/board_form.html', form=form)

@bp.route('/create/', methods=('GET', 'POST'))
@login_required
def create():
    form = BoardForm()
    if request.method == 'POST' and form.validate_on_submit():
        board = Board(title=form.title.data,
                            create_date=datetime.now(), user=g.user)
        db.session.add(board)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('board/board_form.html', form=form)

@bp.route('/list/')
def _list():
    page = request.args.get('page', type=int, default=1)
    board_list = Board.query.order_by(Board.create_date.desc())
    board_list = board_list.paginate(page, per_page=10)
    return render_template('board/board_list.html', board_list=board_list)


@bp.route('/detail/<int:board_id>/')
def detail(board_id):
    board = Board.query.get_or_404(board_id)
    page = request.args.get('page', type=int, default=1)
    article_list = Article.query.filter(Article.board_id==board_id).order_by(Article.create_date.desc())
    article_list = article_list.paginate(page, per_page=10)
    return render_template('board/board_detail.html', board=board, article_list=article_list)