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

### Authentication of requests from code

Another way to perform authentication
is to generate scripts.
We will show you a small example
based on the Python programming language.

First,
we generate the script we want.
Keep in mind that we will always
use the POST method to request
any necessary action.
If you want to know
more about this method,
read more
[here](https://graphql.org/learn/serving-over-http/#post-request).

![Script](https://res.cloudinary.com/fluid-attacks/image/upload/v1661954582/docs/api/api-token/authentication_script.png)

When you run the script,
you will get what you requested
from the query in the terminal.
Please note that the token
generated in the API is
unique and confidential;
we recommend not sharing this token.

## Revoke token

When you want to revoke the API token,
it is either because the token you generated
has expired and you need a new one or
because you lost the token
(there is no way to see it after the first time)
and you need a new one.
To revoke,
you have to go to the API Token in the
[drop-down menu](/machine/web/user)
in the ARM,
and there you will get a pop-up window
where you are given the option to revoke the token.

![Revoke token](https://res.cloudinary.com/fluid-attacks/image/upload/v1675871123/docs/api/api-token/revoke_token.png)

Please note that if you are going to revoke the
token because you do not remember it,
you will get a warning which will tell you the
last time you used it in the previous seven days.

![Warning to revoke token](https://res.cloudinary.com/fluid-attacks/image/upload/v1675871360/docs/api/api-token/warning.png)

If you revoke it and generate a new one,
keep in mind that the old token will no
longer be valid and will no longer be usable
in the implementations you have used it.

Now if you have never used the token or if the
last time you used it was more than seven days ago,
this confirmation message will not appear when
you revoke it and generate a new one.

## Playground Docs

In the playground,
you have a tab called **Docs**,
located on the right,
where it will show you all the
possible fields to build queries
and all the possible mutations.

![Playground](https://res.cloudinary.com/fluid-attacks/image/upload/v1661956347/docs/api/api-token/playground_docs.png)

By clicking on it,
you can continue to explore
tab by tab all the operations
that the API offers.

![Playground Tab](https://res.cloudinary.com/fluid-attacks/image/upload/v1661956661/docs/api/api-token/playground_tab_api.png)

We invite you to explore this
documentation in the API playground.

## Paginated fields

In the API,
you will find two
kinds of list fields.
Some are paginated
and others are not.
The main difference between them
is that non-paginated lists return
all available results directly,
returned as a normal list
between square brackets.

![Paginated Fields](https://res.cloudinary.com/fluid-attacks/image/upload/v1661956832/docs/api/api-token/paginated_list_fields.png)

While paginated lists,
often identified by the
suffix **connection**,
return only a certain amount
of results and a “cursor” that
can be included in subsequent
requests to advance through the pages.

![Suffix Connection](https://res.cloudinary.com/fluid-attacks/image/upload/v1661956982/docs/api/api-token/paginated_connection.png)

It is important to keep these
differences in mind when building
integrations that need to
retrieve all the information
in a paginated field.
We invite you read to more about
it on GraphQL's official website
[here](https://graphql.org/learn/pagination/).

Let's review this example together.
I want to validate the first ten
vulnerabilities of the Narrabri group.

![Paginated Example](https://res.cloudinary.com/fluid-attacks/image/upload/v1661957196/docs/api/api-token/paginated_example.png)

When putting the range of the
information that I want to bring me,
the result will bring me these.
If there is a next page in the
last item of the query,
there is **hasNextPage**
and **endCursor**,
which tells us that there is
the next page and gives
us its cursor token.

![Item Query](https://res.cloudinary.com/fluid-attacks/image/upload/v1661957372/docs/api/api-token/paginated_item.png)

To use the cursor,
you can pass it as the
argument **after** in
the paginated field.

![Argument After](https://res.cloudinary.com/fluid-attacks/image/upload/v1661957408/docs/api/api-token/paginated_argument.png)

You will be able to continue
exploring the pages as long
as hasNextPage is set to true.
The GraphQL documentation
offers more examples
[here](https://graphql.org/learn/pagination/#complete-connection-model).

## Rate limits

You can make 100 requests
per minute to the API.
If this value is exceeded,
it may fail the HTTP status code 429,
accompanied by a header
specifying the time to wait
before making the next request.

It is recommended to handle that
scenario in your script by reading
the  `"retry-after"` header,
and waiting that amount of
time before continuing.
In this example,
you can see how to control this
scenario in a Python script.

```python
import requests
from time import sleep
query = """
{
  me {
    userName
    userEmail
  }
}
"""
token = ""
def request():
    while True:
        response = requests.post(
            "https://app.fluidattacks.com/api",
            json={"query": query},
            headers={"authorization": f"Bearer {token}"},
        )
        if response.status_code == 429:
            seconds = response.headers["retry-after"]
            sleep(seconds + 1)
        else:
            break
    return response
response = request()
print(response.json())

```

This solution may vary depending
on the HTTP client library or
language of your preference.
Waiting 1 additional second to
the value indicated by the header
is also advisable.

## Temporary network errors

There may be moments where
the API cannot respond in
time due to high demand,
connection failures,
or other network-related issues.

It is recommended to implement
a retrying strategy,
where failed requests are performed
again a certain amount of times,
aiming to increase the resiliency
of your integration.
This is especially important
when supporting mission-critical flows.
Here’s a small example in a Python script.

```python
MAX_RETRIES = 10

def request():
    while True:
        response = requests.post(
            "https://app.fluidattacks.com/api",
            json={"query": query},
            headers={"authorization": f"Bearer {token}"},
        )

        if response.status_code == 429:
            seconds = response.headers["retry-after"]
            sleep(seconds + 1)
        elif response.status >= 500:
            retries += 1
            if retries == MAX_RETRIES:
                break
            sleep(retries)
        else:
            break

    return response

```

Remember that this solution may
vary depending on the HTTP client
library or language of your preference.

## ARM API response status

When the ARM API receives a request,
it can respond with different status codes.
Here are the most common ones.

| Code      | Description                                                                                                                                                                                                                                  |
|-----------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 200       | The request has been processed. You can read more about the response body on GraphQL’s official website [here](https://graphql.org/learn/serving-over-http/#response).                                                                                                                                |
| 400       | The request has a syntax error. Check the response for clues as to where it went wrong. Also, check https://graphql.org/learn/ to learn more about the  GraphQL query syntax.                                                                |
| 429       | The limit of requests per minute has been exceeded. Check the limits [here](https://gitlab.com/fluidattacks/universe/-/blob/trunk/common/dns/infra/rate_limit.tf#L3). You can modify your logic to reduce the number of requests or implement a retrying strategy, waiting the time indicated in the "retry-after" header (in seconds). |
| 502 - 504 | These errors can occur at times of high demand when the server cannot handle the request in time. They are usually temporary errors. We recommend implementing a retry mechanism. If the error persists, contact help@fluidattacks.com       |

## Response times

With GraphQL you can request a
large amount of data
in a single request,
but you have to keep in mind
that the response times will
vary accordingly.
Therefore it may be useful to
split queries in different requests as needed.
