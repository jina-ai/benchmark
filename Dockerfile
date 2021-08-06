ARG JINA_VER

FROM jinaai/jina:$JINA_VER

WORKDIR /app

ADD requirements.txt .

# install dependencies
RUN apt-get update && \
    apt-get install -y gcc time && \
    pip3 install -r requirements.txt

# run benchmark
ENTRYPOINT ["bash", "scripts/benchmark.sh"]