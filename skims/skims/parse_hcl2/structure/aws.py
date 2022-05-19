from aws.iam.utils import (
    yield_statements_from_policy_document,
)
from aws.model import (
    AWSApiGatewayStage,
    AWSCloudfrontDistribution,
    AWSCTrail,
    AWSDbInstance,
    AWSDynamoDBTable,
    AWSEbsEncryptionByDefault,
    AWSEbsVolume,
    AWSEC2,
    AWSEC2Rule,
    AWSEfsFileSystem,
    AWSElb,
    AWSIamManagedPolicy,
    AWSIamManagedPolicyArns,
    AWSIamPolicyAttachment,
    AWSIamPolicyStatement,
    AWSInstance,
    AWSKmsKey,
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
from parse_hcl2.common import (
    get_attribute_by_block,
    get_attribute_value,
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
                            "not_principals": "NotPrincipal",
                        }.items()
                        for sub_block in [get_block_block(block, attr)]
                        if sub_block is not None
                    }
                )
                if principals := get_attribute_by_block(
                    block, "principals", "identifiers"
                ):
                    data.update({"Principal": principals.val})

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


def iter_iam_user_policy(model: Any) -> Iterator[Any]:
    iterator = iterate_resources(model, "resource", "aws_iam_user_policy")
    for resource in iterator:
        yield AWSIamManagedPolicy(
            data=resource.body,
            column=resource.column,
            line=resource.line,
        )


def iter_iam_policy_attachment(model: Any) -> Iterator[Any]:
    iterator = iterate_resources(
        model, "resource", "aws_iam_policy_attachment"
    )
    for resource in iterator:
        yield AWSIamPolicyAttachment(
            data=resource.body,
            column=resource.column,
            line=resource.line,
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
