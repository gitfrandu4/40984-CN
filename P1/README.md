# Computación en la Nube. Práctica 1 - Despliegue de Instancias EC2

* Francisco Javier López-Dufour Morales

# Índice

- [Computación en la Nube. Práctica 1 - Despliegue de Instancias EC2](#computación-en-la-nube-práctica-1---despliegue-de-instancias-ec2)
- [Índice](#índice)
  - [1. Introducción](#1-introducción)
  - [2. Objetivos](#2-objetivos)
  - [3. Actividades](#3-actividades)
    - [3.1 Despliegue de Instancia SSH\_gate](#31-despliegue-de-instancia-ssh_gate)
    - [3.2 Despliegue de Servidor Web](#32-despliegue-de-servidor-web)
    - [3.3 Análisis de Costos de las Instancias EC2](#33-análisis-de-costos-de-las-instancias-ec2)
    - [3.4 Configuración de Alertas de Monitoreo](#34-configuración-de-alertas-de-monitoreo)
  - [4. Conclusiones](#4-conclusiones)
  - [5. Referencias](#5-referencias)

## 1. Introducción

Este informe detalla la realización de una práctica en el ámbito de la computación en la nube, específicamente utilizando los servicios de Amazon Web Services (AWS). La práctica se centra en el despliegue básico de instancias en la nube utilizando el servicio EC2 (Elastic Compute Cloud) de AWS.

## 2. Objetivos

El objetivo principal de esta práctica es proporcionar una primera toma de contacto con los servicios de AWS y aplicar los conocimientos teóricos adquiridos en clase. Específicamente, se busca:

- Desplegar y configurar instancias EC2 en AWS.
- Establecer conexiones SSH seguras entre instancias.
- Configurar un servidor web básico en una instancia EC2.
- Analizar los costos asociados con el despliegue de instancias en la nube.

## 3. Actividades

> El objetivo de esta practica es tener una primera toma de contacto con los servicios de AWS y aplicar los conocimientos obtenidos en la clase teórica. Para ello se utilizara el servicio EC2 para  preparar y desplegar instancias en la nube.

### 3.1 Despliegue de Instancia SSH_gate

Se desplegó una instancia en EC2 accesible por SSH desde el exterior, denominada SSH_gate. Las características principales de esta instancia son:

- AMI: `Amazon Linux 2023`
  - ID: `ami-0ebfd941bbafe70c6`
- Instance Type: `t2.micro`
  - Family: `t2`
  - vCPU: `1`
  - RAM: `1 GiB`
- Key Pair: `vockey`
- Storage:
  - Volume: `8 GiB`
  - Type: `gp3`
- Network:
  - VPC: `default`
  - Subnet: `default`
  - Public IP: `Auto-assign public IP`
- Security Group:
  - Name: `SSH_gate`
  - Description: `Security group for SSH_gate`
  - Inbound Rules:
    - Type: `SSH`
      - Port Range: `22`
      - Source: `0.0.0.0/0` (Anywhere)

El proceso de despliegue y conexión se realizó exitosamente, como se muestra en la siguiente imagen:

![EC2 Dashboard. Instancia desplegada.](img/ec2_instance_running.png)

Comprobamos que la instancia está en ejecución y nos conectamos a ella por SSH.

Nos hace falta:

- Un cliente SSH
- La clave privada: `vockey.pem` que se encuentra en el directorio `~/.ssh/`
  - En linux/macOS: `chmod 400 vockey.pem` para establecer los permisos adecuados.
- El usuario: `ec2-user`
- La dirección IP pública de la instancia: `ec2-54-87-55-252.compute-1.amazonaws.com`

Ejecutamos el siguiente comando para conectarnos a la instancia:

```bash
ssh -i "~/.ssh/vockey.pem" ec2-user@ec2-54-87-55-252.compute-1.amazonaws.com
```

La conexión se estableció correctamente y pudimos acceder a la instancia SSH_gate.

![SSH connection. Conexión a la instancia SSH_gate.](img/ssh_connection.png)

### 3.2 Despliegue de Servidor Web

Se desplegó una nueva instancia en EC2 que tiene un servidor web en la que muestra nuestro nombre y afición favorita. Esta máquina solo podrá ser accedida por SSH desde la máquina que desplegamos anteriormente SSH_gate.

**Desplegamos una  nueva instancia con las siguientes características:**

**Nombre y etiquetas**
![Nombre y etiquetas](img/name_and_labels.png)

**Imagen**
![AMI de Amazon Linux 2023](img/image.png)

**Tipo de instancia**
![Tipo de instancia. t2.micro](img/instance_type.png)

**Par de claves**
![Par de claves](img/key_pair.png) 

> **Nota:** Se creó una nueva clave en AWS para conectarnos a `MyWebServer` a través de `SSH_Gate` y la hemos seleccionado en "par de claves".

**Red y subred**

![Red y subred](img/red_and_subnet.png)
  - VPC: `default`
  - Subnet: `default`
  - Public IP: `Auto-assign public IP`
  
**Grupo de seguridad**

![Grupo de seguridad](img/security_group.png)

  - Security Group:
    - Name: `MyWebServerSG`
    - Description: `Security group for MyWebServer`
    - Inbound Rules:
      - Type: `SSH`
        - Port Range: `22`
        - Source: `172.31.39.183/32` (SSH_Gate)
      - Type: `HTTP`
        - Port Range: `80`
        - Source: `0.0.0.0/0` (Anywhere)
      - Type: `HTTPS`
        - Port Range: `443`
        - Source: `0.0.0.0/0` (Anywhere)

> **Nota:** Configuramos el Grupo de Seguridad `WebServerSG` para que también permita el tráfico `https`, aunque ahora mismo no sería necesario.

**Almacenamiento**

![Almacenamiento](img/add_storage.png)

    - Volume: `8 GiB`
    - Type: `gp3`

**Lanzamos la instancia y esperamos a que esté disponible**:

![Instance running](img/instance_running.png)

**Accedemos a la instancia por SSH**:

```bash
ssh -i "~/.ssh/vockey.pem" ec2-user@ec2-54-87-55-252.compute-1.amazonaws.com
```

**Configuramos la clave privada de la nueva instancia**

```bash
chmod 400 "~/.ssh/SSH_Gate.pem"
```

**Desde la instancia `SSH_gate` nos conectamos por SSH a la nueva instancia `MyWebServer_P1`**

```bash
[ec2-user@ip-172-31-39-183 .ssh]$ ssh -i "~/.ssh/SSH_Gate.pem" ec2-user@ec2-18-206-188-39.compute-1.amazonaws.com
   ,     #_
   ~\_  ####_        Amazon Linux 2023
  ~~  \_#####\
  ~~     \###|
  ~~       \#/ ___   https://aws.amazon.com/linux/amazon-linux-2023
   ~~       V~' '->
    ~~~         /
      ~~._.   _/
         _/ _/
       _/m/'
[ec2-user@ip-172-31-38-62 ~]$ 
```

**Ejecutamos el script de configuración del servidor web**

```bash
chmod +x setup-web-server.sh 
./setup-web-server.sh 
```

**Comprobamos que el servidor web está funcionando**

* IP pública de la instancia: `18.206.188.39`

```bash
(base) franciscoj ~ % curl http://18.206.188.39:80
```

![Servidor web funcionando](img/web_server.png)
 
### 3.3 Análisis de Costos de las Instancias EC2

![Costos](img/costs.png)

**Resumen de la Estimación**

- Instancia EC2: SSH_gate
  - Costo inicial: 0,00 USD
  - Costo mensual: 2,99 USD
- Instancia EC2: MyWebServer
  - Costo inicial: 0,00 USD
  - Costo mensual: 2,99 USD

El costo mensual total para mantener ambas instancias EC2 es de 5,98 USD, lo que se traduce en un costo anual de 71,76 USD. 

### 3.4 Configuración de Alertas de Monitoreo

1. Navegamos a la consola de `CloudWatch` en AWS.
2. Seleccionamos "Alarms" en el menú de navegación.
3. Hacemos clic en "Create Alarm".
4. Seleccionamos la métrica que queremos monitorear (por ejemplo, `EstimatedCharges`).
5. Configuramos los detalles de la alerta, incluyendo el umbral y la frecuencia de evaluación.
6. Seleccionamos la acción que queremos que se realice cuando se active la alerta (por ejemplo, enviar un correo electrónico al correo institucional).
7. Hacemos clic en "Create Alarm".

![CloudWatch Overview](img/cloudwatch_overview.png)
![Alerta de monitoreo](img/alarm.png)
![Alerta de monitoreo (detalles)](img/alarm_details.png)

## 4. Conclusiones

En conclusión, esta práctica nos ha proporcionado una visión general de los servicios de AWS, centrándonos específicamente en el servicio EC2. Hemos aprendido a desplegar y configurar instancias, establecer conexiones SSH, configurar un servidor web básico y analizar los costos asociados.

## 5. Referencias

- [AWS EC2](https://aws.amazon.com/ec2/)
- [AWS EC2 User Guide](https://docs.aws.amazon.com/ec2/index.html)
