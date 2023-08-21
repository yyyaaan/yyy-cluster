FROM fluent/fluentd:edge
# FROM fluent/fluentd:v1.12.0-debian-1.0
USER root
RUN ["gem", "install", "fluent-plugin-elasticsearch", "--no-document"]
COPY fluent.conf /fluentd/etc/fluent.conf
USER fluent