from aws.iam.utils import (
    yield_statements_from_policy_document,
)
from aws.model import (
    AWSCloudfrontDistribution,
    AWSDbInstance,
    AWSDynamoDBTable,
    AWSEbsEncryptionByDefault,
    AWSEbsVolume,
    AWSEC2,
    AWSEC2Rule,
    AWSElb,
    AWSFsxWindowsFileSystem,
    AWSIamManagedPolicyArns,
    AWSIamPolicyStatement,
    AWSInstance,
    AWSLaunchTemplate,
    AWSLbTargetGroup,
    AWSRdsCluster,
    AWSRdsClusterInstance,
    AWSS3Bucket,
)
from itertools import (
    chain,
)
from parse_hcl2.common import (
    get_block_attribute,
    get_block_block,
    iterate_resources,
)
from parse_hcl2.tokens import (
    Block,
    Json,
)
from typing import (
    Any,
    Iterator,
)


def iterate_iam_policy_documents(
    model: Any,
) -> Iterator[AWSIamPolicyStatement]:
    for iterator in (
        _iterate_iam_policy_documents_from_data_iam_policy_document,
        _iterate_iam_policy_documents_from_resource_with_assume_role_policy,
        _iterate_iam_policy_documents_from_resource_with_policy,
    ):
        yield from iterator(model)


def _iterate_iam_policy_documents_from_resource_with_assume_role_policy(
    model: Any,
) -> Iterator[AWSIamPolicyStatement]:
    for resource in iterate_resources(model, "resource", "aws_iam_role"):
        attribute = get_block_attribute(resource, "assume_role_policy")
        yield from _yield_statements_from_policy_document_attribute(attribute)


def _iterate_iam_policy_documents_from_resource_with_policy(
    model: Any,
) -> Iterator[AWSIamPolicyStatement]:
    for res in chain(
        iterate_resources(model, "resource", "aws_iam_group_policy"),
        iterate_resources(model, "resource", "aws_iam_policy"),
        iterate_resources(model, "resource", "aws_iam_role_policy"),
        iterate_resources(model, "resource", "aws_iam_user_policy"),
    ):
        attribute = get_block_attribute(res, "policy")
        yield from _yield_statements_from_policy_document_attribute(attribute)


def _iterate_iam_policy_documents_from_data_iam_policy_document(
    model: Any,
) -> Iterator[AWSIamPolicyStatement]:
    iterator = iterate_resources(model, "data", "aws_iam_policy_document")
    for resource in iterator:
        for block in resource.body:
            if (
                isinstance(block, Block)
                and block.namespace
                and block.namespace[0] == "statement"
            ):
                data = {
                    attr_alias: attr_data.val
                    for attr, attr_alias in {
                        "sid": "Sid",
                        "effect": "Effect",
                        "actions": "Action",
                        "not_actions": "NotAction",
                        "resources": "Resource",
                        "not_resources": "NotResource",
                        # pending to implement:
                        #  condition, not_principals, principals
                    }.items()
                    for attr_data in [get_block_attribute(block, attr)]
                    if attr_data is not None
                }

                # Load nested blocks
                data.update(
                    {
                        attr_alias: "set"
                        for attr, attr_alias in {
                            "condition": "Condition",
                            "principals": "Principal",
                            "not_principals": "NotPrincipal",
                        }.items()
                        for sub_block in [get_block_block(block, attr)]
                        if sub_block is not None
                    }
                )

                # By default it's Allow in terraform
                if "Effect" not in data:
                    data["Effect"] = "Allow"

                yield AWSIamPolicyStatement(
                    column=block.column,
                    data=data,
                    line=block.line,
                )


def _yield_statements_from_policy_document_attribute(
    attribute: Any,
) -> Iterator[AWSIamPolicyStatement]:
    if attribute and isinstance(attribute.val, Json):
        data = attribute.val
        for stmt in yield_statements_from_policy_document(data.data):
            yield AWSIamPolicyStatement(
                column=data.column,
                data=stmt,
                line=data.line,
            )


def iterate_managed_policy_arns(
    model: Any,
) -> Iterator[Any]:
    for resource in chain(
        iterate_resources(
            model, "resource", "aws_iam_group_policy_attachment"
        ),
        iterate_resources(model, "resource", "aws_iam_policy_attachment"),
        iterate_resources(model, "resource", "aws_iam_role_policy_attachment"),
        iterate_resources(model, "resource", "aws_iam_user_policy_attachment"),
    ):
        for block in resource.body:
            if block.key != "policy_arn":
                continue
            yield AWSIamManagedPolicyArns(
                line=block.line, column=block.column, data=[block.val]
            )


def iter_s3_buckets(model: Any) -> Iterator[Any]:
    iterator = iterate_resources(model, "resource", "aws_s3_bucket")
    for bucket in iterator:
        yield AWSS3Bucket(
            data=bucket.body,
            column=bucket.column,
            line=bucket.line,
        )


def iter_aws_cloudfront_distribution(model: Any) -> Iterator[Any]:
    iterator = iterate_resources(
        model, "resource", "aws_cloudfront_distribution"
    )
    for bucket in iterator:
        yield AWSCloudfrontDistribution(
            data=bucket.body,
            column=bucket.column,
            line=bucket.line,
        )


def iter_aws_fsx_windows_file_system(model: Any) -> Iterator[Any]:
    iterator = iterate_resources(
        model, "resource", "aws_fsx_windows_file_system"
    )
    for bucket in iterator:
        yield AWSFsxWindowsFileSystem(
            data=bucket.body,
            column=bucket.column,
            line=bucket.line,
        )


def iter_aws_ebs_volume(model: Any) -> Iterator[Any]:
    iterator = iterate_resources(model, "resource", "aws_ebs_volume")
    for bucket in iterator:
        yield AWSEbsVolume(
            data=bucket.body,
            column=bucket.column,
            line=bucket.line,
        )


def iter_aws_instance(model: Any) -> Iterator[Any]:
    iterator = iterate_resources(model, "resource", "aws_instance")
    for bucket in iterator:
        yield AWSInstance(
            data=bucket.body,
            column=bucket.column,
            line=bucket.line,
        )


def iter_aws_elb(model: Any) -> Iterator[Any]:
    iterator = iterate_resources(model, "resource", "aws_elb")
    for bucket in iterator:
        yield AWSElb(
            data=bucket.body,
            column=bucket.column,
            line=bucket.line,
        )


def iter_aws_lb_target_group(model: Any) -> Iterator[Any]:
    iterator = iterate_resources(model, "resource", "aws_lb_target_group")
    for bucket in iterator:
        yield AWSLbTargetGroup(
            data=bucket.body,
            column=bucket.column,
            line=bucket.line,
        )


def iter_aws_db_instance(model: Any) -> Iterator[Any]:
    iterator = iterate_resources(model, "resource", "aws_db_instance")
    for bucket in iterator:
        yield AWSDbInstance(
            data=bucket.body,
            column=bucket.column,
            line=bucket.line,
        )


def iter_aws_ebs_encryption_by_default(model: Any) -> Iterator[Any]:
    iterator = iterate_resources(
        model, "resource", "aws_ebs_encryption_by_default"
    )
    for bucket in iterator:
        yield AWSEbsEncryptionByDefault(
            data=bucket.body,
            column=bucket.column,
            line=bucket.line,
        )


def iter_aws_rds_cluster(model: Any) -> Iterator[Any]:
    iterator = iterate_resources(model, "resource", "aws_rds_cluster")
    for bucket in iterator:
        yield AWSRdsCluster(
            data=bucket.body,
            column=bucket.column,
            line=bucket.line,
        )


def iter_aws_rds_cluster_instance(model: Any) -> Iterator[Any]:
    iterator = iterate_resources(model, "resource", "aws_rds_cluster_instance")
    for bucket in iterator:
        yield AWSRdsClusterInstance(
            data=bucket.body,
            column=bucket.column,
            line=bucket.line,
        )


def iter_aws_dynambodb_table(model: Any) -> Iterator[Any]:
    iterator = iterate_resources(model, "resource", "aws_dynamodb_table")
    for bucket in iterator:
        yield AWSDynamoDBTable(
            data=bucket.body,
            column=bucket.column,
            line=bucket.line,
        )


def iter_aws_launch_template(model: Any) -> Iterator[Any]:
    iterator = iterate_resources(model, "resource", "aws_launch_template")
    for bucket in iterator:
        yield AWSLaunchTemplate(
            data=bucket.body,
            column=bucket.column,
            line=bucket.line,
        )


def iter_aws_security_group(model: Any) -> Iterator[Any]:
    iterator = iterate_resources(model, "resource", "aws_security_group")
    for bucket in iterator:
        yield AWSEC2(
            data=bucket.body,
            column=bucket.column,
            line=bucket.line,
        )


def iter_aws_security_group_rule(model: Any) -> Iterator[Any]:
    iterator = iterate_resources(model, "resource", "aws_security_group_rule")
    for bucket in iterator:
        yield AWSEC2Rule(
            data=bucket.body,
            column=bucket.column,
            line=bucket.line,
        )
