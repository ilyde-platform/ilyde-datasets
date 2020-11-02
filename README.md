## gRPC Service for Datasets

Questo progetto implementaun servizio gRPC per la gestione dei Datasets:

1. A riga di commando, eseguire il commando:

    ```shell script
    python ./server.py 
    ```
2. Compilando il Docker file:

    ```shell script
    docker build -t datasets-services:latest .
    docker run -d -p 50051:50051 -n datasets-services datasets-services:latest
    ```