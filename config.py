import itertools
import re

__version__ = '0.3.0'

def xrepr(arg):
    if isinstance(arg, str):
        return "'%s'" % arg
    else:
        return repr(arg)

def generated_warning():
    return """\
#############################################################################
# NOTE: FILE GENERATED AUTOMATICALLY, DO NOT EDIT!!!
#############################################################################
"""

def doctum_params(ver, php):
    """Configuration parameters for doctum with their default values"""
    return {'TLR_CODE': '/code',
            'DOCTUM_VERSION': ver,
            'DOCTUM_CONFIG': '/etc/doctum/doctum.conf.php',
            'DOCTUM_PROJECT_TITLE': 'API Documentation',
            'DOCTUM_SOURCE_DIR': 'src',
            'DOCTUM_BUILD_DIR': 'docs/build/html/api',
            'DOCTUM_CACHE_DIR': 'docs/cache/html/api',
            'DOCTUM_FLAGS': '-v --force --ignore-parse-errors',
            'DOCTUM_SERVER_PORT': 8001,
            'DOCTUM_SOURCE_REGEX': r'\.\(php\|txt\|rst\)$',
            'DOCTUM_THEME': 'default'}


def doctum_env_defaults_str(ver, php):
    items = doctum_params(ver, php).items()
    return '\n'.join(("DEFAULT_%s=%s" % (k, xrepr(v)) for k, v in items))


def doctum_env_settings_str(ver, php):
    params = list(doctum_params(ver, php))
    return '\n'.join(('%s=${%s-$DEFAULT_%s}' % (k, k, k) for k in params))


def docker_doctum_args_str(ver, php):
    items = doctum_params(ver, php).items()
    return '\n'.join(('ARG %s=%s' % (k, xrepr(v)) for k, v in items))


def docker_doctum_env_str(ver, php):
    params = list(doctum_params(ver, php))
    return 'ENV ' + ' \\\n    '.join(('%s=$%s' % (k, k) for k in params))


def context_dir(ver, php, sep='/'):
    dir = re.sub(r'-dev$', '', ver)
    return sep.join((dir, ('php%s' % php)))


def context_from_tag(php, os, sep='-'):
    return sep.join((php, os))


def context_files(ver, php):
    return {'Dockerfile.in': 'Dockerfile',
            'etc/doctum.conf.php.in': 'etc/doctum.conf.php',
            'bin/autobuild.in': 'bin/autobuild',
            'bin/autoserve.in': 'bin/autoserve',
            'bin/build.in': 'bin/build',
            'bin/build_once.in': 'bin/build_once',
            'bin/doctum-defaults.in': 'bin/doctum-defaults',
            'bin/doctum-entrypoint.in': 'bin/doctum-entrypoint',
            'bin/doctum-env.in': 'bin/doctum-env',
            'bin/serve.in': 'bin/serve',
            'hooks/build.in': 'hooks/build'}


def context_subst(ver, php):
    return dict({'GENERATED_WARNING': generated_warning(),
                 'DOCTUM_ENV_DEFAULTS': doctum_env_defaults_str(ver, php),
                 'DOCTUM_ENV_SETTINGS': doctum_env_settings_str(ver, php),
                 'DOCKER_FROM_TAG': context_from_tag(php, 'alpine'),
                 'DOCKER_DOCTUM_ARGS': docker_doctum_args_str(ver, php),
                 'DOCKER_DOCTUM_ENV': docker_doctum_env_str(ver, php),
                 'VERSION': __version__}, **doctum_params(ver, php))


def context(ver, php):
    return {'dir': context_dir(ver, php),
            'files': context_files(ver, php),
            'subst': context_subst(ver, php)}

contexts = [ context(ver, php) for (ver, php) in [
        ('5.3-dev', '7.4'),
        ('5.3-dev', '8.0')
]]
