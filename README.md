# Serums Data Lake API

This is the updated and near-final version of the Serums Data Lake API. There are many, many small tweaks and changes to the previous version that improve stability as well as maintainability. The core amongst these features is the testing suite. **This should be your first port of call when identifying issues as it should rapidly isolate any issues that you encounter.**

***
## Changes to the API

The basic functionality should remain identical including all of the end points. However, the API itself has been rewritten to use FastAPI instead of Flask. This has allowed for clearer documentation which can be found at either http://localhost:8000/docs or http://localhost:5000/docs depending on whether you are running this inside a docker container.

You will also notice that there are no JWT's provided by default in the front end. You must supply these yourself by accessing the [Serums Web Portal](https://flexpass.serums.cs.st-andrews.ac.uk/web_app/login_username.html). I will provide you with patient, healthcare provider, and hospital admin login details for each of the three hospitals.

***
## Requirements

In order to properly test this you will need access to the blockchain module. Potentially this could be cloned from GitHub and deployed locally, however, this will require a decent understanding of Kubenetes to achieve. Luckily, you can request access to the host server Fracas and the rest should be easy. Once you have that sorted, you can use the **Tunnels** program I have shared separately to ssh into Fracas and connect to the blockchain module running on port 30001. 

***
## Deploying

For deployment, you have a couple different options. Both have their pluses and minuses so I leave it to you how you to decide. I would suggest the Docker deployment is the easier of the two, however, it is entirely possible to use virtual environments on a unix system. The unix option will require a bit more setup and a few changes to files which we will cover below. But first...

***
### Docker deployment

The files are setup ready for Docker deployment so there should be no changes to make. **You must make sure you are tunnelled into the blockchain module in Fracas for many of the end points to work!**

Once ready, run:
```bash
docker-compose up --build
```

This will create the container and be attached to it so you can monitor the logs. The API will be ready to consume once the logs say `Application startup complete`.

You can now interact with it via your method of choice, however, I would suggest going to http://localhost:5000/docs as a starting point to see each of the end points and their expected inputs and outputs.

To run the test suite, you can pass the container a command to run it, however, the output is less than ideal. I would suggest you enter into the container and run it from within. To achieve this, open a new tab in your terminal and run:

```bash
docker ps
```

This will show you all of the currently running containers. You should see a container with the image name of `data_lake`. Copy the container id and run:

```bash
docker exec -it <container_id> bash
```

This will bring you into the running container and allow you to make live edits or to run the test suite. To do this, change into the code's directory:

```bash
cd api
```

Now you can run the tests:

```bash
python3.9 -m pytest -vv
```

You can also make edits to the code in real time by connecting [VS Code](https://code.visualstudio.com/Download) to it using the `Remote-Containers: Attach to Running Container...` via the command palette. The server is set to reload on changes so you should see these in real time.

***
### Virtual Environments

For development, I have been using a Python virtual environment on a Mac so this is a valid option for deployment if Docker is not your bag. You will require to declare a number of environment variables as well as have [PostgreSQL](https://www.postgresql.org/download/) installed[^1].

All of the environment variables can be found in the Dockerfile on lines that start `ENV`. You should `export` these either manually or by adding them to your `~/.bashrc` or `~/.zshrc` files. However, you must change 2 of these. These are:
- ALCHEMY_USER: Change `root` to `postgres`
- BC_PATH: Change `host.docker.internal` to `localhost`

You should now be able to create and activate a Python virtual environment and install the dependencies in `requirements.txt`. With that in place, you can run:

```bash
python3 databases/source_table.py
```
Then:

```bash
python3 databases/fill_source_tables.py
```

And finally:
```bash
uvicorn main:app --reload
```


[^1]: As well as having PostgreSQL installed, you will also need to set it up so that the *postgres user* can authenticated via password. This is typically achieved by altering the PostgreSQL configuration file *pg_hba.conf*. This can be found at `/Library/PostgreSQL/<version_number>/data/pg_hba.conf` on Mac and `/etc/postgresql/<version_number>/main/pg_hba.conf` on Ubuntu. Inside you will need to edit the line `local all all peer` to change *peer* to *md5*: `local all all md5` using the appropriate spacing as shown by the other records. You can now add a password for the `postgres user` by running `sudo -u postgres psql -c "ALTER USER postgres PASSWORD '<new-password>';"`. Restart the PostgreSQL service and you should now be able to login to PostgreSQL using a password.