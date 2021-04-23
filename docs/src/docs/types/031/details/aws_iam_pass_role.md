---
id: aws_iam_pass_role
title: AWS iam:PassRole
sidebar_label: AWS iam:PassRole
slug: /types/031/details/aws_iam_pass_role
---

To configure many AWS services, you must pass an IAM role to the service.
This allows the service to later assume the role and perform actions on your behalf.

By giving a role or user the `iam:PassRole` permission,
you are saying:
> this principal is allowed to assign AWS roles to resources and services in this account.

You can limit which roles a user or service can pass to others by specifying the
role ARN(s) in the Resource field of the policy that grants them `iam:PassRole`:

```json
{
  "Effect": "Allow",
  "Action": "iam:PassRole",
  "Resource": [
    "arn:aws:::123456789012:role/SomeRole"
    "arn:aws:::123456789012:role/OtherRole"
  ]
}
```

As a rule of thumb you should include **only** the roles required by your
application.
Wildcards and over-permissive resource grants highly increase the probability of
(or completely allow) a privilege escalation.

# References

- [AWS IAM:PassRole explained](https://blog.rowanudell.com/iam-passrole-explained/)
- [Granting a user permissions to pass a role to an AWS service](
    https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use_passrole.html)
