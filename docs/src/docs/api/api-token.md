---
id: api-token
title: Accessing ASM via API
sidebar_label: Accessing ASM via API
slug: /api
---

The ASM app allows users to make requests directly to our GraphQL API.
You can do this by using one of the following methods:

### Using the GraphQL playground

1. Log in to https://app.fluidattacks.com
2. Open https://app.fluidattacks.com/api
3. Open the Settings using the upper-right button

![Browser Api Settings](/img/api/api-token/api_highlight_settings.png)

4. Set a new value: `"request.credentials": "include"` and save the settings

![Setting Request Credentials](/img/api/api-token/api_highlight_reqcreds.png)

5. Go to a new tab and make your queries

![Query Example](/img/api/api-token/query_example.png)

**Note**: This method uses the same session as the web application, which lasts for 40
minutes. After that, you need to log in to https://app.fluidattacks.com again
and refresh the https://app.fluidattacks.com/api page.
If you want your session to last more than 40 minutes, you can use an API Token as
shown below.

### Using the ASM API Token

1. Log in to https://app.fluidattacks.com

2. Generate the API Token from the web application using the `API` option in the
left panel:

![ASM API Button](/img/api/api-token/app_highlight_apibutton.png)

3. Select an expiration date up to six months after the creation date:

![API Token Modal](/img/api/api-token/api_token_modal.png)

4. After clicking the “Proceed” button, you will see a string labeled “Access Token”.
This will be your API Token:

![Generated API Token in App](/img/api/api-token/app_apitoken_generated.png)

5. Store this token safely, as it is the only time you will see it. With it, you can
do the same things that you usually do on the Integrates web application.

You can also generate the API Token using the next GraphQL mutation on
https://app.fluidattacks.com/api, where `expirationTime` is a `Unix Timestamp`

```
mutation {
  updateAccessToken(expirationTime:1577854799) {
    sessionJwt
  }
}
```

You will get the API Token under the `sessionJwt` value:

![Generated API Token in Browser](/img/api/api-token/browser_apitoken_generated.png)

Add a new Header in `HTTP HEADERS` with the name `Authorization` and the value
`Bearer <api-token>`, where `<api-token>` is the token generated in the previous steps:

![Set Authorization Example](/img/api/api-token/apitoken_setheader.png)

Done! Now you can make queries with the same API Token for up to six months
(depending on the `expirationTime` you set earlier)
