FROM ubuntu:bionic
RUN apt-get update
RUN apt install postgresql postgresql-contrib -y
EXPOSE 8000
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV DEBIAN_FRONTEND=nonintercative
ENV PGUSER=postgres
ENV PGPASSWORD=password
ENV ALCHEMY_USER=root
ENV ALCHEMY_PWD=password
USER postgres
RUN    /etc/init.d/postgresql start &&\
    psql --command "CREATE USER root WITH SUPERUSER PASSWORD 'password';" &&\
    createdb -O root root
USER root
RUN echo "host all  all    0.0.0.0/0  md5" >> /etc/postgresql/10/main/pg_hba.conf
RUN apt-get install software-properties-common -y
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get update
RUN apt-get install python3.9 python3-pip python3.9-distutils python3.9-dev -y
RUN python3.9 -m pip install --upgrade setuptools
RUN python3.9 -m pip install --upgrade pip
RUN python3.9 -m pip install --upgrade distlib
COPY requirements.txt /api/
RUN apt-get install libpq-dev -y
RUN python3.9 -m pip install -r /api/requirements.txt
COPY start_api.sh /scripts/
RUN chmod +x /scripts/start_api.sh
COPY main.py /api/
COPY /models /api/models/
COPY /tests /api/tests/
COPY /databases /api/databases/
COPY /auth /api/auth/
COPY /components /api/components/
COPY /control_files /api/control_files/
ENV BCPASSWORD=P5p3SNyA02lNoo9ti7OYI1aa0Tgcdrp+YwnZ1Dowl7A=
# ENV BC_PATH=http://192.168.122.24:30001
ENV BC_PATH=http://host.docker.internal:30001
ENV JWT_PATH=https://authentication.serums.cs.st-andrews.ac.uk/ua
ENV JWT_KEY="7@1+7bld_nx_79&12t5rl*d4)sc@i20w@-=)k-+to+6l@n=cgn"
ENV PGPORT=5432
ENTRYPOINT ["./scripts/start_api.sh"]
CMD ["/bin/bash"]