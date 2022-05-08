FROM python:3.10

ENV PYTHONUNBUFFERED=1 \
    # prevents python creating .pyc files
    PYTHONDONTWRITEBYTECODE=1 \
    \
    # pip
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    \
    # poetry minimal version
    POETRY_VERSION=1.2.0b1 \
    # make poetry create the virtual environment in the project's root
    # it gets named `.venv`
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    # do not ask any interactive question
    POETRY_NO_INTERACTION=1

RUN pip install --upgrade pip \
 && pip install 'poetry>=$POETRY_VERSION'

WORKDIR /opt/app

# Install dependencies
COPY pyproject.toml poetry.lock ./

# Install the dependencies first, then add the versioning
# plugin to remove the need to mount the `.git` folder, and
# thus caching better.
RUN poetry install --without=dev --no-root \
 && poetry plugin add poetry-dynamic-versioning-plugin

# Install the project
COPY README.md ./
COPY src ./src
RUN --mount=source=.git,target=.git,type=bind \
    poetry dynamic-versioning \
 && poetry install --without=dev

CMD ["poetry", "run", "linkhub_exporter"]
