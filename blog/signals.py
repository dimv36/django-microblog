from django.core.signals import request_finished, request_started


def request_started_callback(sender, environ, **kwargs):
    method = environ.get('REQUEST_METHOD', None)
    uri = '%s%s' % (environ.get('HTTP_HOST'), environ.get('PATH_INFO'))
    print('request started -> %s on %s' % (method, uri))


def request_finished_callback(sender, **kwargs):
    print('request finished')


request_started.connect(request_started_callback)
request_finished.connect(request_finished_callback)
