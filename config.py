import itertools

__version__ = '0.1.1'

def xrepr(arg):
    if isinstance(arg, str):
        return "'%s'" % arg
    else:
        return repr(arg)

def generated_warning(php, os):
    return """\
#############################################################################
# NOTE: FILE GENERATED AUTOMATICALLY, DO NOT EDIT!!!
#############################################################################
"""

def sami_params(php, os):
    """Configuration parameters for doctum with their default values"""
    return {'TLR_CODE': '/code',
            'DOCTUM_CONFIG': '/etc/doctum/doctum.conf.php',
            'DOCTUM_PROJECT_TITLE': 'API Documentation',
            'DOCTUM_SOURCE_DIR': 'src:packages/*',
            'DOCTUM_BUILD_DIR': 'docs/build/html/api',
            'DOCTUM_CACHE_DIR': 'docs/cache/html/api',
            'DOCTUM_FLAGS': '-v --force',
            'DOCTUM_SERVER_PORT': 8001,
            'DOCTUM_SOURCE_REGEX': r'\.\(php\|txt\|rst\)$',
            'DOCTUM_THEME': 'default'}


def sami_env_defaults_str(php, os):
    items = sami_params(php, os).items()
    return '\n'.join(("DEFAULT_%s=%s" % (k, xrepr(v)) for k, v in items))


def sami_env_settings_str(php, os):
    params = list(sami_params(php, os))
    return '\n'.join(('%s=${%s-$DEFAULT_%s}' % (k, k, k) for k in params))


def docker_sami_args_str(php, os):
    items = sami_params(php, os).items()
    return '\n'.join(('ARG %s=%s' % (k, xrepr(v)) for k, v in items))


def docker_sami_env_str(php, os):
    params = list(sami_params(php, os))
    return 'ENV ' + ' \\\n    '.join(('%s=$%s' % (k, k) for k in params))


def context_id(php, os, sep):
    return sep.join((php, os))


def context_dir(php, os, sep='/'):
    return context_id(php, os, sep)


def context_tag(php, os, sep='-'):
    return context_id(php, os, sep)


def context_files(php, os):
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


def context_subst(php, os):
    return dict({'GENERATED_WARNING': generated_warning(php, os),
                 'DOCTUM_ENV_DEFAULTS': sami_env_defaults_str(php, os),
                 'DOCTUM_ENV_SETTINGS': sami_env_settings_str(php, os),
                 'DOCKER_FROM_TAG': context_tag(php, os),
                 'DOCKER_DOCTUM_ARGS': docker_sami_args_str(php, os),
                 'DOCKER_DOCTUM_ENV': docker_sami_env_str(php, os),
                 'VERSION': __version__}, **sami_params(php, os))


def context(php, os):
    return {'dir': context_dir(php, os),
            'files': context_files(php, os),
            'subst': context_subst(php, os)}


phps = ['7.3', '7.4']
oses = ['alpine']
contexts = [context(php, os) for (php, os) in itertools.product(phps, oses)]
del phps
del oses
