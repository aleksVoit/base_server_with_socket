FROM ubuntu:20.04

RUN apt update
RUN apt install -y python3
RUN apt install -y python3-pip

WORKDIR /base_server

COPY . .

RUN pip install -r requirements.txt

RUN chmod +x start.sh

CMD ["./start.sh"]