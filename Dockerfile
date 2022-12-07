FROM ubuntu:jammy

ARG version

RUN apt-get update
RUN apt-get install -y python3.10 python3-pip git
RUN apt-get clean

RUN pip3.10 install CSCN73030-Attendance-Module==$version waitress

COPY --chown=root:root dockerfile-entrypoint.sh /entrypoint.sh

EXPOSE 8080/tcp
ENTRYPOINT [ "/entrypoint.sh" ]
