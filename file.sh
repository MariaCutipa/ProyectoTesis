#!/bin/bash

# Variables
ID_BACK_C="service-csharp"
ID_BACK_F="service-flask"
ID_FRONT="service-vue"
BUILD_NAME_BACK_C="img-csharp"
BUILD_NAME_BACK_F="img-flask"
BUILD_NAME_FRONT="img-vue"
NETDATA_CONTAINER="netdata"

# Clonar el repositorio de GitHub
git clone https://github.com/ByronMG/recomendacion.git
cd aspnet-flask-vue

# Construcción y ejecución del backend Flask
cd backend/api-flask
docker build -t $BUILD_NAME_BACK_F .
docker run -it -d --rm -p 8081:5000 --name $ID_BACK_F $BUILD_NAME_BACK_F

# Construcción y ejecución del backend C#
cd ../api-csharp
docker build -t $BUILD_NAME_BACK_C .
docker run -it -d --rm -p 8082:8080 --name $ID_BACK_C --link $ID_BACK_F:flask $BUILD_NAME_BACK_C

# Construcción y ejecución del frontend Vue.js
cd ../../frontend
docker build -t "$BUILD_NAME_FRONT" .
docker run -it -d --rm -p 5173:5173 --name $ID_FRONT $BUILD_NAME_FRONT


# Monitoreo Netdata en un nuevo puerto (8085)
docker run -d --name $NETDATA_CONTAINER --cap-add=SYS_PTRACE --security-opt apparmor=unconfined -p 8085:19999 netdata/netdata

# Limpieza de recursos (descomentar si se desea ejecutar)
# sleep 30
# docker stop $ID_BACK_C
# docker stop $ID_BACK_F
# docker stop $ID_FRONT
# docker stop $NETDATA_CONTAINER
# docker rmi $BUILD_NAME_BACK_C
# docker rmi $BUILD_NAME_BACK_F
# docker rmi $BUILD_NAME_FRONT
