FROM debian:bookworm-20241016

RUN apt update && apt install -y \
    build-essential \
    python3 \
    python3-pip \
    curl \
    nodejs \
    npm
WORKDIR /akd-studios/lectorium/tools