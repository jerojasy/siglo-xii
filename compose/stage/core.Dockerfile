# FROM python:3.6.11
FROM python:3.6.11-alpine3.11
ENV ENVTYPE=local
ENV PYTHONUNBUFFERED 1
ENV https_proxy=http://10.46.0.210:3128
ENV http_proxy=http://10.46.0.210:3128
ENV APP_HOME=/home/app/web
RUN mkdir -p $APP_HOME
WORKDIR $APP_HOME

RUN apk update && apk add --no-cache mariadb-dev build-base gcc make python3-dev libffi-dev

RUN apk --no-cache add libaio libnsl libc6-compat curl && \
cd /tmp && \
curl -o instantclient-basiclite.zip https://download.oracle.com/otn_software/linux/instantclient/instantclient-basiclite-linuxx64.zip -SL && \
unzip instantclient-basiclite.zip && \
mv instantclient*/ /usr/lib/instantclient && \
rm instantclient-basiclite.zip && \
ln -s /usr/lib/instantclient/libclntsh.so.19.1 /usr/lib/libclntsh.so && \
ln -s /usr/lib/instantclient/libocci.so.19.1 /usr/lib/libocci.so && \
ln -s /usr/lib/instantclient/libociicus.so /usr/lib/libociicus.so && \
ln -s /usr/lib/instantclient/libnnz19.so /usr/lib/libnnz19.so && \
ln -s /usr/lib/libnsl.so.2 /usr/lib/libnsl.so.1 && \
ln -s /lib/libc.so.6 /usr/lib/libresolv.so.2 && \
ln -s /lib64/ld-linux-x86-64.so.2 /usr/lib/ld-linux-x86-64.so.2

ENV ORACLE_BASE /usr/lib/instantclient
ENV LD_LIBRARY_PATH /usr/lib/instantclient
ENV TNS_ADMIN /usr/lib/instantclient
ENV ORACLE_HOME /usr/lib/instantclient
ADD /requirements/$ENVTYPE.txt $APP_HOME
RUN pip install -r /home/app/web/$ENVTYPE.txt; mkdir /log;
COPY /src/ $APP_HOME
CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8080"]