from bitnami/redis

ENV REDIS_PASSWORD default-password

COPY . /etc/redis

RUN redis-server --daemonize yes

