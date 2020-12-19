# phptailors/docker-doctum

[![](https://img.shields.io/docker/stars/phptailors/doctum.svg)](https://hub.docker.com/r/phptailors/doctum/ "Docker Stars")
[![](https://img.shields.io/docker/pulls/phptailors/doctum.svg)](https://hub.docker.com/r/phptailors/doctum/ "Docker Pulls")

Docker container with [doctum](https://github.com/code-lts/doctum/)
documentation generator.

## Image versions

  - [![](https://images.microbadger.com/badges/version/phptailors/doctum:5.3-php7.4.svg)](https://microbadger.com/images/phptailors/doctum:5.3-php7.4 "Get your own version badge on microbadger.com")
    [![](https://images.microbadger.com/badges/image/phptailors/doctum:5.3-php7.4.svg)](https://microbadger.com/images/phptailors/doctum:5.3-php7.4 "Get your own image badge on microbadger.com")
    [![](https://images.microbadger.com/badges/commit/phptailors/doctum:5.3-php7.4.svg)](https://microbadger.com/images/phptailors/doctum:5.3-php7.4 "Get your own commit badge on microbadger.com") (latest)
  - [![](https://images.microbadger.com/badges/version/phptailors/doctum:5.3-php8.0.svg)](https://microbadger.com/images/phptailors/doctum:5.3-php8.0 "Get your own version badge on microbadger.com")
    [![](https://images.microbadger.com/badges/image/phptailors/doctum:5.3-php8.0.svg)](https://microbadger.com/images/phptailors/doctum:5.3-php8.0 "Get your own image badge on microbadger.com")
    [![](https://images.microbadger.com/badges/commit/phptailors/doctum:5.3-php8.0.svg)](https://microbadger.com/images/phptailors/doctum:5.3-php8.0 "Get your own commit badge on microbadger.com")

## Features

With this container you can:

  - build documentation once and exit,
  - build documentation once and then serve it with http server,
  - build documentation continuously (rebuilding when sources change),
  - build documentation continuously and serve it at the same time.

The default behavior is to build continuously and serve at the same time.

## Quick example

Assume we have the following file hierarchy (the essential here is assumption
that php source files are found under `src`, also we expect the documentation
to be written-out somewhere under `docs`)

```console
user@pc:$ tree .
.
|-- docs
`-- src
    `-- Foo
        `-- Bar.php
```

### Running with docker

Run it as follows

```console
user@pc:$ docker run --rm -it -v "$(pwd):/code" -p 8001:8001 -u "`id -u`:`id -g`" phptailors/doctum
```

### Running with docker-compose

In the top level directory create `docker-compose.yml` containing the following

```yaml
version: '3'
# ....
services:
   # ...
   doctum:
      image: phptailors/doctum
      ports:
         - "8001:8001"
      volumes:
         - ./:/code
      user: "${MYUID:-1000}:${MYGID:-1000}"
      environment:
        - MYUID
        - MYGID
```

Then run

```console
user@pc:$ MYUID=`id -u` MYGID=`id -g` docker-compose up doctum
```

### Results

Whatever method you chose to run the container, you shall see two new directories

```console
user@pc:$ ls -d docs/*
docs/build docs/cache
```

The documentation is written to `docs/build/html/api`

```console
user@pc:$ find docs -name 'index.html'
docs/build/html/api/index.html
```

As long as the container is running, the documentation is available at

  - <http://localhost:8001>.

## Customizing

Several parameters can be changed via environment variables, for example we can
change build to ``build/docs/api`` dir as follows

```console
user@pc:$ docker run --rm -it -v "$(pwd):/code" -p 8001:8001 -u "`id -u`:`id -g`"  -e DOCTUM_BUILD_DIR=build/docs/api phptailors/doctum
```

## Details

### Volume mount points exposed

  - `/code` - bind top level directory of your project here.

### Working directory

  - `/code`

### Files inside container

#### In `/usr/local/bin`

  - scripts which may be used as container's command:
      - `autobuild` - builds documentation continuously (watches
        source directory for changes),
      - `autoserve` - builds documentation continuously and runs
        http server,
      - `build` - builds documentation once and exits,
      - `serve` - builds source once and starts http server,
  - other files
      - `doctum-defaults` - sets `DEFAULT_DOCTUM_xxx` variables (default values
        for `DOCTUM_xxx` variables),
      - `doctum-env` - initializes `DOCTUM_xxx` variables,
      - `doctum-entrypoint` - provides an entry point for docker.

#### In `/etc/doctum`

  - `doctum.conf.php` - default configuration file for doctum.

### Build arguments & environment variables

The container defines several build arguments which are copied to corresponding
environment variables within the running container. Most of the arguments/variables
have names starting with `DOCTUM_` prefix. All the `doctum-*` scripts, and the
configuration file `doctum.conf.php` respect these variables, so the easiest way
to adjust the container to your needs is to set environment variables (`-e`
flag to [docker](https://docker.com/)).  `TLR_CODE` is an exception, it must be
defined at build time, so it may only be changed via docker's build arguments.

| Argument               | Default Value                    | Description                                            |
| ---------------------- | -------------------------------- | ------------------------------------------------------ |
| TLR\_CODE              | /code                            | Volume mount point and default working directory.      |
| DOCTUM\_CONFIG         | /etc/doctum/doctum.conf.php      | Path to the config file for doctum.                    |
| DOCTUM\_PROJECT\_TITLE | API Documentation                | Title for the generated documentation.                 |
| DOCTUM\_SOURCE\_DIR    | src                              | Colon-separated directories with the PHP source files. |
| DOCTUM\_BUILD\_DIR     | docs/build/html/api              | Where to output the generated documentation.           |
| DOCTUM\_CACHE\_DIR     | docs/cache/html/api              | Where to write cache files.                            |
| DOCTUM\_FLAGS          | -v --force --ignore-parse-errors | Commandline flags passed to doctum.                    |
| DOCTUM\_SERVER\_PORT   | 8001                             | Port numer (within container) for the http server.     |
| DOCTUM\_SOURCE\_REGEX  | `\.\(php\\|txt\\|rst\)$`         | Regular expression for source files' discovery.        |
| DOCTUM\_THEME          | default                          | Doctum theme.                                          |

### Software included

  - [php](https://php.net/)
  - [git](https://git-scm.com/)
  - [doctum](https://github.com/code-lts/doctum/)

## LICENSE

Copyright (c) 2020 by Paweł Tomulik <ptomulik@meil.pw.edu.pl>

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE
