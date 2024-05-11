# Eventor BackEnd - Flyer Generation

## What is this?

This part of the backend is composed of a microservice that leverages FastAPI, Pillow and AI-generated images to create flyers for events.

Its purpose is to isolate the responsibility of generating flyers to this particular endpoint while also establishing it behind a well defined interface for other code to reuse it over a distributed system.

## How to use it?

The workflow for this microservice is documented on the `Makefile` on this directory.

### Dependency Management
We are using [poetry](https://python-poetry.org/) for dependency management and python packaging.

You can enter the virtual enviroment via:
```
poetry shell
```

Install required dependencies:
```
poetry install
```

### Configuration

In order for this service to work you will need a working stable difussion instance on an `.env` file from which you can find a working example in this repository's `env.example`.

```
STABLE_DIFUSION_INSTANCE=<your instance>

# Maximum number of flyers in temporal memory
# after which a service unavailable message
# will be returned.
MAX_IN_MEMORY=3000 

# Maximum batch size that can be asked to the
# server.
MAX_BATCH_SIZE=5

# Path to the metro logo for your city.
# This is still a experimental feature.
METRO_PATH=<path to the metro logo in your city>

# Set to false if you only want to unit test
# without querying the SD instance feature.
TEST_END_TO_END=True

# A master API key to limit access from the
# internet and to be distributed to authorized
# clients.
API_MASTER_KEY=<a secret API key>
```

You can use this repository script `./setenvkey.sh` to generate a random `API_MASTER_KEY` on your `.env` file.

Just remember that without a reverse TLS proxy, this key could be easily intercepted and abused.

### Development

And you should be able to live run the server using [uvicorn](https://www.uvicorn.org/).
```
uvicorn main:app --app-dir ./app --reload
```

You can test this service inside the virtual environment using:
```
pytest .
```

### Deployment

For deployment, docker and docker composed can be used.

To build the image and run a server in port 8000, execute the following:
```
poetry export -f requirements.txt --without-hashes > requirements.txt
docker compose up --build
```
