---
id: streams
title: Streams
sidebar_label: Streams
slug: /development/stack/aws/dynamodb/streams
---

## Description

This [DynamoDB feature][feature] enables an [event-driven][event] approach to
process changes in the items of a DynamoDB table, which is suitable for
post-processing tasks such as replication to secondary datastores, updating
analytics, archiving data or triggering notifications.

## Implementation details

There are two approaches to consuming a DynamoDB stream:

1. Using [lambdas][lambdas]: This is the most common approach, in which the
   developer sets up an association between a stream and a lambda function.

   A big advantage here is that AWS takes care of consuming the stream on their
   side and triggering the lambda function automatically according to the
   event source mapping declared by the developer.

   On the other hand, this approach has the downside of coupling the stack to
   AWS lambdas, which are notoriously tricky to deploy as code with their
   dependencies using terraform and cannot run makes, making it harder to
   achieve local reproducibility.

1. Using the [Kinesis Client Library (KCL)][kcl]:
   DynamoDB streams was designed with a similar API to that of
   [Kinesis][kinesis], another AWS data streaming service, thus it is possible
   to use the KCL with an [adapter][adapter] to develop a custom consumer
   application.

   KCL is a java library that supports a language agnostic interface known as
   [MultiLangDaemon][daemon], which works by spawning the consumer process and
   communicating with it via stdin/stdout.

   While it is possible to consume the DynamoDB streams API using a
   language-specific SDK like [boto3][boto3], there are many tricks and details
   to take care of in order to guarantee reliable processing, which is why AWS
   provides this purpose-built library abstracting all those behaviors.

We decided to use the latter, aiming to circumvent the complexities and
environment disparities inherent to using lambdas.

[feature]: https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/streamsmain.html
[event]: https://en.wikipedia.org/wiki/Event-driven_architecture
[lambdas]: https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Streams.Lambda.html
[kcl]: https://docs.aws.amazon.com/streams/latest/dev/shared-throughput-kcl-consumers.html
[kinesis]: https://aws.amazon.com/kinesis/
[adapter]: https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Streams.KCLAdapter.html
[daemon]: https://docs.aws.amazon.com/streams/latest/dev/kinesis-record-processor-implementation-app-py.html
[boto3]: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodbstreams.html
