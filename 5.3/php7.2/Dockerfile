#############################################################################
# NOTE: FILE GENERATED AUTOMATICALLY, DO NOT EDIT!!!
#############################################################################

FROM php:7.2-alpine

MAINTAINER Paweł Tomulik <ptomulik@meil.pw.edu.pl>

ARG DOCTUM_WORKDIR='/code'
ARG DOCTUM_CONFIG='/etc/doctum/doctum.conf.php'
ARG DOCTUM_PROJECT_TITLE='API Documentation'
ARG DOCTUM_SOURCE_DIR='src'
ARG DOCTUM_BUILD_DIR='docs/build/html/api'
ARG DOCTUM_CACHE_DIR='docs/cache/html/api'
ARG DOCTUM_FLAGS='-v --force --ignore-parse-errors'
ARG DOCTUM_SERVER_PORT=8001
ARG DOCTUM_SOURCE_REGEX='\.\(php\|txt\|rst\)$'
ARG DOCTUM_THEME='default'
ARG DOCTUM_PHAR_URL='https://github.com/code-lts/doctum/releases/download/v5.3.1/doctum.phar'
ARG DOCTUM_PHAR_SHA256_URL='https://github.com/code-lts/doctum/releases/download/v5.3.1/doctum.phar.sha256'

ARG BUILD_DATE
ARG VCS_REF
ARG VERSION

LABEL org.label-schema.build-date="${BUILD_DATE}" \
      org.label-schema.name="Docker Doctum Image" \
      org.label-schema.description="Docker image with Doctum documentation generator." \
      org.label-schema.vcs-ref="${VCS_REF}" \
      org.label-schema.vcs-url="https://github.com/phptailors/docker-doctum" \
      org.label-schema.vendor="Paweł Tomulik" \
      org.label-schema.version="${VERSION}" \
      org.label-schema.schema-version="1.0"


ENV DOCTUM_CONFIG=$DOCTUM_CONFIG \
    DOCTUM_PROJECT_TITLE=$DOCTUM_PROJECT_TITLE \
    DOCTUM_SOURCE_DIR=$DOCTUM_SOURCE_DIR \
    DOCTUM_BUILD_DIR=$DOCTUM_BUILD_DIR \
    DOCTUM_CACHE_DIR=$DOCTUM_CACHE_DIR \
    DOCTUM_FLAGS=$DOCTUM_FLAGS \
    DOCTUM_SOURCE_REGEX=$DOCTUM_SOURCE_REGEX \
    DOCTUM_THEME=$DOCTUM_THEME

RUN set -xe && \
  apk add --no-cache --update inotify-tools git && \
  curl -s -S -L -o /tmp/doctum.phar ${DOCTUM_PHAR_URL} && \
  curl -s -S -L -o /tmp/doctum.sha256 ${DOCTUM_PHAR_SHA256_URL} && \
  (cd /tmp && sha256sum -s -c -w doctum.sha256) && \
  mv /tmp/doctum.phar /usr/local/bin/doctum && \
  rm -f /tmp/doctum.sha256 && \
  chmod +x /usr/local/bin/doctum && \
  mkdir -p "`dirname \"${DOCTUM_CONFIG}\"`"

COPY bin/* /usr/local/bin/
COPY etc/doctum/* /etc/doctum/

VOLUME ${DOCTUM_WORKDIR}
WORKDIR ${DOCTUM_WORKDIR}

ENTRYPOINT [ "doctum-entrypoint" ]
CMD [ "autoserve" ]

EXPOSE ${DOCTUM_SERVER_PORT}

# vim: ft=dockerfile:
