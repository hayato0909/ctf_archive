FROM ubuntu:24.04 AS base
ENV DEBIAN_FRONTEND=nointeractive

WORKDIR /app
ADD --chmod=755 build/challenge run

FROM pwn.red/jail
COPY --from=base / /srv
ENV JAIL_TIME=60 JAIL_CPU=100 JAIL_MEM=10M
