from typing import (
    Any,
    List,
    NamedTuple,
    Optional,
)


class AWSIamPolicyStatement(NamedTuple):
    column: int
    data: Any
    line: int


class AWSIamManagedPolicyArns(NamedTuple):
    column: int
    data: Optional[List[str]]
    line: int


class AWSS3Bucket(NamedTuple):
    column: int
    data: List[Any]
    line: int


class AWSS3BucketPolicy(NamedTuple):
    column: int
    data: List[Any]
    line: int


class AWSS3Acl(NamedTuple):
    column: int
    data: str
    line: int


class AWSCloudfrontDistribution(NamedTuple):
    column: int
    data: List[Any]
    line: int


class AWSCTrail(NamedTuple):
    column: int
    data: List[Any]
    line: int


class AWSFsxWindowsFileSystem(NamedTuple):
    column: int
    data: List[Any]
    line: int


class AWSEbsVolume(NamedTuple):
    column: int
    data: List[Any]
    line: int


class AWSDynamoDBTable(NamedTuple):
    column: int
    data: List[Any]
    line: int


class AWSInstance(NamedTuple):
    column: int
    data: List[Any]
    line: int


class AWSElb(NamedTuple):
    column: int
    data: List[Any]
    line: int


class AWSElbV2(NamedTuple):
    column: int
    data: List[Any]
    line: int


class AWSLbTargetGroup(NamedTuple):
    column: int
    data: List[Any]
    line: int


class AWSDbInstance(NamedTuple):
    column: int
    data: List[Any]
    line: int


class AWSEbsEncryptionByDefault(NamedTuple):
    column: int
    data: List[Any]
    line: int


class AWSRdsCluster(NamedTuple):
    column: int
    data: List[Any]
    line: int


class AWSRdsClusterInstance(NamedTuple):
    column: int
    data: List[Any]
    line: int


class AWSKmsKey(NamedTuple):
    column: int
    data: List[Any]
    line: int


class AWSFSxFileSystem(NamedTuple):
    column: int
    data: List[Any]
    line: int


class AWSSecretsManagerSecret(NamedTuple):
    column: int
    data: List[Any]
    line: int


class AWSLaunchTemplate(NamedTuple):
    column: int
    data: List[Any]
    line: int


class AWSIamManagedPolicy(NamedTuple):
    column: int
    data: List[Any]
    line: int
