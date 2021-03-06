FROM python:3.8

RUN apt-get -y update && \
    apt-get install -y libgl1-mesa-glx

WORKDIR "/opt/package"
RUN pip install torch
ADD . /opt/package
RUN pip install .[demo]

ENTRYPOINT ["inked-demo"]