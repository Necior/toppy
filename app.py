#!/usr/bin/env python3

from flask import Flask, render_template, Response
from hurry.filesize import size as _size
import csv
import io
import psutil

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


if __name__ == '__main__':
    app.run(debug=True)
