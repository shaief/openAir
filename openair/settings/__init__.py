import os

if 'DOKKU' in os.environ:
	from .dokku import *
else:
    try:
        from .local import *
    except ImportError:
        from .base import *
