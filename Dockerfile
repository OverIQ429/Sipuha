FROM python:3.13

SHELL ["/bin/bash", "-c"]

RUN pip install --upgrade pip

RUN useradd -rms /bin/bash maxim && chmod 777 /opt /run

WORKDIR /sipuha

COPY --chown=linker:linker . .

RUN pip install -r requirements.txt

USER maxim

CMD ["uvicorn main:app --reload"]