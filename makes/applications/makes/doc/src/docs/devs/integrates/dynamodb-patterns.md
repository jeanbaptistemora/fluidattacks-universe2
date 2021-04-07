---
id: dynamodb-patterns
title: DynamoDB Patterns
sidebar_label: DynamoDB Patterns
slug: /devs/integrates/dynamodb-patterns
---

The following patterns were chosen following the best
[DynamoDB practices](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/bp-relational-modeling.html)
and with the business needs in mind. Some are for standardization among all the application

* Attribute names have no relationship to attribute values
* Store date-like data as integers, for easy comparison
* Automatic UUID generation for ids. 
When the attribute must have an id
(this is not applicable to available_groups since it is a simple string value),
it should be an uuid4.
* According to [official documentation](https://forums.aws.amazon.com/thread.jspa?threadID=93743)
the latency of a `get_item` vs a `query limit=1` will be equivalent. 
So it is better to have always both range and sort key for every table and GSI
* Use hierarchical relationships: group attributes will have an attribute, 
which is a sort key, with the following structure: ORG_ID#TYPE#STATUS. 
With this, it is easy to search for groups within a company, 
with a certain type in a given status, and everything in between, 
since a sort key can be searched partially

Calculations for [`write sharding`](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/bp-modeling-nosql-B.html):
```
ItemsPerRCU = 4KB / AvgItemSize

PartitionMaxReadRate = 3K * ItemsPerRCU

N = MaxRequiredIO / PartitionMaxReadRate
```

For groups. Get active and suspended groups. This query is important for forces executions:
```
10000 projected groups (more than fi_projects + fi_project_names) in the following 5 years
Currently, there are 594 projects, with a total size of 1.55MB (1'550.000 bytes)
At least 30% will be active-suspended, so:
MaxRequiredIO = 0.3 * 10000 = 3000
2609 bytes per item
ItemsPerRCU = 4KB / 2.6KB = 1,54
PartitionMaxReadRate = 3000 * 1,54 = 4.6K
N = 3000 / 4.6K = 0,65
```
Given the latter, there is no need to write sharding in groups items


For findings. 

https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/best-practices.html
- NoSQL Design
- Partition Key Design
- Sort Key Design
- Secondary Indexes
- Many-to-Many Relationships
- Relational Modeling
