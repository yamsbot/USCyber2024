# Operating System
FROM ubuntu:20.04

RUN apt-get update -y && \
    apt-get install -y gcc gcc-multilib

COPY main.c flag.txt ynetd ./
RUN chmod +x ynetd

RUN gcc -o pwn_chall -fstack-protector-strong -z noexecstack -no-pie -Wl,-z,relro main.c

USER nobody

EXPOSE 1025
ENTRYPOINT ["./ynetd", "-p", "1025", "./pwn_chall"]
