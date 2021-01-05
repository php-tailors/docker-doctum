#!/usr/bin/env python3

import sys
import json
import re


class DoctumRelease:
    _m_m_p = re.compile(
        r'^v?(?P<major>[0-9]+)\.(?P<minor>[0-9]+)\.(?P<patch>[0-9]+)\.*$'
    )

    @classmethod
    def from_string(cls, string, filename=None):
        return cls(json.loads(string), filename)

    @classmethod
    def from_file(cls, file, mode='r', *args, **kw):
        filename = file if isinstance(file, str) else file.name
        if isinstance(file, str):
            with open(filename, mode, *args, **kw) as file:
                string =file.read()
        else:
            string = file.read()
        return cls(json.loads(string), filename)

    def __init__(self, release, filename=None):
        self.release = release
        self.filename = filename
        self.phar = 'doctum.phar'
        self.short_dict_keys = [
            'url',
            'html_url',
            'id',
            'author',
            'tag_name',
            'name',
            'draft',
            'prerelease',
            'created_at',
            'published_at',
            'downloads',
        ]


    def downloads(self):
        assets = self.assets()
        return { k : assets[k]['browser_download_url'] for k in assets }

    def asset_names(self):
        return {
            'phar': self.phar,
            'phar_asc': '%s.asc' % self.phar,
            'phar_sha256': '%s.sha256' % self.phar,
            'phar_sha256_asc': '%s.sha256.asc' % self.phar,
        }

    def assets(self):
        return { t: self.asset(n) for (t, n) in self.asset_names().items() }

    def asset(self, identifier, key='name'):
        for asset in self.release['assets']:
            if asset.get(key) == identifier:
                return asset

    def major_minor(self):
        m = re.match(_m_m_p, release['name'])
        return '%s.%s' % (m.group('major'), m.group('minor'))

    def short_dict(self):
        keys = set(self.short_dict_keys)
        return dict(
            { k : self.release[k] for k in self.release if k in keys },
         ** {'downloads': self.downloads()}
        )

class App:
    @classmethod
    def create_argparser(cls):
        here = os.path.dirname(__file__)
        config = os.path.join(here, 'config.py')
        description = 'Automatic release support script'
        parser = argparse.ArgumentParser(description=description)
##        parser.add_argument('--config', '-c',
##                            metavar='FILE',
##                            dest='config_file',
##                            type=argparse.FileType('r'),
##                            help='config file', default=config)
##        parser.add_argument('--delete',
##                            dest='delete',
##                            action='store_true',
##                            help='delete existing context direcotries')
##        parser.add_argument('--indir', '-i',
##                            dest='indir',
##                            metavar='DIR',
##                            default='.',
##                            help='Input directory, defaults to "."')
##        parser.add_argument('--quiet', '-q',
##                            dest='quiet',
##                            action='store_true',
##                            help='Do not print messages')
##        parser.add_argument('--outdir', '-o',
##                            dest='outdir',
##                            metavar='DIR',
##                            default='.',
##                            help='Output directory, defaults to "."')
        return parser

    def __init__(self):
        self.argparser = self.create_argparser()

    def run(self):
        self.args = self.argparser.parse_args()
        try:
            release = DoctumRelease.from_file(self.args.config_file)
        except ConfigError as e:
            sys.stderr.write("error: %s\n" % str(e))
            return 1
        finally:
            self.args.config_file.close()
        return Updater(config, **vars(self.args)).run()


if __name__ == '__main__':
    sys.exit(App().run())
