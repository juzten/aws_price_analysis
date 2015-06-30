# -*- coding: utf-8 -*-

import os
import config
from APA.errors import ConfigVarNotFoundError

"""Set up config variables.

If environment variable ENVIRONMENT is set to 'dev' and the config/dev.py
file exists then use that file as config settings, otherwise pull in
settings from the production environment variables.
"""

if os.environ.get('ENVIRONMENT') == 'dev':
    try:
        import dev as config  # config/dev.py
    except:
        raise EnvironmentError('Please create config/dev.py')
else:
    # production server environment variables
    config.APP_SECRET_KEY = os.environ.get('APP_SECRET_KEY')
    config.DEBUG = False

try:
    any([config.APP_SECRET_KEY, config.DEBUG]) is None
except Exception, e:
    missing_var = e.message.split()[-1]
    raise ConfigVarNotFoundError(missing_var)
