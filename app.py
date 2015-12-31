#!/usr/bin/env python3

from flask import Flask, render_template, Response
from hurry.filesize import size as _size
import csv
import io
import psutil
import subprocess

app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'


def get_cpu_stats():
    return psutil.cpu_percent(interval=1, percpu=True)


def get_memory_stats():

    virt = psutil.virtual_memory()
    swap = psutil.swap_memory()

    memory_data = {
        'virtual': {
            'avail': _size(virt.free),
            'total': _size(virt.total),
            'percent': virt.percent,
        },
        'swap': {
            'avail': _size(swap.free),
            'total': _size(swap.total),
            'percent': swap.percent,
        },
    }

    return memory_data


def get_process_list():
    process_list = list()
    for p in psutil.process_iter():
        try:
            process_list.append(
                [
                    p.pid,
                    p.name(),
                    p.status(),
                    p.username(),
                ]
            )
        except psutil.ZombieProcess:
            continue
    return process_list


def guess_description(process_name):
    try:
        out = subprocess.check_output(
                ['apropos', '--section', '1', '^' + process_name + '$'])
    except subprocess.CalledProcessError:
        return 'hidden in the darkness, no one knows who I am'

    return out.decode('utf-8').splitlines()[0].split(' - ')[1]


@app.route('/')
def hello():
    our_response = render_template(
        'show_stats.html',
        cpu_data=enumerate(get_cpu_stats()),
        mem_data=get_memory_stats(),
        process_list=get_process_list(),
    )

    return our_response


@app.route('/csv')
def csv_export():
    csv_content = io.StringIO()
    writer = csv.writer(csv_content)
    writer.writerow(['PID', 'name', 'status', 'user'])
    writer.writerows(get_process_list())

    return Response(csv_content.getvalue(), mimetype='text/csv')


@app.route('/details/<int:pid>')
def process_details(pid):
    try:
        p = psutil.Process(pid=pid)
    except psutil.NoSuchProcess:
        return render_template('show_details.html', error='No such process')

    process = dict()

    process['name'] = p.name()
    process['pid'] = p.pid
    process['ppid'] = p.ppid()

    try:
        process['parent_name'] = psutil.Process(pid=p.ppid()).name()
    except psutil.NoSuchProcess:
        pass

    process['time'] = p.cpu_times().user
    process['desc'] = guess_description(p.name())

    return render_template('show_details.html', process=process)


@app.route('/kill/<int:pid>')
def kill(pid):
    try:
        p = psutil.Process(pid=pid)
        p.kill()
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        return 'Failed (there is no such process or access denied)'

    return 'Zed\'s dead baby, Zed\'s dead.'

if __name__ == '__main__':
    app.run(debug=True)
