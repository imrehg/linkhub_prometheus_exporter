FROM python:3.9-slim

ENV POETRY_VERSION=1.2.0b1
RUN pip install --upgrade pip \
 && pip install 'poetry>=$POETRY_VERSION' \
 && poetry config virtualenvs.create false

WORKDIR /app

# Install dependencies
COPY pyproject.toml poetry.lock ./
RUN  --mount=source=.git,target=.git,type=bind \
    poetry plugin add poetry-dynamic-versioning-plugin \
 && poetry install --without=dev

# Install the project
COPY src ./src
# The below way works 
# RUN --mount=source=.git,target=.git,type=bind \
#     poetry dynamic-versioning \
#  && poetry install --without=dev

# CMD ["poetry", "run", "linkhub_exporter"]

RUN --mount=source=.git,target=.git,type=bind \
    poetry build \
 && pip install dist/*.whl

CMD ["linkhub_exporter"] 