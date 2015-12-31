# toppy

*toppy* is a top-like web app written in Python using Flask.
**Warning**: *toppy* is not secure or stable by any means.
It's just an educational tool.

## Setup

*toppy* has been written with Python 3 in mind.

In order to run *toppy*, you have to download it and install its requirements.
Commands listed below show how to install them in a virtual environment in which *toppy* also will be run.
You might need to install `python3-venv` package or similar, depending on your operating system.

```
$ git clone https://github.com/Necior/toppy
$ cd toppy
$ pyvenv venv
$ source venv/bin/activate
(venv) $ pip3 install Flask hurry.filesize psutil
(venv) $ ./app.py
```

## Origin

This is a homework from [DaftCode workshops](https://github.com/daftcode/zajecia_python_mini/tree/master/2015-12-10%20Zajecia%20nr%205).
