import datetime

from flask import Blueprint, redirect, render_template, request, url_for

from datastore.datastore import get_entity, update_entity
from session.view.login import login_required

home = Blueprint('home', __name__, url_prefix='/home')


@home.route('/', methods=['GET'])
@login_required
def show_home():
    now_time = datetime.datetime.now().strftime('%Y%m%d')
    time_entity = get_entity(now_time[:6], now_time)
    if time_entity is None:
        update_entity(now_time[:6], now_time, {
                      'startTime': None, 'endTime': None})
    else:
        if time_entity['startTime'] is None:
            start_time = '未打刻'
        else:
            start_time = datetime.datetime.strftime(
                time_entity['startTime'], '%H:%M:%S')

        if time_entity['endTime'] is None:
            end_time = '未打刻'
        else:
            end_time = datetime.datetime.strftime(
                time_entity['endTime'], '%H:%M:%S')

    return render_template('index.html', title='home',
                           startTime=start_time, endTime=end_time)


@home.route('/', methods=['POST'])
@login_required
def record_time():
    submit_time = request.form['submitTime']
    submit_type = request.form['submitType']
    now_time_str = datetime.datetime.now().strftime('%Y%m%d')
    time_entity = get_entity(now_time_str[:6], now_time_str)
    time_entity[submit_type] = datetime.datetime.strptime(
        submit_time, '%Y/%m/%d/%H:%M:%S')
    update_entity(now_time_str[:6], now_time_str, time_entity)

    return redirect(url_for('home.show_home'))
