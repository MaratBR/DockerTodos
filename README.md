# DockerTodos

## Installation

1. Create new network:
   ```
   # docker network create --subnet=192.100.255.0/8 todo-net
   ```
2. Create new volume:
   ```
   # docker volume create todo-app
   ```
   
3. Create MongoDB container and run it:
   ```
   # docker run \
       -v todo-app:/data/db \
       --rm -d --name todo-app-mongo \
       --net todo-net \
       -h local-mongodb \
       --ip 192.100.255.10 \
       mongo
   ```
4. Run main application:
   ```
   # docker build -t todo-app-python .
   # docker run --name todo-app-instance -p 8080:8080 --net todo-net -d todo-app-python
   ```