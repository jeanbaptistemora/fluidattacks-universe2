---
slug: oss-seguridad/
title: ¿Seguros por estar en una cueva?
date: 2020-11-05
subtitle: Seguridad del OSS — Fluid Attacks como claro ejemplo
category: philosophy
tags: security, cybersecurity, code, software, company, business
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1620330967/blog/oss-seguridad/cover_mpada0.webp
alt: Photo by Karsten Winegeart on Unsplash
description: Queremos recordarte que ocultar el código fuente de tus apps
  a menudo puede proporcionarte una ilusión de seguridad
  y que el OSS es una valiosa alternativa.
keywords: Ciberseguridad, OSS, Open Source, Código Abierto, Software,
  Compañía, Ethical Hacking, Pentesting
author: Felipe Ruiz
writer: fruiz
spanish: yes
name: Felipe Ruiz
about1: Cybersecurity Editor
source: https://unsplash.com/photos/2HlidfG6ihs
---

En dos posts que publiqué anteriormente, ya había mencionado el software
de código abierto
([**OSS**](https://en.wikipedia.org/wiki/Open-source_software), por sus
siglas en inglés). [En el primero](../vulns-triage-synopsys/), recuerdo
haber citado a Dale Gardner, refiriéndose al creciente uso del **OSS**
por parte de los equipos de desarrollo encargados de construir
aplicaciones. [En el segundo](../look-inside-oss/), que puede servir de
introducción al post que estás leyendo ahora, abordé algunas
generalidades sobre el **OSS**, su diferenciación del [software
propietario](https://es.wikipedia.org/wiki/Software_propietario) y
algunos de sus beneficios como estrategia empresarial. Para este post,
hemos decidido dar más espacio a la seguridad del **OSS** y presentar
brevemente nuestra experiencia en `Fluid Attacks`.

Hace unos dos meses,
[Nivel4](https://blog.nivel4.com/noticias/filtracion-revela-el-codigo-fuente-de-tres-bancos-en-mexico/)
informó que se habían filtrado los códigos fuente de las aplicaciones
móviles de tres bancos mexicanos y se habían revelado en la web.
Algunas personas en las redes comentaron que la causa de la filtración
fue una mala configuración, y los bancos inmediatamente reportaron que
no había ningún impacto en la seguridad de los sistemas y en los datos
sensibles de los clientes. ¿Era eso cierto? Creo que muchísima gente
comenzó a sospechar de esa seguridad en aquel momento. Por cierto, si no
había nada que perder mostrando los códigos fuente, ¿por qué los
ocultaban? Sin duda, estos bancos perdieron la confianza de muchos de
sus usuarios y vieron afectada su reputación entre los competidores.

Las aplicaciones de los tres bancos se convirtieron inadvertidamente en
**OSS**. Podríamos decir que sus propietarios pretendían mantener una
imagen de seguridad al no hacer público el código. Sin embargo, oculto o
abierto, la seguridad del código dependerá es de lo sólida y cualificada
que haya sido su elaboración. Se pueden encontrar vulnerabilidades o
fallas tanto en el software abierto como en el propietario, pero como
compartió [Bruce
Byfield](https://www.datamation.com/open-source/nine-reasons-for-using-open-source-software.html)
hace unos años, "los vendedores de software propietario son famosos por
la seguridad mediante oscuridad". Ellos suelen creer erróneamente que
mantener sus sistemas en las oscuras cuevas los hará más seguros. Por
eso, en muchos casos, realizan pocas evaluaciones de seguridad y aplican
parches a las vulnerabilidades con relativa lentitud.

Uno de los beneficios empresariales del **OSS** más mencionados es, en
contra de la intuición de mucha gente, la seguridad. Cuando hablamos de
un proyecto de **OSS** ampliamente reconocido en la web, podemos decir
que son muchos los ojos que lo escrutan y muchas las manos que lo
prueban con regularidad. En consecuencia, las posibilidades de pasar por
alto los riesgos de ciberseguridad son mucho menores que cuando el
proyecto es privado. Una gran comunidad con una amplia variedad de
miembros puede detectar y corregir fallas y vulnerabilidades en el
código mucho más rápido que un pequeño grupo de desarrolladores
pertenecientes a una sola empresa.

No obstante, debo señalar que muchas empresas mantienen sus códigos en
secreto, algunos de ellos al mismo tiempo bastante bien asegurados, por
ninguna otra razón que la de preservar como propias las ideas que las
hacen únicas frente a sus competidores. Eso es comprensible. Sin
embargo, algunos ocultan solo sus partes 'esenciales' de código y
exponen el resto en la web para beneficiarse del trabajo en comunidades
abiertas. Eso es lo que, según [Yevgeniy
Brikman](https://www.ycombinator.com/library/56-why-the-best-companies-and-developers-give-away-almost-everything-they-do),
por ejemplo, hace Google con su "principal diferenciador\[:\] su
arquitectura de búsqueda". Mientras tanto, muchas compañías que
comparten TODO el código al público en general, generando confianza por
la seguridad que proporcionan, pueden [recibir ingresos por otros
medios](https://www.sciencedirect.com/science/article/abs/pii/S026840121100123X?via%3Dihub),
incluso [ofreciendo servicios](https://lwn.net/Articles/786068/)
relacionados con su **OSS**. Ellas tienen su ["salsa
secreta"](https://www.ycombinator.com/library/56-why-the-best-companies-and-developers-give-away-almost-everything-they-do)
ubicada en otra parte, y aquí es donde entra `Fluid Attacks`.

## Fluid Attacks está a salvo fuera de la cueva

<div class="imgblock">

![Karsten](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330967/blog/oss-seguridad/karsten_jryt90.webp)

<div class="title">

Figure 1. Fotografía por [Karsten Winegeart](https://unsplash.com/@karsten116)
en [Unsplash](https://unsplash.com/photos/v_OICS4SdEA)

</div>

</div>

`Fluid Attacks` nació directamente en el software libre y de código
abierto, haciendo uso de él y manteniéndolo en esa condición. Como dijo
[Mauricio Gomez](https://www.linkedin.com/in/mgomezarango/en-us),
cofundador de la empresa, ellos comenzaron a trabajar directamente en
Linux y se encargaron de la creación de redes, basadas en **OSS**, antes
de convertirse en un Red Team en 2008, el cual no ha dejado de compartir
su código. Un código que no está adherido exclusivamente a un par de
mentes privilegiadas de las que siempre dependerá su existencia y
funcionamiento. Cada vez que alguien abandone `Fluid Attacks`, otra
persona con habilidades y experiencia similares podrá relevarle, porque
la materia prima con la que trabajamos no pretendemos dejar de
compartirla.

Aparte de la colaboración que podemos recibir de personas inteligentes
de [nuestra comunidad](https://docs.fluidattacks.com/) y no afiliadas
legalmente a nuestra empresa, casi todos los miembros de `Fluid Attacks`
pueden y son animados a revisar el código para proponer nuevas ideas
para su optimización (incluyendo la seguridad). Desde los inicios de
`Fluid Attacks` hemos aprovechado el **OSS** como organización, y nos
hemos comprometido, con carácter recíproco, a generar nuestra
contribución a la comunidad de ciberseguridad en general.

Podría entonces alguien preguntarnos, ¿no están ustedes regalando un
trabajo que tanto les ha costado? ¿No están sus competidores observando
con detalle, incluso copiando, lo que ustedes utilizan para atender a
sus clientes? ¿Mantener un **OSS** no podría significar entregar el
material necesario a otros grupos de individuos para establecer nuevas
empresas y más competencia para ustedes? Y, tal vez aún más importante,
**¿no son ustedes muy vulnerables a los ataques de hackers
malintencionados al exponer su código?**

En respuesta a estas preguntas, podemos decir que lo que hemos
construido hasta ahora también ha sido en parte gracias a muchas
personas de todo el mundo que han mantenido el movimiento **OSS**.
También podemos decir que nos sentimos cómodos haciendo público el
conocimiento, ganando experiencia y reduciendo la duplicación de
esfuerzos. Adicionalmente, nos apoyamos en nuestro principal
diferenciador —que no está en el código— para distinguirnos de los
viejos y nuevos competidores. (Ellos no pueden depender de nosotros para
evolucionar). Como he dicho, nuestra forma de obtener beneficios no se
centra en ofrecer un código, sino servicios de inteligencia humana
utilizando ese código. Por último, **revelar nuestro código no nos hace
altamente vulnerables a los ataques**, siempre y cuando este cuente con
los controles de seguridad necesarios y sus vulnerabilidades se reduzcan
al mínimo.

Es imprescindible tener en cuenta que el código que mostramos
públicamente no es solo el mismo que utilizamos en las prestaciones de
seguridad para nuestros clientes. También es el código que sirve para
realizar los análisis de seguridad de nuestros sistemas y productos de
forma continua ([Continuous
Hacking](../../services/continuous-hacking/)). No estamos dando a la
comunidad un lote de líneas de código mediocres y a medio hacer. El
material que desarrollamos y actualizamos con fervor a un ritmo
acelerado es el material de nuestros analistas de seguridad en su día a
día. Al mismo tiempo, es el material que puede utilizar de forma fiable
cualquier persona en cualquier rincón del planeta para detectar
vulnerabilidades en sistemas informáticos.

En `Fluid Attacks`, entendemos que tener un código oculto no es
necesariamente mantenerlo seguro. Comprendemos que la seguridad depende
de la fuerza y la calidad del código, que preferiblemente debe ser
revisado por muchas personas y de forma continua. Por lo tanto, no
ocultamos el código. No hay ningún misterio detrás de lo que puede
hacer. Lo que mantenemos oculto y seguro son los datos sensibles de
nuestra empresa y de nuestros clientes, mediante complejos procesos de
encriptación, por ejemplo. Eso es lo que ayudamos a conseguir a muchas
empresas (descubriendo vulnerabilidades y promoviendo mejores prácticas
de desarrollo) y lo que te damos como recomendación a través de este
post.

Dentro o fuera de la cueva, tu seguridad dependerá de tu armadura, de
tus armas y tus habilidades. Nosotros podemos, y la comunidad también
puede, ayudarte a mejorar tu seguridad. Sal de la cueva voluntariamente
(no esperes a que te saquen como a aquellos bancos). Reflejarás
confianza, fuerza y transparencia ante tus seguidores, clientes o
interesados. Más adelante, incluso podrás generar y facilitar
aportaciones a la comunidad. Solo tienes que [ponerte en contacto con
nosotros](../../contact-us/).

P.D. ¡Echa un vistazo [aquí en Gitlab](https://gitlab.com/fluidattacks)
a nuestro código\!
