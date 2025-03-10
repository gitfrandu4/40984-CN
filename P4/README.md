# Práctica 4 - Contenedores en AWS con ECS

**Asignatura**: Computación en la Nube

**Fecha**: 20-12-2024

**Autor**: Francisco Javier López-Dufour Morales

<br>
<br>
<br>
<br>
<br>

<img src="img/Amazon_Web_Services_Logo.svg" alt="AWS Logo" width="200px" style="display: block; margin: 0 auto;"/>

<div class="page"/>

## Índice

- [Práctica 4 - Contenedores en AWS con ECS](#práctica-4---contenedores-en-aws-con-ecs)
  - [Índice](#índice)
  - [1. Introducción](#1-introducción)
  - [2. Objetivos](#2-objetivos)
    - [3.1. Creación de un contenedor Docker con una aplicación](#31-creación-de-un-contenedor-docker-con-una-aplicación)
    - [3.2. Creación de un repositorio en ECR y subida del contenedor](#32-creación-de-un-repositorio-en-ecr-y-subida-del-contenedor)
    - [3.3. Despliegue del contenedor usando ECS](#33-despliegue-del-contenedor-usando-ecs)
      - [3.3.1. Pasos para crear un Clúster de ECS con Instancias EC2](#331-pasos-para-crear-un-clúster-de-ecs-con-instancias-ec2)
      - [3.3.2. Arquitectura Final](#332-arquitectura-final)
      - [3.3.3. Análisis de Costos](#333-análisis-de-costos)
    - [3.4. Despliegue del contenedor usando Fargate y comparación](#34-despliegue-del-contenedor-usando-fargate-y-comparación)
      - [3.4.1. Pasos para Desplegar en Fargate](#341-pasos-para-desplegar-en-fargate)
      - [3.4.2. Comparación entre EC2 y Fargate](#342-comparación-entre-ec2-y-fargate)
      - [3.4.3. Arquitectura Final con Fargate](#343-arquitectura-final-con-fargate)
      - [3.4.4. Análisis de Costos](#344-análisis-de-costos)
    - [3.5. Actividad Extra: Despliegue de un cluster con varios contenedores](#35-actividad-extra-despliegue-de-un-cluster-con-varios-contenedores)
  - [4. Conclusiones](#4-conclusiones)
  - [5. Referencias](#5-referencias)
  - [6. Anexos](#6-anexos)
    - [Anexo 1: Docker Compose para WordPress y MariaDB](#anexo-1-docker-compose-para-wordpress-y-mariadb)
    - [Anexo 2: Implementación de la tarea en ECS (Punto 3.1)](#anexo-2-implementación-de-la-tarea-en-ecs-punto-31)
    - [Anexo 3: Implementación de la tarea en Fargate](#anexo-3-implementación-de-la-tarea-en-fargate)

<div class="page"/>

## 1. Introducción

En esta práctica exploraremos el uso de contenedores en AWS utilizando el servicio Amazon Elastic Container Service (ECS). El objetivo es familiarizarse con la creación y despliegue de contenedores Docker en AWS, gestionando repositorios en ECR y comparando diferentes métodos de despliegue, incluyendo Fargate.

**Tecnologías Utilizadas**:

- **Docker**: Plataforma que permite empaquetar aplicaciones y sus dependencias en contenedores, asegurando que se ejecuten de manera consistente en diferentes entornos.
- **Amazon ECS**: Servicio de orquestación de contenedores que facilita el despliegue, gestión y escalado de aplicaciones en contenedores en AWS.
- **Amazon ECR**: Registro de contenedores gestionado que facilita el almacenamiento, gestión y despliegue de imágenes Docker.
- **AWS Fargate**: Motor de cómputo serverless para contenedores que elimina la necesidad de gestionar servidores, permitiendo ejecutar contenedores directamente.

<div class="page"/>

## 2. Objetivos

- Crear un contenedor Docker con una aplicación sencilla para comprobar su funcionamiento.
- Configurar un repositorio en Amazon ECR y subir el contenedor creado.
- Desplegar el contenedor usando Amazon ECS.
- Desplegar el contenedor usando AWS Fargate y comparar la experiencia con el despliegue anterior.
- Extender el despliegue para implementar un cluster con varios contenedores distintos.

<div class="page"/>

### 3.1. Creación de un contenedor Docker con una aplicación

> **Objetivo**: Crear un contenedor Docker que contenga una aplicación que permita comprobar su funcionamiento, como por ejemplo una página web sencilla.

**Conceptos Clave**:

- **ECS** (_Elastic Container Service_): Servicio de orquestación de contenedores que permite ejecutar y escalar aplicaciones en contenedores.
- **Clúster ECS**: Conjunto lógico de recursos en el que se ejecutan las tareas y servicios de ECS.
- **Definición de Tarea** (_Task Definition_): Plantilla que describe uno o más contenedores (por ejemplo, imagen de contenedor, variables de entorno, puertos, volúmenes).
- **Servicio ECS**: Gestiona la ejecución de tareas y asegura que se mantenga el número deseado de tareas en ejecución.

**Pasos a seguir**:

1. **Instalar Docker**:

   - Asegurarse de tener Docker instalado en el sistema local.
   - [Guía de instalación de Docker](https://docs.docker.com/get-docker/)

2. **Crear la aplicación**:

   - Vamos a utilizar una aplicación existente, WordPress, para simplificar la configuración.
   - Descargamos la imagen oficial de WordPress desde Docker Hub: `docker pull wordpress:latest`
   - Descargar también la imagen de MariaDB para la base de datos: `docker pull mariadb:latest`

3. **Escribir el Dockerfile**:

   - Crear un archivo `docker-compose.yml` que defina los servicios de WordPress y MariaDB.
   - Ejemplo de `docker-compose.yml`: [Anexo 1](#anexo-1-docker-compose-para-wordpress-y-mariadb)

4. **Construir y ejecutar los contenedores**:

   - Ejecutar el comando para construir y ejecutar los contenedores:

     ```bash
     docker-compose up
     ```

5. **Probar el contenedor localmente**:

   - Acceder a `http://localhost` para comprobar que la aplicación de WordPress funciona.

  <img src="img/wordpress.png" alt="WordPress" width="600"/>

<div class="page"/>

### 3.2. Creación de un repositorio en ECR y subida del contenedor

> **Descripción**: Configurar un repositorio en Amazon Elastic Container Registry (ECR) y subir la imagen del contenedor creado en el paso anterior.

**Pasos**:

1. **Creación del repositorio en ECR**:

   - Accedemos a la consola de AWS ECR.
   - Creamos un nuevo repositorio privado.
   - Anotar el URI del repositorio: `[account].dkr.ecr.[region].amazonaws.com/my-app`.
     - En nuestro caso, el URI del repositorio quedaría: `491250998585.dkr.ecr.us-east-1.amazonaws.com/wordpress`
   - Mutabilidad de la imagen: Seleccionamos "Mutable" para poder sobreescribir la imagen.
   - Configuración de cifrado: Seleccionamos "KMS" y dejamos la configuración por defecto.
   - Análisis de imágenes: habilitamos la opción "Análisis de imágenes" para poder escanear las imágenes en busca de vulnerabilidades automáticamente al subirlas al repositorio.

2. **Configuración de las credenciales de AWS**:

   - Instalamos y configuramos AWS CLI en el sistema local.
   - [Guía de instalación de AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html)
   - Configuramos las credenciales con `aws configure`.

3. **Iniciar sesión en ECR**:

   - Ejecutar el comando de inicio de sesión en ECR:

   ```bash
   aws ecr get-login-password --region [region] | docker login --username AWS --password-stdin [account].dkr.ecr.[region].amazonaws.com
   ```

   En nuestro caso:

   ```bash
   aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 491250998585.dkr.ecr.us-east-1.amazonaws.com
   Login Succeeded
   ```

4. **Etiquetar la imagen para ECR**:

   - Etiquetar la imagen local para que coincida con el repositorio de ECR:

     ```bash
     docker tag my-app:latest [account].dkr.ecr.[region].amazonaws.com/my-app:latest
     ```

     En nuestro caso:

     ```bash
     docker tag wordpress:latest 491250998585.dkr.ecr.us-east-1.amazonaws.com/wordpress:latest
     docker tag mariadb:11.0.2 491250998585.dkr.ecr.us-east-1.amazonaws.com/mariadb:latest
     ```

5. **Subir la imagen a ECR**:

   - Ejecutar el comando para subir la imagen:

     ```bash
     docker push [account].dkr.ecr.[region].amazonaws.com/my-app:latest
     ```

     En nuestro caso:

     ```bash
     docker push 491250998585.dkr.ecr.us-east-1.amazonaws.com/wordpress:latest
     docker push 491250998585.dkr.ecr.us-east-1.amazonaws.com/mariadb:latest
     ```

6. **Verificar la imagen en ECR**:

   - Acceder a la consola de ECR y verificar que la imagen se ha subido correctamente.

   <img src="img/ecr-image.png" alt="ECR Image" width="600"/>

<div class="page"/>

### 3.3. Despliegue del contenedor usando ECS

> **Descripción**: Ahora crearemos un clúster en ECS usando instancias EC2, definiendo la tarea y el servicio. Esto proporciona más control sobre la infraestructura subyacente, permitiendo por ejemplo el uso de tipos de instancia específicos y estrategias de escalado personalizadas.

#### 3.3.1. Pasos para crear un Clúster de ECS con Instancias EC2

1. **Crear un clúster de ECS**:

   - Acceder a la consola de Amazon ECS.
   - Crear un nuevo clúster (por ejemplo, con EC2 Linux + Networking).
     - Nombre: `wordpress-cluster`
   - Configuración de la Infraestructura:
     - Instancias EC2
     - Grupo de Auto Scaling: Crear un nuevo grupo de Auto Scaling.
     - Modelo de aprovisionamiento: `On-Demand`.
     - Imagen de la máquina EC2: `Amazon Linux 2 (kernel 5.10/arm64)`.
       - Es importante seleccionar una imagen compatible con ARM si vamos a utilizar instancias ARM.
     - Tipo de instancias EC2: `t2.medium` para soportar la carga de WordPress y la base de datos. Ajustar según las necesidades de la aplicación.
       - **Nota**: Ajustar el tipo de instancia según los requisitos de la aplicación.
     - Rol de instancia: Crear un nuevo rol de IAM o seleccionar uno existente. (`LabInstanceProfile` en nuestro caso).
     - Capacidad deseada:
       - Número de instancias: `1`.
       - Capacidad máxima: `2`.
     - Par de claves: Seleccionar un par de claves existente o crear uno nuevo. (`vockey` en nuestro caso).
     - Tamaño del volumen raíz: `30 GiB`.
   - Configuración de la red:
     - VPC: Seleccionamos la VPC por defecto.
     - Subredes: Seleccionamos todas las subredes.
     - Grupo de seguridad: Crear un nuevo grupo de seguridad o seleccionar uno existente.
       - Debemos asegurarnos de que permite tráfico en los puertos necesarios (80 para HTTP y 3306 para MariaDB).
     - Balanceador de carga: No seleccionar balanceador de carga.
     - Asignar automáticamente direcciones IP públicas: `Activado`.
   - Monitoreo, Cifrado y Etiquetas: Mantenemos la configuración por defecto.

Resumen de la configuración:

<img src="img/ecs-cluster.png" alt="ECS Cluster" width="600"/>

**Nota**: Debemos asegurarnos de que las imágenes de los contenedores soporten la arquitectura elegida.

2. **Definir una tarea (_Task Definition_)**:

Como estamos ejecutando dos contenedores (WordPress y MariaDB) que necesitan comunicarse entre sí, usaremos una definición de tarea que incluye ambos contenedores.

- Accedemos a **Definiciones de Tareas** en la consola de ECS.
  - Familia de la tarea: `wordpress-task`.
  - Requisitos de infraestructura:
    - Tipo de Lanzamiento: `EC2`.
    - Sistema operativo: `Linux/ARM64`.
      - **Nota**: Si estamos utilizando instancias ARM, debemos asegurarnos de que las imágenes de los contenedores son compatibles con ARM.
    - Modo de red: `bridge`.
    - CPU: `1 vCPU`.
    - Memoria: `1 GB`.
      - **Nota**: Ajustar la memoria y CPU según los requisitos de la aplicación.
    - Rol de tarea: Crear un nuevo rol de IAM o seleccionar uno existente. (`LabRole` en nuestro caso).
    - Rol de ejecución de tareas: Crear un nuevo rol de IAM o seleccionar uno existente. (`LabRole` en nuestro caso).
  - Contenedor 1: **mariadb**
    - Nombre: `mariadb`.
    - Contenedor esencial: `Si`.
    - URI de la imagen: `491250998585.dkr.ecr.us-east-1.amazonaws.com/mariadb:latest`.
    - Mapeo de puertos:
      - Puerto de anfitrión: `0`. (mapeo dinámico al host).
      - Puerto de contenedor: `3306`.
      - Protocolo: `tcp`.
      - Nombre: `mariadb-3306-tcp`.
    - Variables de entorno:
      - `MYSQL_ROOT_PASSWORD`: root
      - `MYSQL_DATABASE`: wordpress
      - `MYSQL_USER`: wordpress
      - `MYSQL_PASSWORD`: wordpress
  - Contenedor 2: **wordpress**
    - Nombre: `wordpress`.
    - URI de la imagen: `491250998585.dkr.ecr.us-east-1.amazonaws.com/wordpress:latest`.
    - Contenedor esencial: `Si`.
    - Mapeo de puertos:
      - Puerto de anfitrión: `80`.
      - Puerto de contenedor: `80`.
      - Protocolo: `tcp`.
      - Nombre: `wordpress-80-tcp`.
      - Protocolo de la aplicación: `http`.
    - Ordenación de la dependencia de inicio:
      - Nombre del contenedor: `mariadb`. Condiciones: `Start`. (Para asegurar que MariaDB se inicia antes de WordPress).
    - Variables de entorno:
      - `WORDPRESS_DB_HOST`: mariadb:3306
      - `WORDPRESS_DB_USER`: wordpress
      - `WORDPRESS_DB_PASSWORD`: wordpress
      - `WORDPRESS_DB_NAME`: wordpress
    - Configuración de red de contenedores:
      - Enlaces: `mariadb`. Alias: `mariadb`. (Como estamos utilizando el modo bridge, necesitamos enlazar los contenedores para que puedan comunicarse).

Resumen de la configuración:

<img src="img/task-definition.png" alt="Task Definition" width="600"/>

Esta configuración centralizada en la `Task Definition` proporciona una plantilla reutilizable, facilitando futuras actualizaciones y despliegues.

3. **Crear un servicio de ECS**:

   - Acceder a Servicios:
     - En la consola de ECS, seleccionamos `Clusters`, luego seleccionamos nuestro clúster `wordpress-cluster` y procedemos a crear un servicio.
   - Configuración el Servicio:
     - Entorno:
       - Tipo de lanzamiento: `EC2`.
     - Configuración de la implementación:
       - Tipo de implementación: `Servicio`.
       - Familia de la tarea: `wordpress-task`. (la definición de tarea que creamos anteriormente).
       - Nombre del servicio: `wordpress-service`.
       - Tipo de servicio: `REPLICA`. (para mantener un número fijo de tareas en ejecución).
       - Tareas deseadas: `1`.
   - Mantenemos las opciones por defecto en el resto de las secciones.

Resumen de la configuración:

<img src="img/service.png" alt="Service" width="600"/>

El servicio mantiene el número de tareas especificado en ejecución, lo que aporta resiliencia ante fallos. La creación del servicio permite escalar el número de contenedores de forma dinámica y asegura alta disponibilidad (si se configura con múltiples tareas y balanceador de carga).

4. **Probar el despliegue**:
   - Comprobar que las instancias de tarea están en ejecución.
     - <img src="img/ecs-tasks.png" alt="ECS Tasks" width="600"/>
   - Obtener la dirección IP o el balanceador de carga para acceder a la aplicación.
     - En nuestro caso, la dirección IP pública de la instancia EC2 es `ec2-54-144-88-19.compute-1.amazonaws.com`

<img src="img/wodpress-service.png" alt="WordPress Service" width="600"/>
<img src="img/wordpress-service-2.png" alt="WordPress EC2" width="600"/>

**Notas**:

- Debemos asegurarnos de que el rol de ejecución de tareas de ECS (`ECS Task Execution Role`) tenga permisos suficientes para acceder a ECR.
- Verificar que el grupo de seguridad permita tráfico en el puerto `80`.
- Ajustar recursos según las necesidades reales, evitando sobrecostes o subdimensionamiento.

<div class="page"/>

#### 3.3.2. Arquitectura Final

<img src="img/arquitectura_ecs_con_ec2.png" alt="ECS Architecture" width="400"/>

La arquitectura final incluye un clúster de ECS con instancias EC2, una definición de tarea con dos contenedores (WordPress y MariaDB) y un servicio que mantiene una tarea en ejecución. La comunicación entre los contenedores se realiza a través de la red interna de ECS.

<div class="page"/>

#### 3.3.3. Análisis de Costos

<img src="img/ecs-costs.png" alt="ECS Costs" width="600"/>

Los costos principales se dividen entre instancias EC2 ($16.86 USD/mes), almacenamiento de imágenes en ECR ($0.08 USD/mes), y transferencia de datos ($9.00 USD/mes). Los costos adicionales opcionales incluyen balanceadores de carga (ELB), almacenamiento adicional (EBS) y monitoreo (CloudWatch).

| Servicio                                    | Costo Mensual (USD) | Costo Anual (USD)     |
| ------------------------------------------- | ------------------- | --------------------- |
| **Amazon EC2**                              | $16.86              | $202.32               |
| **Amazon Elastic Container Registry (ECR)** | $0.08               | $0.96                 |
| **AWS Data Transfer**                       | $9.00               | $108.00               |
| **Elastic Load Balancer (ELB)** (opcional)  | ~$16.20             | ~$194.40              |
| **Almacenamiento EBS** (opcional)           | $1.00               | $12.00                |
| **AWS CloudWatch** (opcional)               | ~$1.10              | ~$13.20               |
| **Total Estimado**                          | **$27.94 - $44.24** | **$335.28 - $530.88** |

<div class="page"/>

### 3.4. Despliegue del contenedor usando Fargate y comparación

> **Descripción**: Desplegar la misma aplicación (WordPress y MariaDB) en AWS ECS, pero empleando el tipo de lanzamiento Fargate en lugar de EC2. Esto facilitará la comparación entre ambas opciones, resaltando las diferencias en la gestión de infraestructura, costos, escalabilidad y simplicidad de la operación.

**Consideraciones Previas**:

- Arquitectura sin servidores (Serverless): Fargate es un servicio serverless que permite ejecutar contenedores sin necesidad de gestionar servidores, clústeres ni instancias EC2 subyacentes. Esto simplifica el mantenimiento pero puede tener un impacto en el costo.

**Compatibilidad y Requerimientos**:

- Asegurar que las imágenes y configuraciones empleadas anteriormente (WordPress, MariaDB) sean compatibles con Fargate. Normalmente lo son, pero es importante recordar:
  - Fargate no soporta el modo de red `bridge`, así que en la `Task Definition` hay que emplear `awsvpc`.
  - Cada contenedor debe contar con puertos definidos en el modo awsvpc.

**Costos y Dimensionamiento**:

- Con Fargate se paga por tiempo de cómputo y recursos asignados (vCPU y RAM) a las tareas, no por la infraestructura persistente como en EC2. Ajustar adecuadamente la CPU y la memoria asignadas a la `Task Definition` evitará sobrecostos.

#### 3.4.1. Pasos para Desplegar en Fargate

1. **Crear un nuevo Clúster de ECS**:

   - Acceder a la consola de ECS.
   - Configuración del Cluster
     - Nombre: `wordpress-fargate-cluster`.
   - Infraestructura
     - Tipo de lanzamiento: `FARGATE`.
   - Monitoreo, Cifrado y Etiquetas: Mantenemos la configuración por defecto.

2. **Configurar la Task Definition para Fargate**:

Creamos una nueva definición de tarea para Fargate, basada en la definición anterior pero con algunas modificaciones:

- Familia de la tarea: `wordpress-fargate-task`.
- Requisitos de infraestructura:
  - Tipo de Lanzamiento: `FARGATE`.
  - Sistema operativo/arquitectura: `Linux/ARM64`.
    - **Nota**: Asegurarse de que las imágenes de los contenedores sean compatibles con ARM.
  - CPU: `0.5 vCPU`.
  - Memoria: `1 GB`.
  - Rol de tarea: `LabRole`. (mismo rol que en el despliegue anterior).
  - Rol de ejecución de tareas: `LabRole`.
  - Red: `awsvpc`.
- Contenedor 1: **mariadb**
  - URI de la imagen: `491250998585.dkr.ecr.us-east-1.amazonaws.com/mariadb:latest`.
  - Mapeo de puertos:
    - Puerto de contenedor: `3306`.
    - Protocolo: `tcp`.
  - Variables de entorno:
    - `MYSQL_ROOT_PASSWORD`: root
    - `MYSQL_DATABASE`: wordpress
    - `MYSQL_USER`: wordpress
    - `MYSQL_PASSWORD`: wordpress
- Contenedor 2: **wordpress**
  - URI de la imagen: `491250998585.dkr.ecr.us-east-1.amazonaws.com/wordpress:latest`.
  - Mapeo de puertos:
    - Puerto de contenedor: `80`.
    - Protocolo: `tcp`.
  - Variables de entorno:
    - `WORDPRESS_DB_HOST`: mariadb:3306
    - `WORDPRESS_DB_USER`: wordpress
    - `WORDPRESS_DB_PASSWORD`: wordpress
    - `WORDPRESS_DB_NAME`: wordpress
  - Ordenación de la dependencia de inicio:
    - Nombre del contenedor: `mariadb`. Condiciones: `Start`.

Cambios en la configuración de la `Task Definition`:

- No es necesario mapear a un puerto de host (en Fargate el puerto del host se asigna automáticamente).
- Retirar dependencias de tipo links ya que con awsvpc cada contenedor obtiene su propia interfaz de red y se comunican a través de la dirección interna asignada por la VPC (usando el nombre del contenedor como referencia en las variables de entorno).

3. **Crear el Servicio en Modo Fargate**:

En la consola de ECS, ir a la sección “Servicios” dentro del clúster existente o crear uno nuevo si se desea separar ambientes.

- Entorno:
  - Clúster: `wordpress-fargate-cluster`.
  - Estrategia de proveedor de capacidad: `FARGATE`.
- Configuración de la implementación:
  - Tipo de aplicación: `Servicio`.
  - Nombre del servicio: `wordpress-fargate-service`.
  - Tipo de servicio: `REPLICA`.
  - Tareas deseadas: `1`.
- Redes:
  - VPC: Seleccionar la VPC y subredes configuradas para Fargate.
  - Asignar automáticamente direcciones IP públicas: `Activado`.
  - Grupo de seguridad: Seleccionar un grupo de seguridad que permita tráfico en los puertos necesarios (80 y 3306).

<img src="img/fargate-service.png" alt="Fargate Service" width="600"/>

4. **Desplegar y Probar**:

- Crear el servicio y esperar a que las tareas se inicien.

<img src="img/fargate-tasks.png" alt="Fargate Tasks" width="600"/>

- Una vez en estado `RUNNING`, obtener la dirección IP pública asignada a la tarea.
- Acceder desde el navegador a la URL y verificar que WordPress funcione correctamente.

**Resultado del Despliegue**

<img src="img/ecs-fargate.png" alt="ECS Fargate" width="600"/>

Tras intentar desplegar los contenedores (WordPress y MariaDB) en ECS utilizando Fargate, encontramos un problema: **los contenedores dentro de la misma tarea no lograron establecer comunicación entre sí**.

**Análisis del Problema**

Según la documentación oficial de AWS ECS:

> "Containers that belong to the same task can also communicate over the localhost interface." ([Fuente: AWS Docs](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/fargate-task-networking.html))

En teoría, al usar el modo de red `awsvpc`, los contenedores de una misma tarea pueden comunicarse utilizando el nombre del contenedor como DNS. Sin embargo, en la práctica, el contenedor de WordPress no pudo resolver correctamente el nombre del contenedor de MariaDB (`mariadb`) ni conectarse al puerto `3306`.

**Posibles Causas**

- Problemas con la configuración de DNS en Fargate para la resolución de nombres entre contenedores.
- La dependencia `dependsOn` no garantiza que MariaDB esté listo antes de que WordPress intente conectarse.
- Limitaciones intrínsecas del diseño de Fargate para este caso específico de comunicación directa entre contenedores.

**Propuestas de Solución**

1. **Dividir los contenedores en dos servicios ECS separados:**

   - Crear un servicio para MariaDB y otro para WordPress, conectándolos mediante:
     - Un endpoint público para MariaDB (con acceso restringido a la IP del servicio de WordPress).
     - Un balanceador de carga interno (opcional).
   - Ventaja: Esto desacopla los contenedores, lo que permite una configuración más robusta y escalable.
   - Desventaja: Aumenta la complejidad de la configuración.

2. **Usar un motor de bases de datos gestionado (RDS):**
   - Reemplazar MariaDB en contenedor con un servicio RDS de Amazon (MariaDB o MySQL).
   - Ventaja: Simplifica la configuración, mejora la disponibilidad y permite un escalado más eficiente.
   - Desventaja: Puede ser más costoso en escenarios pequeños.

#### 3.4.2. Comparación entre EC2 y Fargate

| Característica                 | EC2                                                        | Fargate                                                 |
| ------------------------------ | ---------------------------------------------------------- | ------------------------------------------------------- |
| **Gestión de Infraestructura** | Requiere aprovisionar y gestionar instancias manualmente.  | Totalmente serverless, AWS gestiona la infraestructura. |
| **Flexibilidad**               | Alta, permite elegir tipos de instancias específicas.      | Limitada a las configuraciones disponibles en Fargate.  |
| **Escalabilidad**              | Puede configurarse manualmente o mediante Auto Scaling.    | Escala automáticamente según la carga de trabajo.       |
| **Costo**                      | Menor costo en cargas de trabajo constantes y predecibles. | Puede ser más caro en cargas pequeñas o irregulares.    |
| **Simplicidad**                | Requiere conocimientos de gestión de infraestructura.      | Más sencillo, adecuado para usuarios nuevos.            |
| **Disponibilidad**             | Depende de la configuración de las instancias y la red.    | Alta disponibilidad integrada por defecto.              |

<div class="page"/>

#### 3.4.3. Arquitectura Final con Fargate

<img src="img/arquitectura_ecs_con_fargate.png" alt="Fargate Architecture" width="400"/>

La arquitectura final con Fargate incluye un clúster de ECS con tareas ejecutadas en el servicio Fargate, sin necesidad de gestionar instancias EC2. Aunque Fargate ofrece una solución serverless y simplificada, puede presentar desafíos en la comunicación entre contenedores dentro de la misma tarea.

<div class="page"/>

#### 3.4.4. Análisis de Costos

| Servicio                                    | Costo Mensual (USD) | Costo Anual (USD)     |
| ------------------------------------------- | ------------------- | --------------------- |
| **Fargate Compute**                         | $28.80              | $345.60               |
| **Amazon Elastic Container Registry (ECR)** | $0.08               | $0.96                 |
| **AWS Data Transfer**                       | $9.00               | $108.00               |
| **Elastic Load Balancer (ELB)** (opcional)  | ~$16.20             | ~$194.40              |
| **AWS CloudWatch** (opcional)               | ~$1.10              | ~$13.20               |
| **Total Estimado**                          | **$38.98 - $55.18** | **$467.76 - $662.16** |

**Observaciones sobre costos con Fargate y EC2**:

- **EC2** es más económico en configuraciones predecibles y constantes, con mayor flexibilidad para personalizar los recursos.
- **Fargate** elimina la necesidad de gestionar infraestructura, pero tiene un costo mayor debido al modelo de pago por recursos asignados.

<div class="page"/>

### 3.5. Actividad Extra: Despliegue de un cluster con varios contenedores

En esta actividad se realizó el despliegue de un clúster con múltiples contenedores utilizando AWS ECS en dos configuraciones principales:

1. **ECS con instancias EC2:**

   - Se desplegó un clúster ECS utilizando instancias EC2 como capacidad subyacente.
   - Los contenedores de WordPress y MariaDB se ejecutaron en una sola tarea, aprovechando el modo de red `bridge` para facilitar la comunicación entre ellos.
   - Este despliegue permitió una mayor personalización en las configuraciones de red y almacenamiento, pero requirió la gestión manual de la infraestructura subyacente.

2. **ECS con Fargate:**
   - Se intentó realizar el despliegue de los mismos contenedores (WordPress y MariaDB) en un clúster ECS utilizando Fargate, eliminando la necesidad de gestionar servidores.
   - Aunque Fargate ofrece una solución más simplificada y serverless, encontramos problemas con la conectividad interna entre los contenedores en la misma tarea.
   - Según la documentación oficial, los contenedores deberían comunicarse mediante el localhost o utilizando el nombre del contenedor como DNS. Sin embargo, en la práctica, WordPress no logró conectarse a MariaDB debido a posibles limitaciones o errores en la configuración del modo de red `awsvpc`.

<div class="page"/>

## 4. Conclusiones

En esta práctica se ha demostrado el proceso completo de empaquetar una aplicación en contenedores utilizando Docker, alojar las imágenes resultantes en el registro privado de Amazon ECR y desplegarlas en AWS ECS. La experiencia ha permitido comparar dos modos de despliegue distintos: el uso de instancias EC2 para el clúster y la opción serverless que ofrece Fargate.

Como resultado, la práctica ha proporcionado una serie de aprendizajes y consideraciones:

- **Aprendizaje de Orquestación de Contenedores**: La práctica proporcionó una comprensión sólida sobre cómo orquestar contenedores utilizando Amazon ECS, gestionando tanto la infraestructura subyacente como las configuraciones serverless.

- **Impacto de las Decisiones de Despliegue**: Al comparar EC2 y Fargate, se evidenció cómo las decisiones de despliegue afectan no solo los costos, sino también la flexibilidad y la carga operativa. Esto es importante para seleccionar la mejor solución según los requisitos específicos de cada proyecto.

- **Desafíos Encontrados**: La dificultad para la comunicación entre contenedores en Fargate resaltó la importancia de comprender las configuraciones de red al trabajar con servicios serverless, lo que ayudará en futuras implementaciones a evitar o resolver problemas similares.

- **Recomendaciones para Futuros Proyectos**: Considerar el uso de servicios gestionados adicionales, como Amazon RDS para bases de datos, puede simplificar la arquitectura y mejorar la escalabilidad y disponibilidad de las aplicaciones.

<div class="page"/>

## 5. Referencias

- [Amazon ECS Developer Guide](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/Welcome.html)
- [Amazon ECR User Guide](https://docs.aws.amazon.com/AmazonECR/latest/userguide/what-is-ecr.html)
- [AWS Fargate Documentation](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/AWS_Fargate.html)
- [Docker Documentation](https://docs.docker.com/)
- [AWS CLI Command Reference](https://docs.aws.amazon.com/cli/latest/reference/)

<div class="page"/>

## 6. Anexos

### Anexo 1: Docker Compose para WordPress y MariaDB

```yaml
version: '3.8'

services:
db:
  image: mariadb:11.0.2
  restart: always
  ports:
    - '3306:3306'
  environment:
    MYSQL_ROOT_PASSWORD: root
    MYSQL_DATABASE: wordpress
    MYSQL_USER: wordpress
    MYSQL_PASSWORD: wordpress
wordpress:
  image: wordpress:latest
  restart: always
  ports:
    - '80:80'
  depends_on:
    - db
  environment:
    WORDPRESS_DB_HOST: db:3306
    WORDPRESS_DB_USER: wordpress
    WORDPRESS_DB_PASSWORD: wordpress
    WORDPRESS_DB_NAME: wordpress
    WORDPRESS_CONFIG_EXTRA: |
      /** disable wp core auto update */
      define('WP_AUTO_UPDATE_CORE', false);
```

### Anexo 2: Implementación de la tarea en ECS (Punto 3.1)

```json
{
  "family": "wordpress-task",
  "containerDefinitions": [
    {
      "name": "mariadb",
      "image": "491250998585.dkr.ecr.us-east-1.amazonaws.com/mariadb:latest",
      "cpu": 0,
      "portMappings": [
        {
          "name": "mariadb-3306-tcp",
          "containerPort": 3306,
          "hostPort": 0,
          "protocol": "tcp"
        }
      ],
      "essential": true,
      "environment": [
        {
          "name": "MYSQL_DATABASE",
          "value": "wordpress"
        },
        {
          "name": "MYSQL_PASSWORD",
          "value": "wordpress"
        },
        {
          "name": "MYSQL_ROOT_PASSWORD",
          "value": "root"
        },
        {
          "name": "MYSQL_USER",
          "value": "wordpress"
        }
      ],
      "environmentFiles": [],
      "mountPoints": [],
      "volumesFrom": [],
      "ulimits": [],
      "systemControls": []
    },
    {
      "name": "wordpress",
      "image": "491250998585.dkr.ecr.us-east-1.amazonaws.com/wordpress:latest",
      "cpu": 0,
      "links": ["mariadb:mariadb"],
      "portMappings": [
        {
          "name": "wordpress-80-tcp",
          "containerPort": 80,
          "hostPort": 80,
          "protocol": "tcp",
          "appProtocol": "http"
        }
      ],
      "essential": true,
      "environment": [
        {
          "name": "WORDPRESS_DB_USER",
          "value": "wordpress"
        },
        {
          "name": "WORDPRESS_DB_HOST",
          "value": "mariadb:3306"
        },
        {
          "name": "WORDPRESS_DB_PASSWORD",
          "value": "wordpress"
        },
        {
          "name": "WORDPRESS_DB_NAME",
          "value": "wordpress"
        }
      ],
      "environmentFiles": [],
      "mountPoints": [],
      "volumesFrom": [],
      "dependsOn": [
        {
          "containerName": "mariadb",
          "condition": "START"
        }
      ],
      "systemControls": []
    }
  ],
  "taskRoleArn": "arn:aws:iam::491250998585:role/LabRole",
  "executionRoleArn": "arn:aws:iam::491250998585:role/LabRole",
  "networkMode": "bridge",
  "volumes": [],
  "placementConstraints": [],
  "requiresCompatibilities": ["EC2"],
  "cpu": "1024",
  "memory": "1024",
  "runtimePlatform": {
    "cpuArchitecture": "ARM64",
    "operatingSystemFamily": "LINUX"
  }
}
```

### Anexo 3: Implementación de la tarea en Fargate

```json
{
  "family": "wordpress-fargate-task",
  "containerDefinitions": [
    {
      "name": "mariadb",
      "image": "491250998585.dkr.ecr.us-east-1.amazonaws.com/mariadb:latest",
      "cpu": 0,
      "portMappings": [
        {
          "name": "mariadb-3306-tcp",
          "containerPort": 3306,
          "hostPort": 3306,
          "protocol": "tcp"
        }
      ],
      "essential": false,
      "environment": [
        {
          "name": "MYSQL_DATABASE",
          "value": "wordpress"
        },
        {
          "name": "MYSQL_PASSWORD",
          "value": "wordpress"
        },
        {
          "name": "MYSQL_ROOT_PASSWORD",
          "value": "root"
        },
        {
          "name": "MYSQL_USER",
          "value": "wordpress"
        }
      ],
      "mountPoints": [],
      "volumesFrom": [],
      "systemControls": []
    },
    {
      "name": "wordpress",
      "image": "491250998585.dkr.ecr.us-east-1.amazonaws.com/wordpress:latest",
      "cpu": 0,
      "portMappings": [
        {
          "name": "wordpress-80-tcp",
          "containerPort": 80,
          "hostPort": 80,
          "protocol": "tcp",
          "appProtocol": "http"
        }
      ],
      "essential": true,
      "environment": [
        {
          "name": "WORDPRESS_DB_USER",
          "value": "wordpress"
        },
        {
          "name": "WORDPRESS_DB_HOST",
          "value": "localhost:3306"
        },
        {
          "name": "WORDPRESS_DB_PASSWORD",
          "value": "wordpress"
        },
        {
          "name": "WORDPRESS_DB_NAME",
          "value": "wordpress"
        }
      ],
      "mountPoints": [],
      "volumesFrom": [],
      "dependsOn": [
        {
          "containerName": "mariadb",
          "condition": "START"
        }
      ],
      "systemControls": []
    }
  ],
  "taskRoleArn": "arn:aws:iam::491250998585:role/LabRole",
  "executionRoleArn": "arn:aws:iam::491250998585:role/LabRole",
  "networkMode": "awsvpc",
  "volumes": [],
  "placementConstraints": [],
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "1024",
  "memory": "2048",
  "runtimePlatform": {
    "cpuArchitecture": "ARM64",
    "operatingSystemFamily": "LINUX"
  },
  "enableFaultInjection": false
}
```
