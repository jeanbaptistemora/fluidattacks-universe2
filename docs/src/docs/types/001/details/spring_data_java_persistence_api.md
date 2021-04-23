---
id: spring_data_java_persistence_api
title: Spring Data Java Persistence API
sidebar_label: Spring Data Java persistence API
slug: /types/001/details/spring_data_java_persistence_api
---

In **Spring Data JPA** framework you can create SQL queries in many ways:

```c {3,7,15}
public interface UserRepository extends JpaRepository<User, Long> {
  // Using Java Persistence Query Language (JPQL)
  @Query("select u from User u where u.emailAddress = ?1")
  List<User> findByEmailAddress1(String emailAddress);

  // Using Spring Expression Language (SpEL)
  @Query("select u from User u where u.emailAddress = :#{[0]}")
  List<User> findByEmailAddress2(@Param("emailAddress") String emailAddress);
}

@Entity
// Using named queries
@NamedQuery(
  name = "User.findByEmailAddress3",
  query = "select u from User u where u.emailAddress = ?1"
)
public class User { /* ... */ }
```

## Abuse cases

No framework is silver-bullet, though.

### Java Persistence Query Language

By default the `JPQL` engine will escape the following
user-supplied input parameters:
- `JPQL` Positional Parameters: `?1`
- `JPQL` Named Parameters: `:emailAddress`

In other words,
`emailAddress` will be interpreted by the SQL engine as a string literal,
with possible special characters in a SQL context escaped.

However, if you write a `JPQL` query like this one:

```c {1}
@Query("select u from User u where u.emailAddress like %?1")
User findByEmailAddress(String emailAddress);
```

Notice the `%` we added in front of the JPQL positional parameter `?1`.

An attacker that manages to supply an `emailAddress` equal to `a`
will fetch all email addresses from the database that end with the letter `a`.
The resulting query will be:

```sql
SELECT u FROM User u WHERE u.emailAddress LIKE '%a'
```

We highly recommend you avoid mixing:
- `LIKE` conditions (or similar in its kind)
- hard-coded special wildcard characters
- user-supplied input

As noted in the example, sanitizing is no solution at all.
The problem is having a hard-coded `%` in the `JPQL` statement.

### Spring Expression Language

By default `SpEL` Expressions are **not escaped**.
This happens because `SpEL` is designed as an expression language,
not a SQL language.

In other words `SpEL Expressions Bindings` like `:#{[0]}` or `?#{[0]}`
will just copy the value of `[0]` into the SQL operation to be executed by the database.

If you write a `SpEL` query like this one:

```c
@Query("select u from User u where u.emailAddress = :#{[0]}")
List<User> findByEmailAddress2(@Param("emailAddress") String emailAddress);
```

An attacker that manages to supply an `emailAddress` equal to `%`,
will fetch all email addresses from the database.
The evaluated query will be:

```sql
SELECT u FROM User u WHERE u.emailAddress LIKE '%'
```

We highly recommend you to use the `escape` function from `SpEL` context as follow:

```c {3-4}
@Query(
  "select u from User u " +
  "where u.emailAddress like ?#{escape([0])} " +
  "escape ?#{escapeCharacter()}"
)
List<User> findByEmailAddress2(@Param("emailAddress") String emailAddress);
```

In this case the evaluated query would be:

```sql
SELECT u FROM User u WHERE u.emailAddress LIKE '\%' ESCAPE '\'
```
