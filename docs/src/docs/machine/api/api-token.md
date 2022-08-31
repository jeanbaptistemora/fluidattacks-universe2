---
id: api-token
title: Accessing ARM via API
sidebar_label: Accessing ARM via API
slug: /machine/api
---

The ARM allows users to make
requests to its **GraphQL API**.
To get started,
it is recommended to get some
basic knowledge of this query language.

## What is GraphQL?

[GraphQL](https://graphql.org/) is a
query language for APIs,
with a single endpoint which
is `https://app.fluidattacks.com/api`
where you can perform requests with
**Queries** to fetch data and
**Mutations** to create,
delete,
and modify the data you need.
Having this clear,
it is necessary to have basic
knowledge of this language;
if you are new to GraphQL,
we invite you to read more
[here](/machine/api/basics-api).

After learning the basics,
let’s find out how we can **authenticate**
ourselves and start exploring the **GraphQL API**.

## Autentication

There are two ways you can authenticate
and start using the API:
from the **GraphQL playground**
or by **HTTP** requests in **code**.

We will now explain the GraphQL
playground authentication,
which allows two ways.

### Authentication with the ARM login

Here the authentication is done
through the ARM platform login,
these are the following steps:

1. Log in to https://app.fluidattacks.com
1. Open https://app.fluidattacks.com/api
1. Open the Settings using the upper-right button.

  ![Settings](https://res.cloudinary.com/fluid-attacks/image/upload/v1661897870/docs/api/api-token/armlogin_settings.png)

1. Here you open the
  playground settings,
  and you have to change the
  item called "request.credentials"
  which comes with the word "omit"
  you have to change it to the word
  "include" followed by
  clicking save settings.

  ![Request Credentials](https://res.cloudinary.com/fluid-attacks/image/upload/v1661898294/docs/api/api-token/armlogin_requestcredentials.png)

1. Once you save the changes,
  you can write the queries you need,
  and then click the “play” button
  to get the answer to your request.

  ![Play Button](https://res.cloudinary.com/fluid-attacks/image/upload/v1661898294/docs/api/api-token/token_play_button.png)

> **Note:** This method uses the same session
> as the web application,
> which lasts for 40 minutes.
> After that,
> you need to log in to https://app.fluidattacks.com again and
> refresh the https://app.fluidattacks.com/api page.
> If you want your session to last more than 40 minutes,
> you can use an API Token as shown below.

### Authentication with the ARM API Token

In this authentication process,
it is required to generate
the ARM API Token.
The steps are explained below.

1. Log in to https://app.fluidattacks.com
1. Generate the API Token from
  the web application by going
  to the User information drop-down menu,
  by clicking on the option that says API.

  ![Generate API Token](https://res.cloudinary.com/fluid-attacks/image/upload/v1661898294/docs/api/api-token/token_api.png)

1. Select an expiration date
  up to six months after the creation date:

  ![Expiration Date](https://res.cloudinary.com/fluid-attacks/image/upload/v1661898294/docs/api/api-token/token_expiration.png)

1. After clicking the “Confirm” button,
  you will see a string labeled “Access Token”.
  This will be your API Token:

  ![Confirm Date](https://res.cloudinary.com/fluid-attacks/image/upload/v1661898294/docs/api/api-token/token_confirm.png)

1. Store this token safely,
  as it is the only time
  you will see it.
  With it,
  you can do the same things
  that you usually do on the
  web application.
1. Now,
  enter the playground by browsing
  to https://app.fluidattacks.com/api
1. Here,
  go to the bottom of the page
  and click on HTTP HEADERS

  ![Headers](https://res.cloudinary.com/fluid-attacks/image/upload/v1661898294/docs/api/api-token/token_http_header.png)

1. Type `{"authorization":"Bearer API Token"}`

  ![Type](https://res.cloudinary.com/fluid-attacks/image/upload/v1661898294/docs/api/api-token/token_type.png)

1. Then you put the query of
  the request you want to make,
  click the “play” button to see
  the answer to that request.

  ![Play Button](https://res.cloudinary.com/fluid-attacks/image/upload/v1661898294/docs/api/api-token/token_play_button.png)
