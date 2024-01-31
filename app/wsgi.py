import os
import sys

from django.core.wsgi import get_wsgi_application

path = '/home/miluhina/web/up-miluhina.xn--80ahdri7a.site/private/app'
if path not in sys.path:
    sys.path.insert(0, path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

application = get_wsgi_application()
