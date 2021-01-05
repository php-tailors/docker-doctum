import re

__version__ = '0.7.0'

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
    return {'DOCTUM_WORKDIR': '/code',
            'DOCTUM_CONFIG': '/etc/doctum/doctum.conf.php',
            'DOCTUM_PROJECT_TITLE': 'API Documentation',
            'DOCTUM_SOURCE_DIR': 'src',
            'DOCTUM_BUILD_DIR': 'docs/build/html/api',
            'DOCTUM_CACHE_DIR': 'docs/cache/html/api',
            'DOCTUM_FLAGS': '-v --force --ignore-parse-errors',
            'DOCTUM_SERVER_PORT': 8001,
            'DOCTUM_SOURCE_REGEX': r'\.\(php\|txt\|rst\)$',
            'DOCTUM_THEME': 'default',
            'DOCTUM_PHAR_URL': doctum_phar_url(ver),
            'DOCTUM_PHAR_SHA256_URL': doctum_phar_sha256_url(ver)}

def doctum_runtime_params(ver, php):
    """Configuration parameters that may be modified at runtime"""
    items = doctum_params(ver, php).items()
    exclude = set([
        'DOCTUM_WORKDIR',
        'DOCTUM_SERVER_PORT',
        'DOCTUM_VERSION',
        'DOCTUM_PHAR_URL',
        'DOCTUM_PHAR_SHA256_URL',
    ])
    return {k: v for (k, v) in items if k not in exclude}

def doctum_env_defaults_str(ver, php):
    items = doctum_runtime_params(ver, php).items()
    return '\n'.join(("DEFAULT_%s=%s" % (k, xrepr(v)) for k, v in items))


def doctum_env_settings_str(ver, php):
    params = list(doctum_runtime_params(ver, php))
    return '\n'.join(('export %s=${%s-$DEFAULT_%s}' % (k, k, k) for k in params))


def doctum_versions(php):
    versions = [ ver for (ver, p) in matrix if p == php ]
    return sorted(list(set(versions)))


def php_versions(ver):
    versions = [ php for (v, php) in matrix if v == ver ]
    return sorted(list(set(versions)))


def doctum_phar_url(ver):
    return doctum_releases[ver]['downloads']['phar']


def doctum_phar_sha256_url(ver):
    return doctum_releases[ver]['downloads']['phar_sha256']


def docker_doctum_args_str(ver, php):
    items = doctum_params(ver, php).items()
    return '\n'.join(('ARG %s=%s' % (k, xrepr(v)) for k, v in items))


def docker_doctum_env_str(ver, php):
    params = list(doctum_runtime_params(ver, php))
    return 'ENV ' + ' \\\n    '.join(('%s=$%s' % (k, k) for k in params))


def tag_aliases(ver, php):
    aliases = []
    maj = make_tag(ver.split('.')[0])

    if doctum_versions(php)[-1] == ver:
        aliases.append(make_tag(maj, php))
        aliases.append(make_tag('latest', php))

    if php_versions(ver)[-1] == php:
        aliases.append(make_tag(ver))
        if doctum_versions(php)[-1] == ver:
            aliases.append(make_tag(maj))
            aliases.append(make_tag('latest'))

    return aliases


def microbadges_str_for_tag(tag):
    name = 'phptailors/doctum:%(tag)s' % locals()
    url1 = 'https://images.microbadger.com/badges'
    url2 = 'https://microbadger.com/images/%(name)s' % locals()
    return "\n".join([
        '[![](%(url1)s/version/%(name)s.svg)](%(url2)s "%(name)s")' % locals(),
        '[![](%(url1)s/image/%(name)s.svg)](%(url2)s "Docker image size")' % locals(),
        '[![](%(url1)s/commit/%(name)s.svg)](%(url2)s "Source code")' % locals()
  ])


def microbadges_str_for_tags(tags):
    return '- ' + "\n- ".join(reversed([microbadges_str_for_tag(tag) for tag in tags]))


def microbadges_str(matrix):
    lines = []
    for (ver, php) in reversed(matrix):
        lines.append("")
        lines.append("### %s" % make_tag(ver, php))
        lines.append("")
        tag = context_tag(ver, php)
        lines.append(microbadges_str_for_tag(tag))
        aliases = tag_aliases(ver, php)
        if aliases:
            lines.append("")
            lines.append("- **aliases**: %s" % ', '.join(aliases))
            lines.append("")
    return "\n".join(lines)


def make_tag(ver=None, php=None, sep='-'):
    if php is not None and not php.startswith('php'):
       php = 'php%s' % php
    return sep.join([x for x in (ver, php) if x is not None])

def context_tag(ver, php):
    return make_tag(ver, php, '-')

def context_tags(ver, php):
    return [context_tag(ver, php)] + tag_aliases(ver, php)


def context_dir(ver, php):
    return make_tag(ver, php, '/')


def context_from_tag(php, os, sep='-'):
    return sep.join((php, os))


def context_files(ver, php):
    return {'Dockerfile.in': 'Dockerfile',
            'etc/doctum/doctum.conf.php.in': 'etc/doctum/doctum.conf.php',
            'bin/autobuild.in': 'bin/autobuild',
            'bin/autoserve.in': 'bin/autoserve',
            'bin/build.in': 'bin/build',
            'bin/build_once.in': 'bin/build_once',
            'bin/doctum-defaults.in': 'bin/doctum-defaults',
            'bin/doctum-entrypoint.in': 'bin/doctum-entrypoint',
            'bin/doctum-env.in': 'bin/doctum-env',
            'bin/serve.in': 'bin/serve',
            'hooks/build.in': 'hooks/build'}

def common_subst():
    return {'GENERATED_WARNING': generated_warning(),
            'VERSION': __version__}


def context_subst(ver, php):
    return dict(common_subst(), **dict({
        'DOCTUM_ENV_DEFAULTS': doctum_env_defaults_str(ver, php),
        'DOCTUM_ENV_SETTINGS': doctum_env_settings_str(ver, php),
        'DOCKER_FROM_TAG': context_from_tag(php, 'alpine'),
        'DOCKER_DOCTUM_ARGS': docker_doctum_args_str(ver, php),
        'DOCKER_DOCTUM_ENV': docker_doctum_env_str(ver, php),
    }, **doctum_params(ver, php)))

def global_subst():
    return dict(common_subst(), **dict({
        'MICROBADGES': microbadges_str(matrix)
    }))

def context(ver, php):
    return {'dir': context_dir(ver, php),
            'files': context_files(ver, php),
            'subst': context_subst(ver, php)}

# each tuple in matrix is:
#
# ( doctum-version, php-version )
#
matrix = [
    ('5.3', '7.2'),
    ('5.3', '7.3'),
    ('5.3', '7.4'),
    ('5.5', '7.4'),
    ('5.5', '8.1'),
    ('5.5', '8.2'),
]

doctum_releases = {
    '5.3': {
        'downloads': {
            'phar': 'https://github.com/code-lts/doctum/releases/download/v5.3.1/doctum.phar',
            'phar_sha256': 'https://github.com/code-lts/doctum/releases/download/v5.3.1/doctum.phar.sha256',
            'phar_asc': 'https://github.com/code-lts/doctum/releases/download/v5.3.1/doctum.phar.asc',
            'phar_sha256_asc': 'https://github.com/code-lts/doctum/releases/download/v5.3.1/doctum.phar.sha256.asc',
        }
    }
}

contexts = [ context(ver, php) for (ver, php) in matrix ]

files = { 'README.md.in': 'README.md' }
subst = global_subst()
