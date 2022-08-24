---
id: api-token
title: Accessing ARM via API
sidebar_label: Accessing ARM via API
slug: /machine/api
---

The ARM app allows users
to make requests directly
to our GraphQL API.
You can do this
by using one of the following methods:

## Using the GraphQL playground

1. Log in to https://app.fluidattacks.com
1. Open https://app.fluidattacks.com/api
1. Open the Settings using the upper-right button

  ![Browser Api Settings](https://res.cloudinary.com/fluid-attacks/image/upload/v1622211883/docs/api/api-token/api_highlight_settings_byubm9.webp)

1. Set a new value:
  `"request.credentials": "include"`
  and save the settings

  ![Setting Request Credentials](https://res.cloudinary.com/fluid-attacks/image/upload/v1622211884/docs/api/api-token/api_highlight_reqcreds_sgljuh.webp)

1. Go to a new tab
  and make your queries

  ![Query Example](https://res.cloudinary.com/fluid-attacks/image/upload/v1622211880/docs/api/api-token/query_example_pcw8ra.webp)

**Note**: This method uses the same session
as the web application,
which lasts for 40 minutes.
After that,
you need to log in to https://app.fluidattacks.com again
and refresh the https://app.fluidattacks.com/api page.
If you want your session
to last more than 40 minutes,
you can use an API Token
as shown below.

## Using the ARM API Token

1. Log in to https://app.fluidattacks.com

1. Generate the API Token
   from the web application
   using the `API` option
   in the left panel:
   ![ARM API Button](https://res.cloudinary.com/fluid-attacks/image/upload/v1622211890/docs/api/api-token/app_highlight_apibutton_ayw1r8.webp)

1. Select an expiration date
  up to six months after
  the creation date:

  ![API Token Modal](https://res.cloudinary.com/fluid-attacks/image/upload/v1622211880/docs/api/api-token/api_token_modal_uqt5k9.webp)

1. After clicking the “Proceed” button,
  you will see a string labeled “Access Token”.
  This will be your API Token:

  ![Generated API Token in App](https://res.cloudinary.com/fluid-attacks/image/upload/v1622211884/docs/api/api-token/app_apitoken_generated_zhrspd.webp)

1. Store this token safely,
  as it is the only time you will see it.
  With it,
  you can do the same things
  that you usually do
  on the Integrates web application.

You can also generate the API Token
using the next GraphQL mutation on
https://app.fluidattacks.com/api,
where `expirationTime` is a `Unix Timestamp`

```graphql
mutation {
  updateAccessToken(expirationTime:1577854799) {
    sessionJwt
  }
}
```

You will get the API Token
under the `sessionJwt` value:

![Generated API Token in Browser](https://res.cloudinary.com/fluid-attacks/image/upload/v1622211883/docs/api/api-token/browser_apitoken_generated_kbkphs.webp)

Add a new Header in `HTTP HEADERS`
with the name `Authorization`
and the value `Bearer <api-token>`,
where `<api-token>` is the token generated
in the previous steps:

![Set Authorization Example](https://res.cloudinary.com/fluid-attacks/image/upload/v1622211885/docs/api/api-token/apitoken_setheader_ehr86e.webp)

Done!
Now you can make queries
with the same API Token
for up to six months
(depending on the `expirationTime` you set earlier)
