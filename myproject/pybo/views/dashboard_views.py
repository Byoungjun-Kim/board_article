from flask import Blueprint, render_template, request, url_for, g, flash
from pybo.models import Board, Article

bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@bp.route('/list/')
def recent_board_article():
    n = 5
    board_list = Board.query
    dash_list =  [(board, Article.query.filter(Article.board_id==board.id).order_by(Article.create_date.desc())[:n]) for board in board_list]
    return render_template('dashboard/dashboard_list.html', dash_list=dash_list)