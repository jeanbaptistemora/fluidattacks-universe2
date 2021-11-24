---
slug: secdevops-security-champions-spa/
title: Hallando Security Champions
date: 2020-05-21
subtitle: Seis recomendaciones para SecDevOps de Carnegie Mellon
category: philosophy
tags: security, devops, software, information, web, cloud
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1620331091/blog/secdevops-security-champions/cover_nkri6h.webp
alt: Photo by Ingo Stiller on Unsplash
description: Aquí aprenderás sobre los Security Champions. Pero antes,
  te damos cinco recomendaciones si estás pensando en implementar
  la seguridad en tu empresa.
keywords: Seguridad, Security Champions, Devops, Secdevops, Software,
  Información, Ethical Hacking, Pentesting
author: Felipe Ruiz
writer: fruiz
spanish: yes
name: Felipe Ruiz
about1: Cybersecurity Editor
source: https://unsplash.com/photos/3tkxfe2GocY
---

Recientemente asistí a un webcast de la Universidad Carnegie Mellon
titulado "[At What Point Does DevSecOps Become Too Risky for the
Business?](https://www.youtube.com/watch?v=n0FRNpoqYT0&feature=youtu.be)"
(No estoy seguro de que fuera el título apropiado, pero no pretendo
criticarlo). Este webcast fue presentado por Hasan Yasar, Director
Técnico del Instituto de Ingeniería de Software de Carnegie Mellon, y
Altaz Valani, Director de Investigación de Security Compass. Cuando lo
vi, encontré algunas similitudes con la información que compartí en [un
post sobre DevSecOps/SecDevOps](../devsecops-concept/). Sin embargo,
estos autores hablaron en un sentido más amplio, considerando los
riesgos de negocio de las empresas que ofrecen software. Quiero
recapitular algunas de sus ideas, agrupadas aquí en cinco
recomendaciones generales, y ampliar un poco otra (una sexta
recomendación): los Security Champions. Esta última sección se apoya en
un documento de SAFECode.org titulado "[Software Security Takes a
Champion](http://safecode.org/wp-content/uploads/2019/02/Security-Champions-2019-.pdf),"
en el que también participó Altaz Valani.

## Recomendaciones generales

### 1. Introduce la seguridad en tus procesos lo antes posible

Muchas empresas reflejan una urgencia por el rápido despliegue de nuevas
características en sus aplicaciones sin tener en cuenta la seguridad.
¿Están omitiendo la seguridad del software porque se supone como un
obstáculo? Y en un contexto más amplio, ¿qué pasa con la seguridad
empresarial? ¿Se está ignorando la gestión del riesgo empresarial?
Dentro de la cultura SecDevOps, se espera que tanto la velocidad como la
seguridad sean incluidas desde un principio. Por tanto, no empieces a
construir y desplegar aplicaciones de forma continua desde tu compañía
si no has identificado cuáles son los riesgos empresariales y cómo se
pueden evitar.

### 2. Establece requisitos de seguridad desde el principio

Las compañías pueden gestionar el riesgo desde diferentes perspectivas.
Por ejemplo, la "perspectiva de la ciber-resiliencia" y la "perspectiva
del cumplimiento". En la primera, teniendo en cuenta los posibles
impactos, producto de vulnerabilidades explotadas, la principal
preocupación es encontrar soluciones rápidas a esos problemas en cada
ocasión. En la segunda, normalmente desde un entorno altamente regulado,
se piensa más en la evaluación del cumplimiento de las normas. Se
recomienda trabajar desde esta perspectiva de cumplimiento y establecer
desde el principio requisitos basados en normas de seguridad públicas
como [GDPR](../../compliance/gdpr/), [HIPAA](../../compliance/hipaa/) y
[PCI DSS](../../compliance/pci/) (véase nuestra recopilación denominada
[**Criteria**](https://docs.fluidattacks.com/criteria/)). Estos
requisitos deben ajustarse a la estructura y funcionalidad del software
desarrollado en tu empresa. Además, algunos deben significar la
traducción de los riesgos de tu negocio al lenguaje técnico.

### 3. Mantén los requisitos de seguridad como obligatorios

En efecto, los requisitos de seguridad pueden estar en constante
remodelación. Pero ten en cuenta que si defines unos requisitos a
cumplir en tu compañía, los cuales pueden ser reevaluados, la idea es
que sean obligatorios. Si en algún momento no se cumplen, entonces hay
que detener cualquier flujo de trabajo previo al despliegue del
software. Luego, deberías plantear preguntas como: ¿El desarrollador no
ha entendido algo? ¿Necesita formación? ¿Es esto un falso positivo de la
herramienta de evaluación? ¿Es una herramienta adecuada? Además,
asegúrate de que los informes de incumplimiento lleguen a cada público
interesado en un lenguaje adecuado para su comprensión.

### 4. Usa las herramientas adecuadas para tu negocio

Mantener infraestructuras y productos seguros es un reto, especialmente
cuando hay cambios constantes en su arquitectura. Por lo tanto, las
pruebas de seguridad también deberían ser continuas. La automatización
en procesos como SAST y DAST dependerá de algunas herramientas; debes
ser bastante cuidadoso respecto a ellas. No se trata de adquirirlas
porque son ofrecidas como novedosas, o porque la competencia utiliza
esta o aquella, o porque se supone serán útiles en tus pruebas de
seguridad. "¿Qué herramientas son esenciales para nuestro negocio?" Esta
es una pregunta que puedes responder con la ayuda de tus desarrolladores
con experiencia en seguridad (¿Security Champions?).

### 5. Mira la seguridad desde las perspectivas técnica y de negocios

Algo muy recomendable en enfoques como SecDevOps es la integración de
grupos. Con la seguridad ya en marcha, además de un 'enfoque técnico'
desde la ingeniería de software, esta debería contar con un 'enfoque de
negocio' desde la gestión de riesgos empresariales. Por lo tanto, se
recomienda incluir al grupo de negocio en SecDevOps con su punto de
vista de la seguridad. Con esto, se espera que la mentalidad de muchos
cambie hacia el marco en el que la seguridad es vista como indispensable
para el mantenimiento de la producción y la generación de ingresos. Es
importante destacar que la información que se transfiere entre grupos
debe ser clara y completa. Por un lado, los desarrolladores de la
empresa deben comprender si su trabajo está contribuyendo o no a la
gestión de los riesgos empresariales. Por otro lado, los responsables de
la seguridad de tu compañía deben entender lo que el equipo técnico les
está comunicando (e.g., retos, problemas, necesidades).

## Security Champions —sexta recomendación

<div class="imgblock">

![Campeones de Seguridad](https://res.cloudinary.com/fluid-attacks/image/upload/v1620331090/blog/secdevops-security-champions/lions_lqcl1b.webp)

<div class="title">

Figure 1. [Fotografía](https://unsplash.com/photos/1pdp-PGplss) por [A P en
Unsplash](https://unsplash.com/@windogram)

</div>

</div>

La integración de los equipos puede verse favorecida por la presencia de
'champions' de cada área. En la inclusión de la seguridad en la
ingeniería de software para empresas, contar con uno o varios 'Security
Champions' (SC) puede ser bastante útil.

### ¿Qué es un Security Champion y qué hace?

En resumen, el SC es un desarrollador de software que posee y aplica
amplios conocimientos de seguridad dentro de un equipo de desarrollo. El
SC es responsable de identificar y resolver los problemas de seguridad
en una fase temprana del SDLC para no ralentizar los procesos. El SC
ayuda a verificar que los requisitos de seguridad sean cumplidos durante
el proceso de desarrollo. Además, traduce la información técnica del
grupo de DevOps a los grupos de seguridad y de gestión empresarial, y
viceversa. Por lo tanto, el SC interactúa estrechamente con estos
grupos, se lleva bien con los expertos de cada lado y tiende un puente
entre ellos.

El SC puede priorizar los problemas de seguridad en función de los
riesgos de la compañía, sobre los cuales tiene un conocimiento completo.
También ayuda a seleccionar y a utilizar las herramientas de evaluación
y a interpretar los resultados. Como producto de la educación en las
universidades, suele haber pocos ingenieros de software formados en
seguridad con amplios conocimientos de "[las necesidades de seguridad (y
normativas) tanto internas como de los
clientes](http://safecode.org/wp-content/uploads/2019/02/Security-Champions-2019-.pdf)".
Con la ayuda del SC, se puede establecer en una compañía un apoyo
formal, contextualizado y bien definido para el entrenamiento en
seguridad de los desarrolladores y otros miembros del personal. El SC
puede llevar a cabo actividades con los desarrolladores para expandir
sus conocimientos y motivarlos a que se conviertan en expertos en
seguridad. Adicionalmente, el SC puede ayudar a garantizar que los
miembros del equipo de seguridad de una compañía dejen de ser vistos
como 'policías malos' y que los desarrolladores no los tomen como
adversarios a evitar.

### ¿Qué conocimientos debe poseer el SC?

En primer lugar, el SC debe ser una persona con conocimientos de
ingeniería de software. Especialmente sobre herramientas y métodos para
el desarrollo y despliegue de software seguro. Esta persona debe saber
sobre identificación y mitigación de amenazas, análisis de riesgos y
análisis de rutas de ataque. Además, esta persona debería conocer la
multiplicidad de vulnerabilidades existentes, las listas que las agrupan
y cómo se clasifican. El SC debería tener habilidades de discusión y
presentación de la información. Y, por último, debería ser capaz de
resolver conflictos, motivar a la gente y ser amable y atento con los
demás.

Las compañías que desarrollan y ofrecen software como producto o
servicio pueden emplear diferentes estrategias para formar parte de una
cultura en la que la seguridad juega un papel esencial. Una cosa es que
estas empresas dispongan de herramientas y servicios pagos para su
protección. Otra cosa es, sin duda, que cuenten en su plantilla con
desarrolladores que, sin estar obligados, quieran adquirir y aplicar
conocimientos de seguridad. Entre ellos, posiblemente, surgirán los
Security Champions, que sin duda les traerán importantes beneficios.

Entonces, ¿ya ha descubierto al menos un SC entre los miembros de su
equipo?
