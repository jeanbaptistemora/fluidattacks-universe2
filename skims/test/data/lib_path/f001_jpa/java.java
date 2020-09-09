package com.fluidattacks.skims.test.f001;

import org.skife.jdbi.v2.sqlobject.SqlQuery;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;

import java.util.List;

// ?0 == ?#{[0]}
public interface ParametersJpaRepository extends JpaRepository<Parameter, String> {

    /* Secure */
    @Query(value = "SELECT * FROM schema.table " +
        "WHERE CODE = ?1", nativeQuery = true)
    List<Parameter> findByParameterType(String parameterTypeCode);
    /* Secure */
    @Query("select u from User u where u.firstname like %?#{escape([0])}% escape ?#{escapeCharacter()}")
    List<User> findContainingEscaped(String namePart);

    /* secure*/
    @Query("select u from User u where u.lastname like :#{[0]}")
    /* LIKE statement injection */
    @SqlQuery("select u from User u where u.lastname like %:#{[0]}%")
    List<User> findByLastnameWithSpelExpression(@Param("lastname") String lastname);
    /* LIKE statement injection */
    @Query("select u from User u where u.lastname like %:#{" + "[0]}%")
    List<User> findByLastnameWithSpelExpression(@Param("lastname") String lastname);
    /* LIKE statement secure */
    @Query("select u from User u where u.lastname like %?#{escape([0])}%")
    List<User> findByLastnameWithSpelExpression(@Param("lastname") String lastname);
    /* LIKE statement secure */
    @Query("select u from User u where u.firstname like %?#{esc" + "ape([0])}%")
    List<User> findByLastnameWithSpelExpression(@Param("lastname") String lastname);

    /* LIKE statement injection */
    @Query("select u from " + "User u where u.lastname like %:lastname%")
    List<User> findByLastnameWithSpelExpression(@Param("lastname") String lastname);
    /* LIKE statement injection a little harder to find*/
    @Query("select u from " + "User u where u.lastname like %:last" + "name%")
    List<User> findByLastnameWithSpelExpression(@Param("lastname") String lastname);
    /* LIKE statement injection */
    @Query("SELECT e FROM ExamplePage e WHERE e.id LIKE CONCAT('%',:id,'%')")
    Page<ExamplePage> getRechargeEvents(@Param("id") Long id, Pageable pageable);
    /* LIKE statement injection */
    @SqlQuery("SEL" +
        "ECT e FROM ExamplePage e WHERE e.id LIKE ?10%")
    Page<ExamplePage> getRechargeEvents(@Param("id") Long id, Pageable pageable);
    /* Secure */
    @SqlQuery("SEL" +
        "ECT e FROM ExamplePage e WHERE e.id LIKE ?10")
    Page<ExamplePage> getRechargeEvents(@Param("id") Long id, Pageable pageable);
}

/*
https://docs.spring.io/spring-data/jpa/docs/current/reference/html

    5.3.1. Query Lookup Strategies

    The JPA module supports defining a query manually as a String or having it being
    derived from the method name.

    Derived queries with the predicates IsStartingWith, StartingWith, StartsWith,
    IsEndingWith, EndingWith, EndsWith, IsNotContaining, NotContaining, NotContains,
    IsContaining, Containing, Contains the respective arguments for these queries
    will get sanitized. This means if the arguments actually contain characters
    recognized by LIKE as wildcards these will get escaped so they match only as
    literals. The escape character used can be configured by setting the
    escapeCharacter of the @EnableJpaRepositories annotation.

> Using IsStartingWith, StartingWith, StartsWith, etc is safe

    Example 69. Using SpEL expressions in repository query methods - accessing arguments.

    @Query("select u from User u where u.firstname = ?1 and u.firstname=?#{[0]} and u.emailAddress = ?#{principal.emailAddress}")
    List<User> findByFirstnameAndCurrentUserWithCustomQuery(String firstname);

    For like-conditions one often wants to append % to the beginning or the end of a
    String valued parameter. This can be done by appending or prefixing a bind parameter
    marker or a SpEL expression with %. Again the following example demonstrates this.

    Example 70. Using SpEL expressions in repository query methods - wildcard shortcut.

    @Query("select u from User u where u.lastname like %:#{[0]}% and u.lastname like %:lastname%")
    List<User> findByLastnameWithSpelExpression(@Param("lastname") String lastname);

    When using like-conditions with values that are coming from a not secure source the
    values should be sanitized so they can’t contain any wildcards and thereby allow
    attackers to select more data than they should be able to. For this purpose the
    the escape(String) method is made available in the SpEL context. It prefixes all
    instances of _ and % in the first argument with the single character from the
    second argument. In combination with the escape clause of the like expression
    available in JPA and standard SQL this allows easy cleaning of bind parameters.

> Any like with parameters is vulnerable unless explicitly escaped

    Example 71. Using SpEL expressions in repository query methods - sanitizing input
    values.

    @Query("select u from User u where u.firstname like %?#{escape([0])}% escape ?#{escapeCharacter()}")
    List<User> findContainingEscaped(String namePart);

    Given this method declaration in an repository interface findContainingEscaped("Peter_")"
    will find `Peter_Parker but not Peter Parker. The escape character used can be
    configured by setting the escapeCharacter of the @EnableJpaRepositories annotation.
    Note that the method escape(String) available in the SpEL context will only escape
    the SQL and JPA standard wildcards _ and %. If the underlying database or the JPA
    implementation supports additional wildcards these will not get escaped.
*/
