from aws.iam.utils import (
    yield_statements_from_policy_document,
)
from aws.model import (
    AWSApiGatewayStage,
    AWSCloudfrontDistribution,
    AWSCTrail,
    AWSDbInstance,
    AWSDefaultNetworkAcl,
    AWSDynamoDBTable,
    AWSEbsEncryptionByDefault,
    AWSEbsVolume,
    AWSEC2,
    AWSEC2Rule,
    AWSEfsFileSystem,
    AWSElb,
    AWSIamManagedPolicy,
    AWSIamManagedPolicyArns,
    AWSIamPolicyStatement,
    AWSIamRole,
    AWSInstance,
    AWSKmsKey,
    AWSLambdaFunction,
    AWSLaunchConfiguration,
    AWSLaunchTemplate,
    AWSLbTargetGroup,
    AWSRdsCluster,
    AWSRdsClusterInstance,
    AWSS3Bucket,
    AWSS3LogginConfig,
    AWSS3SSEConfig,
    AWSS3VersionConfig,
    S3VersioningEnum,
)
from itertools import (
    chain,
)
from lark import (
    Tree,
)
from parse_hcl2.common import (
    get_attribute_value,
    get_block_attribute,
    get_block_block,
    get_blocks_by_namespace,
    iterate_resources,
)
from parse_hcl2.tokens import (
    Block,
    Json,
)
from typing import (
    Any,
    Iterator,
    Literal,
)

JSONENCODE = Tree(data="identifier", children=["jsonencode"])


def iterate_iam_policy_documents(
    model: Any,
) -> Iterator[AWSIamPolicyStatement]:
    for iterator in (
        _iterate_iam_policy_documents_from_data_iam_policy_document,
        _iterate_iam_policy_documents_from_resource_with_policy,
    ):
        yield from iterator(model)


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


def get_principals_and_not_principals(
    block: Block,
    kind: Literal["principals", "not_principals"],
) -> str | dict | None:
    principal_val: dict = {}
    wildcard = "*"
    principals = get_blocks_by_namespace(block, kind)
    if not principals:
        return None
    for principal in principals:
        type_attr = get_block_attribute(principal, "type")
        identifiers_attr = get_block_attribute(principal, "identifiers")
        if type_attr is None or identifiers_attr is None:
            continue
        type_val: str = type_attr.val
        identifiers_val: list = (
            [identifiers_attr.val]
            if identifiers_attr and identifiers_attr.val == wildcard
            else identifiers_attr.val
        )
        if type_val == wildcard and wildcard in identifiers_val:
            return wildcard
        principal_val.update({type_val: identifiers_val})

    return principal_val


def get_conditions(block: Block) -> dict | None:
    condition_val: dict = {}
    conditions = get_blocks_by_namespace(block, "condition")
    if not conditions:
        return None
    for condition in conditions:
        test_attr = get_block_attribute(condition, "test")
        values_attr = get_block_attribute(condition, "values")
        variable_attr = get_block_attribute(condition, "variable")
        if test_attr is None or values_attr is None or variable_attr is None:
            continue
        test: str = test_attr.val
        values: str = values_attr.val
        variable: str = variable_attr.val
        if test not in condition_val:
            condition_val.update({test: {variable: values}})
        else:
            condition_val[test].update({variable: values})

    return condition_val


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
                    }.items()
                    for attr_data in [get_block_attribute(block, attr)]
                    if attr_data is not None
                }

                if principals := get_principals_and_not_principals(
                    block, "principals"
                ):
                    data.update({"Principal": principals})

                if not_principals := get_principals_and_not_principals(
                    block, "not_principals"
                ):
                    data.update({"NotPrincipal": not_principals})

                if conditions := get_conditions(block):
                    data.update({"Condition": conditions})

                # By default it's Allow in terraform
                if "Effect" not in data:
                    data["Effect"] = "Allow"

                yield AWSIamPolicyStatement(
                    column=block.column,
                    data=data,
                    line=block.line,
                )


def iter_aws_kms_key_policy_statements(
    model: Any,
) -> Iterator[AWSIamPolicyStatement]:
    iterator = iterate_resources(model, "resource", "aws_kms_key")
    for res in iterator:
        attribute = get_block_attribute(res, "policy")
        yield from _yield_statements_from_policy_document_attribute(attribute)


def iter_aws_s3_bucket_policy_statements(
    model: Any,
) -> Iterator[AWSIamPolicyStatement]:
    iterator = iterate_resources(model, "resource", "aws_s3_bucket_policy")
    for res in iterator:
        attribute = get_block_attribute(res, "policy")
        yield from _yield_statements_from_policy_document_attribute(attribute)


def iter_aws_iam_role(
    model: Any,
) -> Iterator[AWSIamRole]:
    iterator = iterate_resources(model, "resource", "aws_iam_role")
    for resource in iterator:
        yield AWSIamRole(
            data=resource.body,
            column=resource.column,
            line=resource.line,
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
    if attribute and isinstance(attribute.val, Tree):
        tree = attribute.val
        if tree.data == "function_call" and JSONENCODE in tree.children:
            data = tree.children[1].children[0]
            for stmt in yield_statements_from_policy_document(data):
                yield AWSIamPolicyStatement(
                    column=tree.column,
                    data=stmt,
                    line=tree.line,
                )


def iter_iam_user_policy(model: Any) -> Iterator[Any]:
    iterator = iterate_resources(model, "resource", "aws_iam_user_policy")
    for resource in iterator:
        yield AWSIamManagedPolicy(
            data=resource.body,
            column=resource.column,
            line=resource.line,
        )


def iterate_managed_policy_arns(
    model: Any,
    key: str = "",
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
            if key and block.key != key:
                continue
            yield AWSIamManagedPolicyArns(
                line=block.line, column=block.column, data=[block.val]
            )


def iter_s3_buckets(model: Any) -> Iterator[AWSS3Bucket]:
    iterator = iterate_resources(model, "resource", "aws_s3_bucket")
    for bucket in iterator:
        yield AWSS3Bucket(
            data=bucket.body,
            column=bucket.column,
            line=bucket.line,
            name=get_attribute_value(bucket.body, "bucket"),
            tf_reference=".".join(bucket.namespace[1:]),
        )


def iter_s3_sse_configuration(model: Any) -> Iterator[AWSS3SSEConfig]:
    iterator = iterate_resources(
        model, "resource", "aws_s3_bucket_server_side_encryption_configuration"
    )
    for sse_config in iterator:
        yield AWSS3SSEConfig(
            bucket=get_attribute_value(sse_config.body, "bucket"),
            column=sse_config.column,
            line=sse_config.line,
        )


def iter_s3_version_configuration(model: Any) -> Iterator[AWSS3VersionConfig]:
    iterator = iterate_resources(model, "resource", "aws_s3_bucket_versioning")
    for version_config in iterator:
        versioning_block = get_block_block(
            version_config, "versioning_configuration"
        )
        versioning_status: S3VersioningEnum
        if versioning_block is not None:
            versioning_status = get_attribute_value(
                versioning_block.body, "status"
            )
        yield AWSS3VersionConfig(
            bucket=get_attribute_value(version_config.body, "bucket"),
            column=version_config.column,
            line=version_config.line,
            status=S3VersioningEnum(versioning_status),
        )


def iter_s3_logging_configuration(model: Any) -> Iterator[AWSS3LogginConfig]:
    iterator = iterate_resources(model, "resource", "aws_s3_bucket_logging")
    for loggin_config in iterator:
        yield AWSS3LogginConfig(
            bucket=get_attribute_value(loggin_config.body, "bucket"),
            column=loggin_config.column,
            line=loggin_config.line,
            target=get_attribute_value(loggin_config.body, "target_bucket"),
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


def iter_aws_cloudtrail(model: Any) -> Iterator[Any]:
    iterator = iterate_resources(model, "resource", "aws_cloudtrail")
    for bucket in iterator:
        yield AWSCTrail(
            data=bucket.body,
            column=bucket.column,
            line=bucket.line,
        )


def iter_aws_kms_key(model: Any) -> Iterator[Any]:
    iterator = iterate_resources(model, "resource", "aws_kms_key")
    for bucket in iterator:
        yield AWSKmsKey(
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


def iter_aws_elb2_listener(model: Any) -> Iterator[Any]:
    iterator = iterate_resources(model, "resource", "aws_lb_listener")
    for resource in iterator:
        yield AWSElb(
            data=resource.body,
            column=resource.column,
            line=resource.line,
        )


def iter_aws_elb2(model: Any) -> Iterator[Any]:
    iterator = iterate_resources(model, "resource", "aws_lb")
    for resource in iterator:
        yield AWSElb(
            data=resource.body,
            column=resource.column,
            line=resource.line,
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


def iter_aws_sg_ingress_egress(
    model: Any,
    ingress: bool = False,
    egress: bool = False,
) -> Iterator[Any]:
    iterator = iterate_resources(
        model, "resource", "aws_security_group", "aws_security_group_rule"
    )
    for sg_res in iterator:
        if (sg_type := get_block_attribute(sg_res, "type")) and (
            (ingress and sg_type.val == "ingress")
            or (egress and sg_type.val == "egress")
        ):
            yield AWSEC2(
                data=sg_res.body,
                column=sg_res.column,
                line=sg_res.line,
            )
            continue
        if ingress and (ingress_block := get_block_block(sg_res, "ingress")):
            yield AWSEC2(
                data=ingress_block.body,
                column=ingress_block.column,
                line=ingress_block.line,
            )
        if egress and (egress_block := get_block_block(sg_res, "egress")):
            yield AWSEC2(
                data=egress_block.body,
                column=egress_block.column,
                line=egress_block.line,
            )


def iter_aws_security_group_rule(model: Any) -> Iterator[Any]:
    iterator = iterate_resources(model, "resource", "aws_security_group_rule")
    for bucket in iterator:
        yield AWSEC2Rule(
            data=bucket.body,
            column=bucket.column,
            line=bucket.line,
        )


def iter_aws_efs_file_system(model: Any) -> Iterator[Any]:
    iterator = iterate_resources(model, "resource", "aws_efs_file_system")
    for bucket in iterator:
        yield AWSEfsFileSystem(
            data=bucket.body,
            column=bucket.column,
            line=bucket.line,
        )


def iter_aws_launch_configuration(model: Any) -> Iterator[Any]:
    iterator = iterate_resources(model, "resource", "aws_launch_configuration")
    for bucket in iterator:
        yield AWSLaunchConfiguration(
            data=bucket.body,
            column=bucket.column,
            line=bucket.line,
        )


def iter_aws_api_gateway_stage(model: Any) -> Iterator[Any]:
    iterator = iterate_resources(model, "resource", "aws_api_gateway_stage")
    for bucket in iterator:
        yield AWSApiGatewayStage(
            data=bucket.body,
            column=bucket.column,
            line=bucket.line,
        )


def iter_aws_default_network_acl(model: Any) -> Iterator[Any]:
    iterator = iterate_resources(model, "resource", "aws_default_network_acl")
    for bucket in iterator:
        yield AWSDefaultNetworkAcl(
            data=bucket.body,
            column=bucket.column,
            line=bucket.line,
        )


def iter_aws_lambda_function(model: Any) -> Iterator[Any]:
    iterator = iterate_resources(model, "resource", "aws_lambda_function")
    for bucket in iterator:
        yield AWSLambdaFunction(
            data=bucket.body,
            column=bucket.column,
            line=bucket.line,
        )
