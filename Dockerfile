# Build the mobile app JS and assets
FROM node:9.2-slim
ENV SRC_DIR /src/fast_webapp

COPY farmer_mobile_app/package.json $SRC_DIR/farmer_mobile_app/package.json
COPY farmer_mobile_app/package-lock.json $SRC_DIR/farmer_mobile_app/package-lock.json

WORKDIR $SRC_DIR/farmer_mobile_app

RUN npm install && npm install --production

COPY farmer_mobile_app $SRC_DIR/farmer_mobile_app

RUN npm run build


# Build the Django server and inject the mobile app statics

FROM python:3.6
ENV SRC_DIR /src/fast_webapp

RUN apt-get update && \
    apt-get install -y netcat wget && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install utility to wait for Postgres to be ready upon startup
ENV DOCKERIZE_VERSION v0.6.1
RUN wget --no-check-certificate https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && rm dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz

# Install Python dependencies
# watch out bug on pipenv https://github.com/pypa/pipenv/issues/3363
RUN pip install pipenv==2018.10.13
ADD backend/Pipfile $SRC_DIR/backend/Pipfile
ADD backend/Pipfile.lock $SRC_DIR/backend/Pipfile.lock
WORKDIR $SRC_DIR/backend
RUN pipenv install

# Add the app codebase
ADD . $SRC_DIR

# Copy the built JS and assets files from the first container
# The JS and assets will be collected by Django collectstatic at container startup
COPY --from=0 $SRC_DIR/farmer_mobile_app/dist $SRC_DIR/farmer_mobile_app/dist

# Make entrypoint script executable
RUN chmod +x $SRC_DIR/entrypoint.sh
ENV PATH $PATH:$SRC_DIR

# Declare media upload volume
VOLUME ["/var/lib/fast/media"]

# Port that Django will listen on
EXPOSE 8080

# Backend startup script
ENTRYPOINT ["entrypoint.sh"]
