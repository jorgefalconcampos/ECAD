<h1 align="center">
  <a href="http://github.com"><img src="https://i.ibb.co/W5qWsf8/ECAD-psd.png" alt="ECAD logo" width="200"></a>
  <br>
  ECAD - Enseñanza Continua A Distancia
</h1>

<h4 align="center">Una plataforma online para continuar con el aprendizaje en cualquier lugar, a cualquier hora.</h4>

<hr>

<p align="center"> 
  <img src="https://img.shields.io/badge/ECAD v.-1.0.3-blue.svg" alt="versionECAD">
</p>

<p align="center">
  <a href="https://www.python.org/" target="_blank"><img src="https://img.shields.io/badge/python-3.8.3-F7CB3F.svg" alt="version"></a>
  <a href="https://www.djangoproject.com/" target="_blank"><img src="https://img.shields.io/badge/django-3.0.7-09541F.svg" alt="version"></a>
  <a href="https://www.nginx.com/" target="_blank"><img src="https://img.shields.io/badge/nginx-009639.svg" alt="nginx"></a>
  <a href="https://www.postgresql.org/" target="_blank"><img src="https://img.shields.io/badge/PostgreSQL-336690" alt="postgresql"></a>
  <a href="https://getbootstrap.com/" target="_blank"><img src="https://img.shields.io/badge/Bootstrap-purple.svg" alt="html5"></a>
  <a href="https://www.docker.com/" target="_blank"><img src="https://img.shields.io/badge/-docker-6CB5EE" alt="docker"></a>
  <a href="https://docs.docker.com/compose/"target="_blank"><img src="https://img.shields.io/badge/-docker%20compose-2391E6" alt="docker-compose"></a>
	
</p>
	
<p align="center">
  <a href="#qué-es-ECAD">¿Qué es ECAD?</a> •
  <a href="#beneficios">Beneficios</a> •
  <a href="#cómo-se-utiliza">Cómo se utiliza</a> •
  <a href="#créditos">Créditos</a> •
  <a href="#licencia">Licencia</a>
</p>

![screenshot](https://raw.githubusercontent.com/amitmerchant1990/electron-madownify/master/app/img/markdownify.gif)

## ¿Qué es **ECAD**?

ECAD es una plataforma online donde el conocimiento converge. Es un libro abierto donde se pueden consultar los apuntes publicados y mejorar competencias académicas, aprender algo nuevo, repasar temas o simplemente realizar preguntas.
Entre otras, las características que posee ECAD, son:

* Publicación de apuntes (también llamados artículos, posts, publicaciones, etc) por parte del profesor, los cuales pueden ser consultados por los interesadados en cualquier momento
* Organización de posts por medio de etiquetas y categorías
* Posibilidad de agregar comentarios a los apuntes y puntuarlos con el objetivo de mejorar el contenido
* Responsividad, el contenido se ajusta al tamaño del dispositivo utilizado
* Sistema de administración completo: permite crear, editar y eliminar usuarios (profesores)
* El usuario puede crear tantas pulicaciones como desee, una vez aprobados podrán ser vistos por los lectores
* El usuario puede crear, editar, archivar o eliminar apuntes creados por él
* El autor de un apunte puede aprobar o rechazar comentarios hechos sobre sus publicaciones
* Integración de contacto con los autores para mejor retroalimentación
* Suscripción al boletín de noticias cuando se publique sobre temas relevantes
* Sistema de administración interno
* Soporte multilenguaje
* Optimización para SEO

## Beneficios

En estos tiempos de enseñanza y aprendizaje a distancia, puede ser díficil comunicar y recibir el conocimiento de manera oportuna y eficaz. Con eso en mente, se decidió desarrollar una plataforma online para que los apuntes, notas, mensajes, clases o incluso las reflexiones de los docentes se comuniquen abiertamente y sean accesibles. El aprendizaje nunca termina, y es por eso que se tomó la iniciativa de desarrollar ECAD.

Uno de los principales beneficios que tiene ECAD es la enseñanza a distancia como instrumento para el progreso de la sociedad. Este elemento, (la enseñanza a distancia) se incluye en el nombre del proyecto, además de la referencia al símbolo WiFi como representación de los datos y disponibilidad 24/7.

## Cómo se utiliza

Para ejecutar ECAD, solo es necesario ejecutar el contenedor Docker
en la máquina o servidor donde se instalará la paltaforma y asignarle una dirección IP. Para ejecutar localmente, también es necesario instalar [Docker](https://www.docker.com/) en el sistema y proceder como se indica en los manuales técnicos y de instalación. Se necesitarán, al menos, [Python](https://www.python.org/downloads/) y [Django](https://www.djangoproject.com/) en las versiones indicadas, cuyas imagenes de instalación se encuentran en el archivo docker-compose-x, donde **x** es la versión de desarrollo o de producción. 

Para la versión de desarrollo, se recomienda instalar en el equipo utilizado para desarrollar; al menos Python y Django, además de Docker.

Para más información sobre las versiones de producción y desarrollo, favor de leer los manuales.


Para ejecutar desde la consola (con docker-compose y en modo desarrollo) ejecutar los siguiente comandos:

```bash
# Paso 1 - Crear el contenedor Docker, montarlo y correrlo en segundo plano
$ docker-compose up -d --build

# Paso 2 - Verificar la creación de la BDD Postgres dentro del servicio "db"
$ docker-compose exec db psql --username=USUARIO_DE_DESARROLLO --dbname=NOMBRE_BDD_DESARROLLO

# (Ejecutar este paso solo si los archivos estáticos [CSS, JS, PNG's, JPG's, etc] han cambiado)
$ docker-compose exec web python manage.py collectstatic --no-input --clear

# Paso 3 - Ejecutar la creación del superusuario dentro del servicio "web"
$ docker-compose exec web python manage.py createsuperuser
```

## Créditos

Este proyecto se hizo posible gracias a la utilización de los siguientes softwares, tecnologías y librerías:

- [Python](https://www.python.org/)
- [Django](https://www.djangoproject.com/)
- [PostgreSQL](https://www.postgresql.org/)
- [Docker](https://www.docker.com/)
- [NGINX](https://www.nginx.com/)
- [Gunicorn](https://gunicorn.org/)
- [Bootstrap](https://getbootstrap.com/)
- [jQuery](https://jquery.com/)
- HTML 5, AJAX, JavaScript




## Licencia
Este trabajo informático fue desarrollado para el [concurso institucional](https://www.ipn.mx/des/alumnos-egresados/concursos-academicos.html) "Premio al Mejor Software 2020" organizado por el Instituto Politécnico Nacional. Cualquier uso del código no autorizado previamente por parte del autor se reportará como indebido y aplicarán las sanciones correspondientes. En caso de que el proyecto resulte ganador, el repositoro pasará a ser privado y su uso, descarga, utilización y distribución quedará en manos del instituto.

---



