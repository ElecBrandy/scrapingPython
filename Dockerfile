FROM python:3.11.4

WORKDIR /usr/src
RUN apt-get update && apt-get install -y wget gnupg2

# 크롬 브라우저 설치
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    dpkg -i google-chrome-stable_current_amd64.deb || true && \
    apt-get install -f -y

# 크롬 드라이버 설치
RUN apt-get install -yqq unzip && \
    wget -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip && \
    unzip /tmp/chromedriver.zip -d /usr/local/bin/ && \
    rm /tmp/chromedriver.zip && \
    chmod +x /usr/local/bin/chromedriver

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# ENTRYPOINT를 사용하여 데몬 프로그램 실행
CMD ["python", "app/app.py"]

# CMD 명령어를 사용하여 컨테이너를 백그라운드에서 실행
ENTRYPOINT ["tail", "-f", "/dev/null"]