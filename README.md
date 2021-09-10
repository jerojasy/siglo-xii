# sigloxxi :stew::wine_glass::ramen:
Restaurante Siglo XXI API

Para levantar el servicio es necesario seguir los siguientes pasos:

1- Es necesario copiar el archivo .env.example como .env

2- Luego cambiar las configuraciones necesarias en el archivo .env(base de datos, puerto de salida,etc)

3- Una vez terminado los pasos anteriores es necesario construir las images de docker:

- docker-compose -f local.yml build

4- Cuando el comando termine de generar las imagenes es necesario levantar los servicios:

- docker-compose -f local.yml up -d

5- Para acceder a la ui debe acceder a la ruta:

- localhost:<puerto designado en el archivo .env>/docs
"# siglo-xvii" 
