FROM python:3.13-slim

ARG VERSION

LABEL maintainer="Henrique Sebastião <contato@henriquesebastiao.com>"
LABEL version="${VERSION}"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHON_COLORS=0

WORKDIR /code

COPY . /code/

RUN pip install --no-cache-dir --root-user-action ignore --upgrade pip \
    && pip install --no-cache-dir --root-user-action ignore -r requirements.txt

EXPOSE 8000

ENTRYPOINT ["./entrypoint.sh"]