ARG JINA_VER

FROM jinaai/jina:$JINA_VER

WORKDIR /app

# install dependencies
RUN apt-get update && \
    apt-get install -y gcc time && \
    pip3 install cmdbench==0.1.13

# run benchmark
ENTRYPOINT ["bash", "-x", "benchmark.sh"]