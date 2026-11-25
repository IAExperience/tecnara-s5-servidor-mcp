# Spec: web de Cierzo Labs

Datos inventados para probar el RAG. Cierzo Labs es una startup ficticia de Zaragoza que hace webs para comercios de barrio.

## Objetivo

Que un comercio entienda en diez segundos qué hacemos y nos escriba.

## Requisitos funcionales

- FR-001: la portada dice qué hacemos en una frase y enseña tres proyectos.
- FR-002: cada persona del equipo tiene su ficha con foto, rol y una bio de tres líneas.
- FR-003: el formulario de contacto no envía correos: abre el cliente de correo del visitante con el asunto ya escrito.
- FR-004: la web se ve bien en un móvil de 360 px de ancho.

## Fuera de alcance

- No hay tienda online ni pagos.
- No hay blog en esta versión.

## Decisiones

- Sin frameworks: HTML, CSS y JavaScript, para que cualquiera del equipo pueda tocarla.
- El formulario abre el correo (mailto) porque no tenemos servidor donde guardar mensajes.
