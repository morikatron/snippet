FROM python:3

RUN apt-get update \
    && apt-get install -y texlive-latex-extra \
    latexmk \
    texlive-lang-japanese

RUN mkdir /code
WORKDIR /code
COPY ../requirements.txt /code/
RUN pip install -r requirements.txt
