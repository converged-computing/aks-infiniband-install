FROM ubuntu:20.04 AS debs

# Instructions:
# Download driver from Nvidia site (referenced below)
# docker build -t ghcr.io/converged-computing/aks-infiniband-install:ubuntu-20.04 .
# docker push ghcr.io/converged-computing/aks-infiniband-install:ubuntu-20.04
# Install ISO from nvidia

WORKDIR /opt/debs
USER root
COPY mlnx-en-4.9-7.1.0.0-ubuntu20.04-x86_64.iso ./mlnx-en-4.9-7.1.0.0-ubuntu20.04-x86_64.iso
FROM ubuntu:20.04

COPY --from=debs /opt/debs /opt/debs
COPY entrypoint.sh /entrypoint.sh 
COPY ./parse-links.py /opt/parse-links.py
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
