from enum import (
    Enum,
)
from typing import (
    Any,
    NamedTuple,
)


class S3VersioningEnum(Enum):
    DISABLED: str = "Disabled"
    ENABLED: str = "Enabled"
    SUSPENDED: str = "Suspended"


class AWSIamPolicyStatement(NamedTuple):
    column: int
    data: Any
    line: int


class AWSIamManagedPolicyArns(NamedTuple):
    column: int
    data: list[str] | None
    line: int


class AWSS3Bucket(NamedTuple):
    column: int
    data: list[Any]
    line: int
    name: str | None = None
    tf_reference: str | None = None


class AWSS3SSEConfig(NamedTuple):
    bucket: str
    column: int
    line: int


class AWSS3VersionConfig(NamedTuple):
    bucket: str
    column: int
    line: int
    status: S3VersioningEnum


class AWSS3LogginConfig(NamedTuple):
    bucket: str
    column: int
    line: int
    target: str


class AWSS3BucketPolicy(NamedTuple):
    column: int
    data: list[Any]
    line: int


class AWSS3Acl(NamedTuple):
    column: int
    data: str
    line: int


class AWSCloudfrontDistribution(NamedTuple):
    column: int
    data: list[Any]
    line: int


class AWSCTrail(NamedTuple):
    column: int
    data: list[Any]
    line: int


class AWSEbs(NamedTuple):
    column: int
    data: list[Any]
    line: int


class AWSEbsVolume(NamedTuple):
    column: int
    data: list[Any]
    line: int


class AWSDynamoDBTable(NamedTuple):
    column: int
    data: list[Any]
    line: int


class AWSInstance(NamedTuple):
    column: int
    data: list[Any]
    line: int


class AWSElb(NamedTuple):
    column: int
    data: list[Any]
    line: int


class AWSElbV2(NamedTuple):
    column: int
    data: list[Any]
    line: int


class AWSLbTargetGroup(NamedTuple):
    column: int
    data: list[Any]
    line: int


class AWSDbInstance(NamedTuple):
    column: int
    data: list[Any]
    line: int


class AWSEbsEncryptionByDefault(NamedTuple):
    column: int
    data: list[Any]
    line: int


class AWSRdsCluster(NamedTuple):
    column: int
    data: list[Any]
    line: int


class AWSRdsClusterInstance(NamedTuple):
    column: int
    data: list[Any]
    line: int


class AWSKmsKey(NamedTuple):
    column: int
    data: list[Any]
    line: int


class AWSEFS(NamedTuple):
    column: int
    data: list[Any]
    line: int


class AWSSecretsManagerSecret(NamedTuple):
    column: int
    data: list[Any]
    line: int


class AWSLaunchTemplate(NamedTuple):
    column: int
    data: list[Any]
    line: int


class AWSIamManagedPolicy(NamedTuple):
    column: int
    data: list[Any]
    line: int


class AWSIamRole(NamedTuple):
    column: int
    data: list[Any]
    line: int


class AWSEC2(NamedTuple):
    column: int
    data: list[Any]
    line: int


class AWSEC2Rule(NamedTuple):
    column: int
    data: list[Any]
    line: int


class AWSEfsFileSystem(NamedTuple):
    column: int
    data: list[Any]
    line: int


class AWSLaunchConfiguration(NamedTuple):
    column: int
    data: list[Any]
    line: int


class AWSApiGatewayStage(NamedTuple):
    column: int
    data: list[Any]
    line: int


class AWSDefaultNetworkAcl(NamedTuple):
    column: int
    data: list[Any]
    line: int


class AWSLambdaFunction(NamedTuple):
    column: int
    data: list[Any]
    line: int


class AWSServerlessApi(NamedTuple):
    column: int
    data: list[Any]
    line: int
