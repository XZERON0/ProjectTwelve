import os
import sys
sys.path.append(os.path.abspath("."))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
from django.core.wsgi import get_wsgi_application
from waitress import serve
from threading import Timer
application = get_wsgi_application()
def open_browser():
    import webbrowser
    webbrowser.open_new('http://localhost:8000/')

if __name__ == '__main__':
    Timer(1, open_browser).start()
    serve(application, host='127.0.0.1', port=8000)
