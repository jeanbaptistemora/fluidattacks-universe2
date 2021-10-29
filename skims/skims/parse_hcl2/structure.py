from aws.iam.utils import (
    yield_statements_from_policy_document,
)
from aws.model import (
    AWSCloudfrontDistribution,
    AWSEbsVolume,
    AWSFsxWindowsFileSystem,
    AWSIamManagedPolicyArns,
    AWSIamPolicyStatement,
    AWSInstance,
    AWSS3Bucket,
)
from itertools import (
    chain,
)
from lark import (
    Tree,
)
from parse_hcl2.tokens import (
    Attribute,
    Block,
    Json,
)
from typing import (
    Any,
    Iterator,
    List,
    Optional,
    Union,
)


def get_block_attribute(block: Block, key: str) -> Optional[Attribute]:
    for attribute in iterate_block_attributes(block):
        if attribute.key == key:
            return attribute
    return None


def get_block_block(block: Block, namespace: str) -> Optional[Block]:
    for nested_block in iterate_block_blocks(block):
        if nested_block.namespace and nested_block.namespace[0] == namespace:
            return nested_block
    return None


def get_attribute_by_block(
    block: Block, namespace: str, key: str
) -> Optional[Attribute]:
    for nested_block in iterate_block_blocks(block):
        if nested_block.namespace and nested_block.namespace[0] == namespace:
            for attribute in iterate_block_attributes(nested_block):
                if attribute.key == key:
                    return attribute
    return None


def iterate_resources(
    model: Any,
    expected_source: str,
    *expected_kinds: str,
) -> Iterator[Block]:
    if isinstance(model, Tree):
        for child in model.children:
            yield from iterate_resources(
                child,
                expected_source,
                *expected_kinds,
            )
    elif isinstance(model, Block) and (
        len(model.namespace) == 3
        and model.namespace[0] == expected_source
        and model.namespace[1] in expected_kinds
    ):
        yield model


def iterate_block_attributes(block: Block) -> Iterator[Attribute]:
    for item in block.body:
        if isinstance(item, Attribute):
            yield item


def iterate_block_blocks(block: Block) -> Iterator[Block]:
    for item in block.body:
        if isinstance(item, Block):
            yield item


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


def get_argument(
    body: List[Union[Attribute, Block]], key: str, default: Any = None
) -> Union[Any, Block]:
    for item in body:
        if isinstance(item, Attribute):
            continue
        if isinstance(item, Block) and key in item.namespace:
            return item
    return default


def get_attribute(
    body: List[Union[Attribute, Block]], key: str, default: Any = None
) -> Union[Any, Block]:
    for item in body:
        if isinstance(item, Block):
            continue
        if isinstance(item, Attribute) and item.key == key:
            return item
    return default


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
