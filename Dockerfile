FROM ubuntu:bionic
RUN apt-get update
RUN apt install postgresql postgresql-contrib -y
EXPOSE 8000
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV DEBIAN_FRONTEND=nonintercative
ENV PGUSER=postgres
ENV PGPASSWORD=password
USER postgres
RUN    /etc/init.d/postgresql start &&\
    psql --command "CREATE USER root WITH SUPERUSER PASSWORD 'password';" &&\
    createdb -O root root
USER root
RUN echo "host all  all    0.0.0.0/0  md5" >> /etc/postgresql/10/main/pg_hba.conf
RUN apt-get install software-properties-common -y
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get update
RUN apt-get install python3.9 python3-pip python3.9-distutils -y
RUN python3.9 -m pip install --upgrade setuptools
RUN python3.9 -m pip install --upgrade pip
RUN python3.9 -m pip install --upgrade distlib

CMD ["/bin/bash"]