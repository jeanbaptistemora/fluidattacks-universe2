---
id: basics-api
title: 'Basics: API'
sidebar_label: 'Basics: API'
slug: /integrates/basics-api
---

This post will help you use Integrates API,
which is built as a GraphQL 2 service
where you can consume data using a common query language.
If you know how GraphQL works,
you can skip ahead to Integrates API Token post:

- The first step is to get some GraphQL knowledge,
  how it works and how to make queries to a GraphQL endpoint,
  you can do it in this Introduction in the official GraphQL site.

- It is recommended that before you face the Integrates API,
  learn how to make Queries and Mutations
  since these are the basics operations over any GraphQL endpoint.

- Once you get the basic knowledge about the main GraphQL concepts
  as Queries, Mutations, Fields, and Arguments,
  you are ready to explore Integrates API:

  - Go to Integrates API Token post
    and use Browser method to see info about you
    (in this case, your role in the application,
    remember that you have to previously log in on Integrates):
    ```
    query {
      me {
        role
      }
    }
    ```
  - If you want to get info about your projects,
    you can enhance the previous query to do it
    so, remember that, since Projects is a list of Project entities,
    whose are GraphQL entities,
    you must specify the items that you want from them,
    in this case, their names:
    ```
    query {
      me {
        projects {
          name
        }
      }
    }
    ```
