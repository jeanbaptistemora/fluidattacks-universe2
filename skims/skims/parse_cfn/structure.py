# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from aws.iam.utils import (
    yield_statements_from_policy,
    yield_statements_from_policy_document,
)
from metaloaders.model import (
    Node,
    Type,
)
from typing import (
    Any,
    Iterator,
    Tuple,
)


def iterate_resources(
    template: Node,
    *expected_resource_kinds: str,
    exact: bool = False,
) -> Iterator[Tuple[Node, Node, Node]]:
    if not isinstance(template, Node):
        return
    if template.data_type != Type.OBJECT:
        return

    if template_resources := template.inner.get("Resources", None):
        for resource_name, resource_config in template_resources.data.items():
            if (
                resource_config.data_type == Type.OBJECT
                and "Properties" in resource_config.inner
                and "Type" in resource_config.inner
            ):
                resource_properties = resource_config.inner["Properties"]
                resource_kind = resource_config.inner["Type"]

                for expected_resource_kind in expected_resource_kinds:
                    if (
                        not exact
                        and resource_kind.inner.startswith(
                            expected_resource_kind
                        )
                    ) or (
                        exact and resource_kind.inner == expected_resource_kind
                    ):
                        yield resource_name, resource_kind, resource_properties


def iterate_iam_policy_documents(
    template: Node,
) -> Iterator[Node]:
    for _, kind, props in iterate_resources(
        template, "AWS::IAM", "AWS::S3::BucketPolicy"
    ):

        if kind.inner in {
            "AWS::IAM::ManagedPolicy",
            "AWS::IAM::Policy",
            "AWS::S3::BucketPolicy",
        }:
            yield from yield_statements_from_policy(props)

        if (kind.inner in {"AWS::IAM::Role", "AWS::IAM::User"}) and (
            policies := props.inner.get("Policies", None)
        ):
            for policy in policies.data:
                yield from yield_statements_from_policy(policy)

        if (kind.inner in {"AWS::IAM::Role"}) and (
            document := props.inner.get("AssumeRolePolicyDocument", None)
        ):
            yield from yield_statements_from_policy_document(document)


def iterate_managed_policy_arns(
    template: Any,
) -> Iterator[Node]:
    for _, _, props in iterate_resources(template, "AWS::IAM"):
        if policies := props.inner.get("ManagedPolicyArns", None):
            yield policies


def iter_ec2_ingress_egress(
    template: Node,
    ingress: bool = False,
    egress: bool = False,
) -> Iterator[Node]:
    for _, kind, props in iterate_resources(
        template, "AWS::EC2::SecurityGroup"  # NOSONAR
    ):
        if kind.raw == "AWS::EC2::SecurityGroup":
            if ingress:
                yield from (
                    ingress
                    for ingress in getattr(
                        props.inner.get("SecurityGroupIngress", object),
                        "data",
                        [],
                    )
                )
            if egress:
                yield from (
                    ingress
                    for ingress in getattr(
                        props.inner.get("SecurityGroupEgress", object),
                        "data",
                        [],
                    )
                )
        elif ingress and kind.raw == "AWS::EC2::SecurityGroupIngress":
            yield props
        elif egress and kind.raw == "AWS::EC2::SecurityGroupEgress":
            yield props


def iter_ebs_block_devices(
    template: Node,
) -> Iterator[Node]:
    for _, _, props in iterate_resources(
        template, "AWS::AutoScaling::LaunchConfiguration"  # NOSONAR
    ):
        if block_dev_map_list := props.inner.get("BlockDeviceMappings"):
            for block_dev_map in block_dev_map_list.data:
                if block_device := block_dev_map.inner.get("Ebs"):
                    yield block_device


def iter_ec2_instance_ebs_block_devices(
    template: Node,
) -> Iterator[Node]:
    for _, _, props in iterate_resources(
        template, "AWS::EC2::Instance"  # NOSONAR
    ):
        if block_dev_map_list := props.inner.get("BlockDeviceMappings"):
            for block_dev_map in block_dev_map_list.data:
                if block_device := block_dev_map.inner.get("Ebs"):
                    yield block_device


def iter_ec2_security_groups(template: Node) -> Iterator[Node]:
    yield from (
        props
        for _, _, props in iterate_resources(
            template,
            "AWS::EC2::SecurityGroup",
            exact=True,
        )
    )


def iter_s3_buckets(template: Node) -> Iterator[Node]:
    yield from (
        props
        for _, _, props in iterate_resources(
            template,
            "AWS::S3::Bucket",
            exact=True,
        )
    )


def iter_s3_bucket_policies(template: Node) -> Iterator[Node]:
    yield from (
        props
        for _, _, props in iterate_resources(
            template,
            "AWS::S3::BucketPolicy",
            exact=True,
        )
    )


def iter_ec2_instances(template: Node) -> Iterator[Node]:
    yield from (
        props
        for _, _, props in iterate_resources(
            template,
            "AWS::EC2::Instance",
            exact=True,
        )
    )


def iter_ec2_launch_templates(template: Node) -> Iterator[Node]:
    yield from (
        props
        for _, _, props in iterate_resources(
            template,
            "AWS::EC2::LaunchTemplate",
            exact=True,
        )
    )


def iter_ec2_ltemplates_and_instances(template: Node) -> Iterator[Node]:
    yield from (
        props
        for _, _, props in iterate_resources(
            template,
            "AWS::EC2::LaunchTemplate",
            "AWS::EC2::Instance",
            exact=True,
        )
    )


def iter_ec2_volumes(template: Node) -> Iterator[Node]:
    yield from (
        props
        for _, _, props in iterate_resources(
            template,
            "AWS::EC2::Volume",
            exact=True,
        )
    )


def iter_api_gateway_stages(template: Node) -> Iterator[Node]:
    yield from (
        props
        for _, _, props in iterate_resources(
            template,
            "AWS::ApiGateway::Stage",
            exact=True,
        )
    )


def iter_cloudfront_distributions(template: Node) -> Iterator[Node]:
    yield from (
        props
        for _, _, props in iterate_resources(
            template,
            "AWS::CloudFront::Distribution",
            exact=True,
        )
    )


def iter_cloudtrail_trail(template: Node) -> Iterator[Node]:
    yield from (
        props
        for _, _, props in iterate_resources(
            template,
            "AWS::CloudTrail::Trail",
            exact=True,
        )
    )


def iter_dynamodb_table(template: Node) -> Iterator[Node]:
    yield from (
        props
        for _, _, props in iterate_resources(
            template,
            "AWS::DynamoDB::Table",
            exact=True,
        )
    )


def iter_elb_load_balancers(template: Node) -> Iterator[Node]:
    yield from (
        props
        for _, _, props in iterate_resources(
            template,
            "AWS::ElasticLoadBalancing::LoadBalancer",
            exact=True,
        )
    )


def iter_elb2_load_balancers(template: Node) -> Iterator[Node]:
    yield from (
        props
        for _, _, props in iterate_resources(
            template,
            "AWS::ElasticLoadBalancingV2::LoadBalancer",
            exact=True,
        )
    )


def iter_elb2_load_target_groups(template: Node) -> Iterator[Node]:
    yield from (
        props
        for _, _, props in iterate_resources(
            template,
            "AWS::ElasticLoadBalancingV2::TargetGroup",
            exact=True,
        )
    )


def iter_elb2_load_listeners(template: Node) -> Iterator[Node]:
    yield from (
        props
        for _, _, props in iterate_resources(
            template,
            "AWS::ElasticLoadBalancingV2::Listener",
            exact=True,
        )
    )


def iter_kms_keys(template: Node) -> Iterator[Node]:
    yield from (
        props
        for _, _, props in iterate_resources(
            template,
            "AWS::KMS::Key",
            exact=True,
        )
    )


def iter_efs_file_systems(template: Node) -> Iterator[Node]:
    yield from (
        props
        for _, _, props in iterate_resources(
            template,
            "AWS::EFS::FileSystem",
            exact=True,
        )
    )


def iter_secret_manager_secrets(template: Node) -> Iterator[Node]:
    yield from (
        props
        for _, _, props in iterate_resources(
            template,
            "AWS::SecretsManager::Secret",
            exact=True,
        )
    )


def iter_rds_clusters_and_instances(template: Node) -> Iterator[Node]:
    yield from (
        props
        for _, _, props in iterate_resources(
            template,
            "AWS::RDS::DBCluster",
            "AWS::RDS::DBInstance",
            exact=True,
        )
    )


def iter_iam_managed_policies_and_roles(template: Node) -> Iterator[Node]:
    yield from (
        props
        for _, _, props in iterate_resources(
            template,
            "AWS::IAM::ManagedPolicy",
            "AWS::IAM::Role",
            exact=True,
        )
    )


def iter_iam_managed_policies_and_mgd_policies(
    template: Node,
) -> Iterator[Node]:
    yield from (
        props
        for _, _, props in iterate_resources(
            template,
            "AWS::IAM::ManagedPolicy",
            "AWS::IAM::Policy",
            exact=True,
        )
    )


def iter_iam_users(template: Node) -> Iterator[Node]:
    yield from (
        props
        for _, _, props in iterate_resources(
            template,
            "AWS::IAM::User",
            exact=True,
        )
    )


def iter_iam_roles(template: Node) -> Iterator[Node]:
    yield from (
        props
        for _, _, props in iterate_resources(
            template,
            "AWS::IAM::Role",
            exact=True,
        )
    )


def iter_lambda_functions(template: Node) -> Iterator[Node]:
    yield from (
        props
        for _, _, props in iterate_resources(
            template,
            "AWS::Lambda::Function",
            exact=True,
        )
    )


def iter_severless_api(template: Node) -> Iterator[Node]:
    yield from (
        props
        for _, _, props in iterate_resources(
            template,
            "AWS::Serverless::Api",
            exact=True,
        )
    )
