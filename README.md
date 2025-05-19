# 🗃🗂 Proyecto Bases de Datos
* Dairo Javier Rodriguez - 1151358
* Jonathan Guevara - 1152229
* David Torres - 1151717

## 📚 Sistema de Biblioteca
Se anexa archivo del [BACKUP](https://github.com/PocketDx/Proyecto_BD_2025_1/blob/main/BACKUP.sql) de MySQL de la base de datos.

### ⚙ Requisitos

* [XAMPP 8.2.12](https://www.apachefriends.org/es/index.html)
* [Python 3.13.3](https://www.python.org/downloads/)
* [Faker 37.3](https://pypi.org/project/Faker/)

    ```
    pip install Faker
    ```

## 🧩 Script - DML
Para cumplir con el requisito de DML se crea un [Script](https://github.com/PocketDx/Proyecto_BD_2025_1/blob/main/poblar_datos.py), el cual hace uso de la libreria "Faker" y "Random" para el minado de datos. Asi se consiguen los mas de 3000 registros solicitados.


## 📋 DDL
Se anexa un [Script SQL](https://github.com/PocketDx/Proyecto_BD_2025_1/blob/main/Modelo_Relacional_Biblioteca.sql) que cumpla con las 20 tablas solicitadas para el proyecto.


## 🛠Tablas
Se anexan las [tablas](https://github.com/PocketDx/Proyecto_BD_2025_1/tree/main/Tablas_CSV) en formato CSV separados por ***;***
Se debe tener en cuenta configurar correctamente la importación en _phpMyAdmin_ usando ***;***


### 🖥 Screenshots

##### Tabla Usuario llenada con 3000 usuarios
[![base.jpg](https://i.postimg.cc/BbPJWwwL/base.jpg)](https://postimg.cc/4HGDVwGs)

##### Tabla copia inyectada con 3782 copias de libros
[![basecopi.jpg](https://i.postimg.cc/3RVdDGsG/basecopi.jpg)](https://postimg.cc/xJG0wXTj)

##### Tabla libro minada con 500 libros
[![baseli.jpg](https://i.postimg.cc/SR9jLs4v/baseli.jpg)](https://postimg.cc/5Qxxbf6B)
