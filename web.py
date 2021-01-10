#!/root/miniconda3/bin/python
from wsgiref.simple_server import make_server
# from waitress import serve
import os, io
import uuid
import shutil
import daemon
from pyramid.response import Response
from pyramid.config import Configurator
from pyramid.response import Response
import random
import subprocess
from PIL import Image


def upload(request):

    fileObj = request.POST.get('filename')
    sid = str(random.randint(1111, 9999)) 

    prb = request.POST.get('prb')

    filename = '{}.png'.format(sid)
    file_path = os.path.join('/tmp/upload', filename )

    image_file = io.BytesIO(fileObj.file.read())
    try:
        im = Image.open(image_file)
        # print(im.size)
        # print(file_path)
        im.save(file_path)
        im.close()
    except:
        return Response('{"error":"image"}', headers={'Content-Type': 'application/json'})

    cwd ='/root/mmdetection'
    subprocess.Popen(["/root/miniconda3/bin/python", "/root/mmdetection/mmdetectionl.py", sid, prb], cwd=cwd)
    print('id', sid)
    return Response('{"success":"Ok", "id": "%s"}' % sid, headers={'Content-Type': 'application/json'})



if __name__ == '__main__':
    with Configurator() as config:

        config.add_route('upload', '/upload')
        config.add_view(upload, route_name='upload')

        # config.add_route('hello', '/')
        # config.add_view(hello_world, route_name='hello')
        app = config.make_wsgi_app()

    # serve(app, host='0.0.0.0', port=8081)

    logfile = '/var/log/web.log'
# pidfile = f'/tmp/det{sys.argv[1]}.pid'

    context = daemon.DaemonContext(
        working_directory='/root',
        umask=0o002,
        # pidfile=PidFile(pidfile),
        stdout=open(logfile, "a"),
        stderr=open(logfile, "a"),
        detach_process=True
        # logfile=logfile
    )
    with context:
        server = make_server('127.0.0.1', 8081, app)
        server.serve_forever()

