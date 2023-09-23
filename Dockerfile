FROM python:3.7.17-slim
RUN apt-get update && \
    apt-get install -y \
        locales && \
	apt-get install -y locales-all && \
    rm -r /var/lib/apt/lists/*
RUN sed -i '/id_ID.UTF-8/s/^# //g' /etc/locale.gen && \
    locale-gen
RUN dpkg-reconfigure locales
WORKDIR /app
COPY . /app
RUN locale
RUN pip install -r requirements.txt
RUN python -m unittest credit_simulation/tests/test_credit_simulation.py
ENTRYPOINT ["python3","credit_menu.py"]