FROM python:3.11.4

# Install Firefox and other dependencies
RUN apt-get update && apt-get install -y firefox-esr xvfb

# Install xvfb and xauth packages
RUN apt-get install -y xvfb xauth

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# ENTRYPOINT를 사용하여 데몬 프로그램 실행
CMD ["xvfb-run", "--server-args='-screen 0 1024x768x24'", "--auto-servernum", "python", "app/scraping.py"]
