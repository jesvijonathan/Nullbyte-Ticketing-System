FROM python:3.10.12-slim-bullseye

ENV LDAP_SERVER="ldap://DC01.Skibbidi.exe"
ENV PATH="$PATH:/usr/local/lib/python3.10/site-packages"

WORKDIR /app

COPY requirements.txt .

RUN apt update -y && \
    apt-get install -y libldap2-dev libsasl2-dev ldap-utils build-essential curl && \
    apt-get clean

RUN pip3 install --no-cache-dir -r requirements.txt

# RUN curl -fsSL https://ollama.com/install.sh | sh
# RUN ollama pull llama3.2
# RUN ollama list
# RUN ollama rm nullbyte || true
# COPY ./Backend/Modelfile /Modelfile
# RUN ollama create nullbyte -f /Modelfile


# newer and better ollama commands
# sudo systemctl stop ollama 
# ollama serve
# ollama run jesvi/nullbyte



EXPOSE 5000

COPY . .

# ollama run nullbyte
CMD ["waitress-serve", "--host","0.0.0.0","--port","5000", "app:app"]


