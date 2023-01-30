# pylint: disable=invalid-name,too-many-lines
"""
Update the vulnerability developer information about skims methods
since the SARIF log did not include that information
since the change in the architecture.
Ensure all Machine vulnerabilities are reported by machine@fluidattacks.com
and remove jrestrepo from all vulnerability reports.

Execution Time:    2022-09-21 at 00:00:00 UTC
Finalization Time: 2022-09-22 at 01:17:30 UTC

Second execution to include vulnerabilities reported by Machine
but with a state modified through ARM

Execution Time:    2022-10-13 at 23:35:59 UTC
Finalization Time: 2022-10-14 at 00:02:28 UTC

"""
from aioextensions import (
    collect,
    run,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.enums import (
    Source,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
    VulnerabilityMetadataToUpdate,
)
from db_model.vulnerabilities.update import (
    update_metadata,
)
from enum import (
    Enum,
)
from organizations import (
    domain as orgs_domain,
)
import time
from typing import (
    Dict,
    List,
    NamedTuple,
    Optional,
    Tuple,
)


class SkimsMethodInfo(NamedTuple):
    file_name: str
    name: str
    developer: str


class SkimsMethods(Enum):
    CS_SQL_INJECTION = SkimsMethodInfo(
        developer="jecheverri@fluidattacks.com",
        file_name="c_sharp",
        name="c_sharp_sql_injection",
    )
    QUERY_F001 = SkimsMethodInfo(
        developer="drestrepo@fluidattacks.com",
        file_name="c_sharp",
        name="c_sharp_sql_user_params",
    )
    QUERY_F004 = SkimsMethodInfo(
        developer="drestrepo@fluidattacks.com",
        file_name="query",
        name="query_f004",
    )
    CS_REMOTE_COMMAND_EXECUTION = SkimsMethodInfo(
        developer="jecheverri@fluidattacks.com",
        file_name="c_sharp",
        name="c_sharp_remote_command_execution",
    )
    JAVA_REMOTE_COMMAND_EXECUTION = SkimsMethodInfo(
        developer="machine@fluidattacks.com",
        file_name="java",
        name="java_remote_command_execution",
    )
    JS_REMOTE_COMMAND_EXECUTION = SkimsMethodInfo(
        developer="machine@fluidattacks.com",
        file_name="javascript",
        name="javascript_remote_command_execution",
    )
    QUERY_F008 = SkimsMethodInfo(
        developer="drestrepo@fluidattacks.com",
        file_name="query",
        name="query_f008",
    )
    CS_INSEC_ADDHEADER_WRITE = SkimsMethodInfo(
        developer="asalgado@fluidattacks.com",
        file_name="c_sharp",
        name="c_sharp_insec_addheader_write",
    )
    AWS_CREDENTIALS = SkimsMethodInfo(
        developer="machine@fluidattacks.com",
        file_name="aws",
        name="aws_credentials",
    )
    DOCKER_ENV_SECRETS = SkimsMethodInfo(
        developer="acuberos@fluidattacks.com",
        file_name="docker",
        name="dockerfile_env_secrets",
    )
    DOCKER_COMPOSE_ENV_SECRETS = SkimsMethodInfo(
        developer="atrujillo@fluidattacks.com",
        file_name="docker",
        name="docker_compose_env_secrets",
    )
    JAVA_PROP_SENSITIVE = SkimsMethodInfo(
        developer="acuberos@fluidattacks.com",
        file_name="java",
        name="java_properties_sensitive_data",
    )
    SENSITIVE_KEY_JSON = SkimsMethodInfo(
        developer="asalgado@fluidattacks.com",
        file_name="conf_files",
        name="sensitive_key_in_json",
    )
    SENSITIVE_INFO_DOTNET_JSON = SkimsMethodInfo(
        developer="jecheverri@fluidattacks.com",
        file_name="conf_files",
        name="sensitive_info_in_dotnet_json",
    )
    SENSITIVE_INFO_JSON = SkimsMethodInfo(
        developer="jecheverri@fluidattacks.com",
        file_name="conf_files",
        name="sensitive_info_in_json",
    )
    WEB_USER_PASS = SkimsMethodInfo(
        developer="machine@fluidattacks.com",
        file_name="conf_files",
        name="web_config_user_pass",
    )
    WEB_DB_CONN = SkimsMethodInfo(
        developer="drestrepo@fluidattacks.com",
        file_name="conf_files",
        name="web_config_db_connection",
    )
    JS_CRYPTO_CREDENTIALS = SkimsMethodInfo(
        developer="machine@fluidattacks.com",
        file_name="javascript",
        name="javascript_crypto_js_credentials",
    )
    JWT_TOKEN = SkimsMethodInfo(
        developer="drestrepo@fluidattacks.com",
        file_name="conf_files",
        name="jwt_token",
    )
    GEM_GEMFILE = SkimsMethodInfo(
        developer="lcontreras@fluidattacks.com",
        file_name="gem",
        name="gem_gemfile",
    )
    GEM_GEMFILE_LOCK = SkimsMethodInfo(
        developer="lcontreras@fluidattacks.com",
        file_name="gem",
        name="gem_gemfile_lock",
    )
    MAVEN_POM_XML = SkimsMethodInfo(
        developer="acuberos@fluidattacks.com",
        file_name="maven",
        name="maven_pom_xml",
    )
    MAVEN_GRADLE = SkimsMethodInfo(
        developer="acuberos@fluidattacks.com",
        file_name="maven",
        name="maven_gradle",
    )
    MAVEN_SBT = SkimsMethodInfo(
        developer="acuberos@fluidattacks.com",
        file_name="maven",
        name="maven_sbt",
    )
    NPM_YARN_LOCK = SkimsMethodInfo(
        developer="machine@fluidattacks.com",
        file_name="npm",
        name="npm_yarn_lock",
    )
    NPM_PACKAGE_JSON = SkimsMethodInfo(
        developer="machine@fluidattacks.com",
        file_name="npm",
        name="npm_package_json",
    )
    NPM_PACKAGE_LOCK_JSON = SkimsMethodInfo(
        developer="machine@fluidattacks.com",
        file_name="npm",
        name="npm_package_lock_json",
    )
    NUGET_CSPROJ = SkimsMethodInfo(
        developer="machine@fluidattacks.com",
        file_name="nuget",
        name="nuget_csproj",
    )
    NUGET_PACKAGES_CONFIG = SkimsMethodInfo(
        developer="machine@fluidattacks.com",
        file_name="nuget",
        name="nuget_packages_config",
    )
    PIP_REQUIREMENTS_TXT = SkimsMethodInfo(
        developer="lsaavedra@fluidattacks.com",
        file_name="pip",
        name="pip_requirements_txt",
    )
    CS_XSL_TRANSFORM_OBJECT = SkimsMethodInfo(
        developer="jecheverri@fluidattacks.com",
        file_name="c_sharp",
        name="c_sharp_xsl_transform_object",
    )
    CS_SCHEMA_BY_URL = SkimsMethodInfo(
        developer="jecheverri@fluidattacks.com",
        file_name="c_sharp",
        name="c_sharp_schema_by_url",
    )
    JAVA_JPA_LIKE = SkimsMethodInfo(
        developer="drestrepo@fluidattacks.com",
        file_name="java",
        name="java_jpa_like",
    )
    JMX_HEADER_BASIC = SkimsMethodInfo(
        developer="jromero@fluidattacks.com",
        file_name="conf_files",
        name="jmx_header_basic",
    )
    TFM_AZURE_VM_INSEC_AUTH = SkimsMethodInfo(
        developer="jecheverri@fluidattacks.com",
        file_name="terraform",
        name="tfm_azure_virtual_machine_insecure_authentication",
    )
    TFM_AZURE_LNX_VM_INSEC_AUTH = SkimsMethodInfo(
        developer="jecheverri@fluidattacks.com",
        file_name="terraform",
        name="tfm_azure_linux_vm_insecure_authentication",
    )
    WWW_AUTHENTICATE = SkimsMethodInfo(
        developer="jecheverri@fluidattacks.com",
        file_name="analyze_headers",
        name="www_authenticate",
    )
    CS_WEAK_PROTOCOL = SkimsMethodInfo(
        developer="jecheverri@fluidattacks.com",
        file_name="c_sharp",
        name="c_sharp_weak_protocol",
    )
    CS_SERVICE_POINT_MANAGER_DISABLED = SkimsMethodInfo(
        developer="jecheverri@fluidattacks.com",
        file_name="c_sharp",
        name="c_sharp_service_point_manager_disabled",
    )
    CS_INSECURE_SHARED_ACCESS_PROTOCOL = SkimsMethodInfo(
        developer="jecheverri@fluidattacks.com",
        file_name="c_sharp",
        name="c_sharp_insecure_shared_access_protocol",
    )
    CS_HTTPCLIENT_NO_REVOCATION_LIST = SkimsMethodInfo(
        developer="jecheverri@fluidattacks.com",
        file_name="c_sharp",
        name="c_sharp_httpclient_no_revocation_list",
    )
    CFN_INSEC_PROTO = SkimsMethodInfo(
        developer="atrujillo@fluidattacks.com",
        file_name="cloudformation",
        name="cfn_serves_content_over_insecure_protocols",
    )
    TFM_AWS_INSEC_PROTO = SkimsMethodInfo(
        developer="jecheverri@fluidattacks.com",
        file_name="terraform",
        name="tfm_aws_serves_content_over_insecure_protocols",
    )
    TFM_AZURE_INSEC_PROTO = SkimsMethodInfo(
        developer="jecheverri@fluidattacks.com",
        file_name="terraform",
        name="tfm_azure_serves_content_over_insecure_protocols",
    )
    SSLV3_ENABLED = SkimsMethodInfo(
        developer="asalgado@fluidattacks.com",
        file_name="analyze_protocol",
        name="sslv3_enabled",
    )
    TLSV1_ENABLED = SkimsMethodInfo(
        developer="asalgado@fluidattacks.com",
        file_name="analyze_protocol",
        name="tlsv1_enabled",
    )
    TLSV1_1_ENABLED = SkimsMethodInfo(
        developer="asalgado@fluidattacks.com",
        file_name="analyze_protocol",
        name="tlsv1_1_enabled",
    )
    TLSV1_2_OR_HIGHER_DISABLED = SkimsMethodInfo(
        developer="asalgado@fluidattacks.com",
        file_name="analyze_protocol",
        name="tlsv1_2_or_higher_disabled",
    )
    FALLBACK_SCSV_DISABLED = SkimsMethodInfo(
        developer="asalgado@fluidattacks.com",
        file_name="analyze_protocol",
        name="fallback_scsv_disabled",
    )
    TLSV1_3_DOWNGRADE = SkimsMethodInfo(
        developer="asalgado@fluidattacks.com",
        file_name="analyze_protocol",
        name="tlsv1_3_downgrade",
    )
    HEARTBLEED_POSSIBLE = SkimsMethodInfo(
        developer="asalgado@fluidattacks.com",
        file_name="analyze_protocol",
        name="heartbleed_possible",
    )
    FREAK_POSSIBLE = SkimsMethodInfo(
        developer="asalgado@fluidattacks.com",
        file_name="analyze_protocol",
        name="freak_possible",
    )
    RACCOON_POSSIBLE = SkimsMethodInfo(
        developer="asalgado@fluidattacks.com",
        file_name="analyze_protocol",
        name="raccoon_possible",
    )
    BREACH_POSSIBLE = SkimsMethodInfo(
        developer="asalgado@fluidattacks.com",
        file_name="analyze_headers",
        name="breach_possible",
    )
    CS_JWT_SIGNED = SkimsMethodInfo(
        developer="jecheverri@fluidattacks.com",
        file_name="c_sharp",
        name="c_sharp_jwt_signed",
    )
    CS_VERIFY_DECODER = SkimsMethodInfo(
        developer="jecheverri@fluidattacks.com",
        file_name="c_sharp",
        name="c_sharp_verify_decoder",
    )
    QUERY_F021 = SkimsMethodInfo(
        developer="drestrepo@fluidattacks.com",
        file_name="query",
        name="query_f021",
    )
    CS_XPATH_INJECTION = SkimsMethodInfo(
        developer="jecheverri@fluidattacks.com",
        file_name="c_sharp",
        name="c_sharp_xpath_injection",
    )
    JAVA_PROP_UNENCRYPTED_TRANSPORT = SkimsMethodInfo(
        developer="drestrepo@fluidattacks.com",
        file_name="java",
        name="java_properties_unencrypted_transport",
    )
    KT_UNENCRYPTED_CHANNEL = SkimsMethodInfo(
        developer="acuberos@fluidattacks.com",
        file_name="kotlin",
        name="kotlin_unencrypted_channel",
    )
    LOCATION = SkimsMethodInfo(
        developer="jecheverri@fluidattacks.com",
        file_name="analyze_headers",
        name="location",
    )
    CFN_ANYONE_ADMIN_PORTS = SkimsMethodInfo(
        developer="acuberos@fluidattacks.com",
        file_name="cloudformation",
        name="cfn_allows_anyone_to_admin_ports",
    )
    AWS_ANYONE_ADMIN_PORTS = SkimsMethodInfo(
        developer="drestrepo@fluidattacks.com",
        file_name="aws",
        name="allows_anyone_to_admin_ports",
    )
    AWS_UNRESTRICTED_CIDRS = SkimsMethodInfo(
        developer="drestrepo@fluidattacks.com",
        file_name="aws",
        name="unrestricted_cidrs",
    )
    AWS_UNRESTRICTED_IP_PROTOCOlS = SkimsMethodInfo(
        developer="drestrepo@fluidattacks.com",
        file_name="aws",
        name="unrestricted_ip_protocols",
    )
    AWS_SEC_GROUPS_RFC1918 = SkimsMethodInfo(
        developer="lsaavedra@fluidattacks.com",
        file_name="aws",
        name="security_groups_ip_ranges_in_rfc1918",
    )
    AWS_UNRESTRICTED_DNS_ACCESS = SkimsMethodInfo(
        developer="lsaavedra@fluidattacks.com",
        file_name="aws",
        name="unrestricted_dns_access",
    )
    AWS_UNRESTRICTED_FTP_ACCESS = SkimsMethodInfo(
        developer="lsaavedra@fluidattacks.com",
        file_name="aws",
        name="unrestricted_ftp_access",
    )
    AWS_OPEN_ALL_PORTS_TO_THE_PUBLIC = SkimsMethodInfo(
        developer="lsaavedra@fluidattacks.com",
        file_name="aws",
        name="open_all_ports_to_the_public",
    )
    AWS_DEFAULT_ALL_TRAFIC = SkimsMethodInfo(
        developer="lsaavedra@fluidattacks.com",
        file_name="aws",
        name="default_seggroup_allows_all_traffic",
    )
    AWS_INSTANCES_WITHOUT_PROFILE = SkimsMethodInfo(
        developer="lsaavedra@fluidattacks.com",
        file_name="aws",
        name="instances_without_profile",
    )
    AWS_INSECURE_PORT_RANGE = SkimsMethodInfo(
        developer="lsaavedra@fluidattacks.com",
        file_name="aws",
        name="insecure_port_range_in_security_group",
    )
    AWS_ADMIN_POLICY_ATTACHED = SkimsMethodInfo(
        developer="lsaavedra@fluidattacks.com",
        file_name="aws",
        name="admin_policy_attached",
    )
    AWS_PUBLIC_BUCKETS = SkimsMethodInfo(
        developer="lsaavedra@fluidattacks.com",
        file_name="aws",
        name="public_buckets",
    )
    AWS_GROUP_WITH_INLINE_POLICY = SkimsMethodInfo(
        developer="lsaavedra@fluidattacks.com",
        file_name="aws",
        name="group_with_inline_policies",
    )
    AWS_USER_WITH_INLINE_POLICY = SkimsMethodInfo(
        developer="lsaavedra@fluidattacks.com",
        file_name="aws",
        name="user_with_inline_policies",
    )
    AWS_OPEN_PASSROLE = SkimsMethodInfo(
        developer="lsaavedra@fluidattacks.com",
        file_name="aws",
        name="open_passrole",
    )
    AWS_PERMISSIVE_POLICY = SkimsMethodInfo(
        developer="lsaavedra@fluidattacks.com",
        file_name="aws",
        name="permissive_policy",
    )
    AWS_FULL_ACCESS_SSM = SkimsMethodInfo(
        developer="lsaavedra@fluidattacks.com",
        file_name="aws",
        name="full_access_to_ssm",
    )
    AWS_NEGATIVE_STATEMENT = SkimsMethodInfo(
        developer="lsaavedra@fluidattacks.com",
        file_name="aws",
        name="negative_statement",
    )
    AWS_INSECURE_PROTOCOLS = SkimsMethodInfo(
        developer="lsaavedra@fluidattacks.com",
        file_name="aws",
        name="serves_content_over_insecure_protocols",
    )
    AWS_INSECURE_SECURITY_POLICY = SkimsMethodInfo(
        developer="lsaavedra@fluidattacks.com",
        file_name="aws",
        name="uses_insecure_security_policy",
    )
    AWS_GROUP_INSECURE_PORT = SkimsMethodInfo(
        developer="lsaavedra@fluidattacks.com",
        file_name="aws",
        name="target_group_insecure_port",
    )
    AWS_HAS_PUBLIC_INSTANCES = SkimsMethodInfo(
        developer="lsaavedra@fluidattacks.com",
        file_name="aws",
        name="has_public_instances",
    )
    AWS_UNENCRYPTED_BUCKETS = SkimsMethodInfo(
        developer="lsaavedra@fluidattacks.com",
        file_name="aws",
        name="unencrypted_buckets",
    )
    AWS_BUCKET_POLICY_ENCRYPTION_DISABLE = SkimsMethodInfo(
        developer="lsaavedra@fluidattacks.com",
        file_name="aws",
        name="bucket_policy_has_server_side_encryption_disable",
    )
    AWS_NOT_INSIDE_A_DB_SUBNET_GROUP = SkimsMethodInfo(
        developer="lsaavedra@fluidattacks.com",
        file_name="aws",
        name="is_not_inside_a_db_subnet_group",
    )
    AWS_DEFAULT_SECURITY_GROUP = SkimsMethodInfo(
        developer="lsaavedra@fluidattacks.com",
        file_name="aws",
        name="use_default_security_group",
    )
    AWS_ACL_PUBLIC_BUCKETS = SkimsMethodInfo(
        developer="lsaavedra@fluidattacks.com",
        file_name="aws",
        name="acl_public_buckets",
    )
    AWS_RDS_HAS_UNENCRYPTED_STORAGE = SkimsMethodInfo(
        developer="lsaavedra@fluidattacks.com",
        file_name="aws",
        name="rds_has_unencrypted_storage",
    )
    AWS_EBS_IS_ENCRYPTION_DISABLED = SkimsMethodInfo(
        developer="lsaavedra@fluidattacks.com",
        file_name="aws",
        name="ebs_is_encryption_disabled",
    )
    CFN_EC2_SEC_GROUPS_RFC1918 = SkimsMethodInfo(
        developer="atrujillo@fluidattacks.com",
        file_name="cloudformation",
        name="cfn_ec2_has_security_groups_ip_ranges_in_rfc1918",
    )
    CFN_EC2_UNRESTRICTED_PORTS = SkimsMethodInfo(
        developer="atrujillo@fluidattacks.com",
        file_name="cloudformation",
        name="cfn_ec2_has_unrestricted_ports",
    )
    CFN_GROUPS_WITHOUT_EGRESS = SkimsMethodInfo(
        developer="atrujillo@fluidattacks.com",
        file_name="cloudformation",
        name="cfn_groups_without_egress",
    )
    CFN_INST_WITHOUT_PROFILE = SkimsMethodInfo(
        developer="acuberos@fluidattacks.com",
        file_name="cloudformation",
        name="cfn_instances_without_profile",
    )
    CFN_UNRESTRICTED_CIDRS = SkimsMethodInfo(
        developer="drestrepo@fluidattacks.com",
        file_name="cloudformation",
        name="cfn_unrestricted_cidrs",
    )
    CFN_UNRESTRICTED_IP_PROTO = SkimsMethodInfo(
        developer="acuberos@fluidattacks.com",
        file_name="cloudformation",
        name="cfn_unrestricted_ip_protocols",
    )
    CFN_EC2_OPEN_ALL_PORTS_PUBLIC = SkimsMethodInfo(
        developer="atrujillo@fluidattacks.com",
        file_name="cloudformation",
        name="cfn_ec2_has_open_all_ports_to_the_public",
    )
    CFN_EC2_UNRESTRICTED_DNS = SkimsMethodInfo(
        developer="atrujillo@fluidattacks.com",
        file_name="cloudformation",
        name="cfn_ec2_has_unrestricted_dns_access",
    )
    CFN_EC2_UNRESTRICTED_FTP = SkimsMethodInfo(
        developer="atrujillo@fluidattacks.com",
        file_name="cloudformation",
        name="cfn_ec2_has_unrestricted_ftp_access",
    )
    TFM_ANYONE_ADMIN_PORTS = SkimsMethodInfo(
        developer="atrujillo@fluidattacks.com",
        file_name="terraform",
        name="tfm_allows_anyone_to_admin_ports",
    )
    TFM_EC2_SEC_GROUPS_RFC1918 = SkimsMethodInfo(
        developer="atrujillo@fluidattacks.com",
        file_name="terraform",
        name="tfm_ec2_has_security_groups_ip_ranges_in_rfc1918",
    )
    TFM_EC2_UNRESTRICTED_DNS = SkimsMethodInfo(
        developer="atrujillo@fluidattacks.com",
        file_name="terraform",
        name="tfm_ec2_has_unrestricted_dns_access",
    )
    TFM_EC2_UNRESTRICTED_FTP = SkimsMethodInfo(
        developer="atrujillo@fluidattacks.com",
        file_name="terraform",
        name="tfm_ec2_has_unrestricted_ftp_access",
    )
    TFM_EC2_OPEN_ALL_PORTS_PUBLIC = SkimsMethodInfo(
        developer="atrujillo@fluidattacks.com",
        file_name="terraform",
        name="tfm_ec2_has_open_all_ports_to_the_public",
    )
    TFM_AWS_EC2_ALL_TRAFFIC = SkimsMethodInfo(
        developer="jecheverri@fluidattacks.com",
        file_name="terraform",
        name="tfm_aws_ec2_allows_all_outbound_traffic",
    )
    TFM_INST_WITHOUT_PROFILE = SkimsMethodInfo(
        developer="atrujillo@fluidattacks.com",
        file_name="terraform",
        name="tfm_ec2_instances_without_profile",
    )
    TFM_AWS_EC2_CFN_UNRESTR_IP_PROT = SkimsMethodInfo(
        developer="jecheverri@fluidattacks.com",
        file_name="terraform",
        name="tfm_aws_ec2_cfn_unrestricted_ip_protocols",
    )
    TFM_AWS_EC2_UNRESTRICTED_CIDRS = SkimsMethodInfo(
        developer="jecheverri@fluidattacks.com",
        file_name="terraform",
        name="tfm_aws_ec2_unrestricted_cidrs",
    )
    TFM_EC2_UNRESTRICTED_PORTS = SkimsMethodInfo(
        developer="atrujillo@fluidattacks.com",
        file_name="terraform",
        name="tfm_ec2_has_unrestricted_ports",
    )
    CFN_ADMIN_POLICY_ATTACHED = SkimsMethodInfo(
        developer="acuberos@fluidattacks.com",
        file_name="cloudformation",
        name="cfn_admin_policy_attached",
    )
    CFN_BUCKET_ALLOWS_PUBLIC = SkimsMethodInfo(
        developer="atrujillo@fluidattacks.com",
        file_name="cloudformation",
        name="cfn_bucket_policy_allows_public_access",
    )
    CFN_IAM_MISSING_SECURITY = SkimsMethodInfo(
        developer="atrujillo@fluidattacks.com",
        file_name="cloudformation",
        name="cfn_iam_user_missing_role_based_security",
    )
    CFN_NEGATIVE_STATEMENT = SkimsMethodInfo(
        developer="acuberos@fluidattacks.com",
        file_name="cloudformation",
        name="cfn_negative_statement",
    )
    CFN_OPEN_PASSROLE = SkimsMethodInfo(
        developer="acuberos@fluidattacks.com",
        file_name="cloudformation",
        name="cfn_open_passrole",
    )
    CFN_PERMISSIVE_POLICY = SkimsMethodInfo(
        developer="acuberos@fluidattacks.com",
        file_name="cloudformation",
        name="cfn_permissive_policy",
    )
    CFN_EC2_NO_IAM = SkimsMethodInfo(
        developer="atrujillo@fluidattacks.com",
        file_name="cloudformation",
        name="cfn_ec2_has_not_an_iam_instance_profile",
    )
    CFN_EC2_ASSOC_PUB_IP = SkimsMethodInfo(
        developer="atrujillo@fluidattacks.com",
        file_name="cloudformation",
        name="cfn_ec2_associate_public_ip_address",
    )
    CFN_EC2_TERMINATE_SHUTDOWN_BEHAVIOR = SkimsMethodInfo(
        developer="atrujillo@fluidattacks.com",
        file_name="cloudformation",
        name="cfn_ec2_has_terminate_shutdown_behavior",
    )
    CFN_IAM_FULL_ACCESS_SSM = SkimsMethodInfo(
        developer="atrujillo@fluidattacks.com",
        file_name="cloudformation",
        name="cfn_iam_has_full_access_to_ssm",
    )
    TFM_ADMIN_POLICY = SkimsMethodInfo(
        developer="acuberos@fluidattacks.com",
        file_name="terraform",
        name="terraform_admin_policy_attached",
    )
    TFM_BUCKET_ALLOWS_PUBLIC = SkimsMethodInfo(
        developer="atrujillo@fluidattacks.com",
        file_name="terraform",
        name="tfm_bucket_policy_allows_public_access",
    )
    TFM_IAM_MISSING_SECURITY = SkimsMethodInfo(
        developer="atrujillo@fluidattacks.com",
        file_name="terraform",
        name="tfm_iam_user_missing_role_based_security",
    )
    TFM_NEGATIVE_STATEMENT = SkimsMethodInfo(
        developer="acuberos@fluidattacks.com",
        file_name="terraform",
        name="terraform_negative_statement",
    )
    TFM_OPEN_PASSROLE = SkimsMethodInfo(
        developer="acuberos@fluidattacks.com",
        file_name="terraform",
        name="terraform_open_passrole",
    )
    TFM_PERMISSIVE_POLICY = SkimsMethodInfo(
        developer="acuberos@fluidattacks.com",
        file_name="terraform",
        name="terraform_permissive_policy",
    )
    TFM_IAM_FULL_ACCESS_SSM = SkimsMethodInfo(
        developer="atrujillo@fluidattacks.com",
        file_name="terraform",
        name="tfm_iam_has_full_access_to_ssm",
    )
    TFM_EC2_NO_IAM = SkimsMethodInfo(
        developer="jecheverri@fluidattacks.com",
        file_name="terraform",
        name="tfm_ec2_has_not_an_iam_instance_profile",
    )
    JS_WEAK_RANDOM = SkimsMethodInfo(
        developer="drestrepo@fluidattacks.com",
        file_name="javascript",
        name="javascript_weak_random",
    )
    QUERY_F034 = SkimsMethodInfo(
        developer="drestrepo@fluidattacks.com",
        file_name="query",
        name="query_f034",
    )
    CS_WEAK_CREDENTIAL = SkimsMethodInfo(
        developer="asalgado@fluidattacks.com",
        file_name="c_sharp",
        name="csharp_weak_credential_policy",
    )
    CS_NO_PASSWORD = SkimsMethodInfo(
        developer="asalgado@fluidattacks.com",
        file_name="c_sharp",
        name="csharp_no_password",
    )
    VIEW_STATE = SkimsMethodInfo(
        developer="machine@fluidattacks.com",
        file_name="analyze_content",
        name="view_state",
    )
    CHECK_DNS_RECORDS = SkimsMethodInfo(
        developer="ugomez@fluidattacks.com",
        file_name="analyze_dns",
        name="check_dns_records",
    )
    DOTNETCONFIG_NOT_SUPPRESS_VULN_HEADER = SkimsMethodInfo(
        developer="lsaavedra@fluidattacks.com",
        file_name="dotnetconfig",
        name="dotnetconfig_not_suppress_vuln_header",
    )
    DOTNETCONFIG_HAS_SSL_DISABLED = SkimsMethodInfo(
        developer="lsaavedra@fluidattacks.com",
        file_name="dotnetconfig",
        name="dotnetconfig_has_ssl_disabled",
    )
    DOTNETCONFIG_HAS_DEBUG_ENABLED = SkimsMethodInfo(
        developer="lsaavedra@fluidattacks.com",
        file_name="dotnetconfig",
        name="dotnetconfig_has_debug_enabled",
    )
    DOTNETCONFIG_NOT_CUSTOM_ERRORS = SkimsMethodInfo(
        developer="lsaavedra@fluidattacks.com",
        file_name="dotnetconfig",
        name="dotnetconfig_not_custom_errors",
    )
    CS_INSEC_COOKIES = SkimsMethodInfo(
        developer="jecheverri@fluidattacks.com",
        file_name="c_sharp",
        name="csharp_insecurely_generated_cookies",
    )
    QUERY_F042 = SkimsMethodInfo(
        developer="drestrepo@fluidattacks.com",
        file_name="query",
        name="query_f042",
    )
    CONTENT_SECURITY_POLICY = SkimsMethodInfo(
        developer="machine@fluidattacks.com",
        file_name="analyze_headers",
        name="content_security_policy",
    )
    UPGRADE_INSEC_REQ = SkimsMethodInfo(
        developer="asalgado@fluidattacks.com",
        file_name="analyze_headers",
        name="upgrade_insecure_requests",
    )
    NO_OBFUSCATION = SkimsMethodInfo(
        developer="lsaavedra@fluidattacks.com",
        file_name="analyze_bytecodes",
        name="no_obfuscation",
    )
    NO_ROOT_CHECK = SkimsMethodInfo(
        developer="machine@fluidattacks.com",
        file_name="analyze_bytecodes",
        name="no_root_check",
    )
    JAVA_PROP_MISSING_SSL = SkimsMethodInfo(
        developer="machine@fluidattacks.com",
        file_name="java",
        name="java_properties_missing_ssl",
    )
    JAVA_PROP_WEAK_CIPHER = SkimsMethodInfo(
        developer="machine@fluidattacks.com",
        file_name="java",
        name="java_properties_weak_cipher_suite",
    )
    CS_INSECURE_HASH = SkimsMethodInfo(
        developer="drestrepo@fluidattacks.com",
        file_name="c_sharp",
        name="c_sharp_insecure_hash",
    )
    CS_INSECURE_CIPHER = SkimsMethodInfo(
        developer="drestrepo@fluidattacks.com",
        file_name="c_sharp",
        name="c_sharp_insecure_cipher",
    )
    CS_MANAGED_SECURE_MODE = SkimsMethodInfo(
        developer="jecheverri@fluidattacks.com",
        file_name="c_sharp",
        name="c_sharp_managed_secure_mode",
    )
    CS_RSA_SECURE_MODE = SkimsMethodInfo(
        developer="jecheverri@fluidattacks.com",
        file_name="c_sharp",
        name="c_sharp_rsa_secure_mode",
    )
    CS_INSECURE_KEYS = SkimsMethodInfo(
        developer="jecheverri@fluidattacks.com",
        file_name="c_sharp",
        name="c_sharp_insecure_keys",
    )
    CS_DISABLED_STRONG_CRYPTO = SkimsMethodInfo(
        developer="jecheverri@fluidattacks.com",
        file_name="c_sharp",
        name="c_sharp_disabled_strong_crypto",
    )
    CS_OBSOLETE_KEY_DERIVATION = SkimsMethodInfo(
        developer="jecheverri@fluidattacks.com",
        file_name="c_sharp",
        name="c_sharp_obsolete_key_derivation",
    )
    GO_INSECURE_CIPHER = SkimsMethodInfo(
        developer="jecheverri@fluidattacks.com",
        file_name="go",
        name="go_insecure_cipher",
    )
    GO_INSECURE_HASH = SkimsMethodInfo(
        developer="jecheverri@fluidattacks.com",
        file_name="go",
        name="go_insecure_hash",
    )
    JAVA_INSECURE_CIPHER = SkimsMethodInfo(
        developer="drestrepo@fluidattacks.com",
        file_name="java",
        name="java_insecure_cipher",
    )
    JAVA_INSECURE_HASH = SkimsMethodInfo(
        developer="drestrepo@fluidattacks.com",
        file_name="java",
        name="java_insecure_hash",
    )
    JAVA_INSECURE_KEY = SkimsMethodInfo(
        developer="drestrepo@fluidattacks.com",
        file_name="java",
        name="java_insecure_key",
    )
    JAVA_INSECURE_PASS = SkimsMethodInfo(
        developer="drestrepo@fluidattacks.com",
        file_name="java",
        name="java_insecure_pass",
    )
    JS_INSECURE_CIPHER = SkimsMethodInfo(
        developer="drestrepo@fluidattacks.com",
        file_name="javascript",
        name="javascript_insecure_cipher",
    )
    JS_INSECURE_KEY = SkimsMethodInfo(
        developer="drestrepo@fluidattacks.com",
        file_name="javascript",
        name="javascript_insecure_key",
    )
    JS_INSECURE_HASH = SkimsMethodInfo(
        developer="drestrepo@fluidattacks.com",
        file_name="javascript",
        name="javascript_insecure_hash",
    )
    KT_INSECURE_CIPHER = SkimsMethodInfo(
        developer="drestrepo@fluidattacks.com",
        file_name="kotlin",
        name="kotlin_insecure_cipher",
    )
    KT_INSECURE_HASH = SkimsMethodInfo(
        developer="drestrepo@fluidattacks.com",
        file_name="kotlin",
        name="kotlin_insecure_hash",
    )
    KT_INSECURE_KEY = SkimsMethodInfo(
        developer="drestrepo@fluidattacks.com",
        file_name="kotlin",
        name="kotlin_insecure_key",
    )
    QUERY_F052 = SkimsMethodInfo(
        developer="drestrepo@fluidattacks.com",
        file_name="query",
        name="query_f052",
    )
    WEAK_CIPHERS_ALLOWED = SkimsMethodInfo(
        developer="asalgado@fluidattacks.com",
        file_name="analyze_protocol",
        name="weak_ciphers_allowed",
    )
    APK_BACKUPS_ENABLED = SkimsMethodInfo(
        developer="bagudelo@fluidattacks.com",
        file_name="analyze_bytecodes",
        name="apk_backups_enabled",
    )
    PATH_APK_BACKUPS_ENABLED = SkimsMethodInfo(
        developer="bagudelo@fluidattacks.com",
        file_name="android",
        name="apk_backups_enabled",
    )
    JSON_ANON_CONNECTION_CONFIG = SkimsMethodInfo(
        developer="jecheverri@fluidattacks.com",
        file_name="conf_files",
        name="json_anon_connection_config",
    )
    APK_DEBUGGING_ENABLED = SkimsMethodInfo(
        developer="bagudelo@fluidattacks.com",
        file_name="analyze_bytecodes",
        name="apk_debugging_enabled",
    )
    PATH_APK_DEBUGGING_ENABLED = SkimsMethodInfo(
        developer="bagudelo@fluidattacks.com",
        file_name="android",
        name="apk_debugging_enabled",
    )
    NOT_VERIFIES_SSL_HOSTNAME = SkimsMethodInfo(
        developer="lsaavedra@fluidattacks.com",
        file_name="analyze_bytecodes",
        name="not_verifies_ssl_hostname",
    )
    JSON_ALLOWED_HOSTS = SkimsMethodInfo(
        developer="jecheverri@fluidattacks.com",
        file_name="conf_files",
        name="json_allowed_hosts",
    )
    QUERY_F063 = SkimsMethodInfo(
        developer="drestrepo@fluidattacks.com",
        file_name="query",
        name="query_f063",
    )
    CS_OPEN_REDIRECT = SkimsMethodInfo(
        developer="jecheverri@fluidattacks.com",
        file_name="c_sharp",
        name="c_sharp_open_redirect",
    )
    DATE = SkimsMethodInfo(
        developer="acuberos@fluidattacks.com",
        file_name="analyze_headers",
        name="date",
    )
    HTML_IS_CACHEABLE = SkimsMethodInfo(
        developer="lsaavedra@fluidattacks.com",
        file_name="html",
        name="html_is_cacheable",
    )
    HTML_HAS_AUTOCOMPLETE = SkimsMethodInfo(
        developer="lsaavedra@fluidattacks.com",
        file_name="html",
        name="html_has_autocomplete",
    )
    CS_HAS_CONSOLE_FUNCTIONS = SkimsMethodInfo(
        developer="jecheverri@fluidattacks.com",
        file_name="c_sharp",
        name="c_sharp_has_console_functions",
    )
    JS_USES_CONSOLE_LOG = SkimsMethodInfo(
        developer="lsaavedra@fluidattacks.com",
        file_name="javascript",
        name="js_uses_console_log",
    )
    CFN_ELB2_INSECURE_SEC_POLICY = SkimsMethodInfo(
        developer="atrujillo@fluidattacks.com",
        file_name="cloudformation",
        name="cfn_elb2_uses_insecure_security_policy",
    )
    CFN_LB_TARGET_INSECURE_PORT = SkimsMethodInfo(
        developer="atrujillo@fluidattacks.com",
        file_name="cloudformation",
        name="cfn_lb_target_group_insecure_port",
    )
    TFM_LB_TARGET_INSECURE_PORT = SkimsMethodInfo(
        developer="jecheverri@fluidattacks.com",
        file_name="terraform",
        name="tfm_lb_target_group_insecure_port",
    )
    TFM_ELB2_INSECURE_SEC_POLICY = SkimsMethodInfo(
        developer="atrujillo@fluidattacks.com",
        file_name="terraform",
        name="tfm_elb2_uses_insecure_security_policy",
    )
    REFERRER_POLICY = SkimsMethodInfo(
        developer="machine@fluidattacks.com",
        file_name="analyze_headers",
        name="referrer_policy",
    )
    CFN_RDS_PUB_ACCESSIBLE = SkimsMethodInfo(
        developer="atrujillo@fluidattacks.com",
        file_name="cloudformation",
        name="cfn_rds_is_publicly_accessible",
    )
    TFM_DB_CLUSTER_PUB_ACCESS = SkimsMethodInfo(
        developer="jecheverri@fluidattacks.com",
        file_name="terraform",
        name="tfm_db_cluster_publicly_accessible",
    )
    TFM_DB_PUB_ACCESS = SkimsMethodInfo(
        developer="jecheverri@fluidattacks.com",
        file_name="terraform",
        name="tfm_db_instance_publicly_accessible",
    )
    APK_EXPORTED_CP = SkimsMethodInfo(
        developer="bagudelo@fluidattacks.com",
        file_name="analyze_bytecodes",
        name="apk_exported_cp",
    )
    PATH_APK_EXPORTED_CP = SkimsMethodInfo(
        developer="bagudelo@fluidattacks.com",
        file_name="android",
        name="apk_exported_cp",
    )
    NON_UPGRADEABLE_DEPS = SkimsMethodInfo(
        developer="machine@fluidattacks.com",
        file_name="generic",
        name="non_upgradeable_deps",
    )
    PIP_INCOMPLETE_DEPENDENCIES_LIST = SkimsMethodInfo(
        developer="lsaavedra@fluidattacks.com",
        file_name="python",
        name="pip_incomplete_dependencies_list",
    )
    USES_INSECURE_DELETE = SkimsMethodInfo(
        developer="lsaavedra@fluidattacks.com",
        file_name="analyze_bytecodes",
        name="uses_insecure_delete",
    )
    SOCKET_GET_INSECURE = SkimsMethodInfo(
        developer="lsaavedra@fluidattacks.com",
        file_name="analyze_bytecodes",
        name="socket_uses_get_insecure",
    )
    JS_CLIENT_STORAGE = SkimsMethodInfo(
        developer="drestrepo@fluidattacks.com",
        file_name="javascript",
        name="javascript_client_storage",
    )
    HTML_HAS_NOT_SUB_RESOURCE_INTEGRITY = SkimsMethodInfo(
        developer="lsaavedra@fluidattacks.com",
        file_name="html",
        name="html_has_not_sub_resource_integrity",
    )
    SUB_RESOURCE_INTEGRITY = SkimsMethodInfo(
        developer="machine@fluidattacks.com",
        file_name="analyze_content",
        name="sub_resource_integrity",
    )
    QUERY_F089 = SkimsMethodInfo(
        developer="drestrepo@fluidattacks.com",
        file_name="query",
        name="query_f089",
    )
    CS_INSECURE_LOGGING = SkimsMethodInfo(
        developer="jecheverri@fluidattacks.com",
        file_name="c_sharp",
        name="c_sharp_insecure_logging",
    )
    CBC_ENABLED = SkimsMethodInfo(
        developer="asalgado@fluidattacks.com",
        file_name="analyze_protocol",
        name="cbc_enabled",
    )
    CS_INSECURE_DESERIAL = SkimsMethodInfo(
        developer="jecheverri@fluidattacks.com",
        file_name="c_sharp",
        name="c_sharp_insecure_deserialization",
    )
    CS_XML_SERIAL = SkimsMethodInfo(
        developer="jecheverri@fluidattacks.com",
        file_name="c_sharp",
        name="c_sharp_check_xml_serializer",
    )
    CS_JS_DESERIALIZATION = SkimsMethodInfo(
        developer="jecheverri@fluidattacks.com",
        file_name="c_sharp",
        name="c_sharp_js_deserialization",
    )
    CS_TYPE_NAME_HANDLING = SkimsMethodInfo(
        developer="jecheverri@fluidattacks.com",
        file_name="c_sharp",
        name="c_sharp_type_name_handling",
    )
    HTML_HAS_REVERSE_TABNABBING = SkimsMethodInfo(
        developer="lsaavedra@fluidattacks.com",
        file_name="html",
        name="html_has_reverse_tabnabbing",
    )
    CS_PATH_INJECTION = SkimsMethodInfo(
        developer="jecheverri@fluidattacks.com",
        file_name="c_sharp",
        name="c_sharp_path_injection",
    )
    CFN_POLICY_SERVER_ENCRYP_DISABLED = SkimsMethodInfo(
        developer="atrujillo@fluidattacks.com",
        file_name="cloudformation",
        name="cfn_bucket_policy_has_server_side_encryption_disabled",
    )
    CFN_UNENCRYPTED_BUCKETS = SkimsMethodInfo(
        developer="atrujillo@fluidattacks.com",
        file_name="cloudformation",
        name="cfn_unencrypted_buckets",
    )
    TFM_UNENCRYPTED_BUCKETS = SkimsMethodInfo(
        developer="atrujillo@fluidattacks.com",
        file_name="terraform",
        name="tfm_unencrypted_buckets",
    )
    CS_INSEC_CREATE = SkimsMethodInfo(
        developer="jecheverri@fluidattacks.com",
        file_name="c_sharp",
        name="c_sharp_insec_create",
    )
    APK_UNSIGNED = SkimsMethodInfo(
        developer="machine@fluidattacks.com",
        file_name="analyze_bytecodes",
        name="apk_unsigned",
    )
    QUERY_F107 = SkimsMethodInfo(
        developer="drestrepo@fluidattacks.com",
        file_name="query",
        name="query_f107",
    )
    CS_LDAP_INJECTION = SkimsMethodInfo(
        developer="jecheverri@fluidattacks.com",
        file_name="c_sharp",
        name="c_sharp_ldap_injection",
    )
    JAVA_LDAP_INJECTION = SkimsMethodInfo(
        developer="machine@fluidattacks.com",
        file_name="java",
        name="java_ldap_injection",
    )
    CFN_RDS_NOT_INSIDE_DB_SUBNET = SkimsMethodInfo(
        developer="atrujillo@fluidattacks.com",
        file_name="cloudformation",
        name="cfn_rds_is_not_inside_a_db_subnet_group",
    )
    CFN_EC2_DEFAULT_SEC_GROUP = SkimsMethodInfo(
        developer="atrujillo@fluidattacks.com",
        file_name="cloudformation",
        name="cfn_ec2_use_default_security_group",
    )
    TFM_DB_INSIDE_SUBNET = SkimsMethodInfo(
        developer="jecheverri@fluidattacks.com",
        file_name="terraform",
        name="tfm_db_cluster_inside_subnet",
    )
    TFM_RDS_INSIDE_SUBNET = SkimsMethodInfo(
        developer="jecheverri@fluidattacks.com",
        file_name="terraform",
        name="tfm_rds_instance_inside_subnet",
    )
    QUERY_F112 = SkimsMethodInfo(
        developer="drestrepo@fluidattacks.com",
        file_name="query",
        name="query_f112",
    )
    UNVERIFIABLE_FILES = SkimsMethodInfo(
        developer="machine@fluidattacks.com",
        file_name="generic",
        name="unverifiable_files",
    )
    QUERY_F127 = SkimsMethodInfo(
        developer="drestrepo@fluidattacks.com",
        file_name="query",
        name="query_f127",
    )
    SET_COOKIE_HTTPONLY = SkimsMethodInfo(
        developer="asalgado@fluidattacks.com",
        file_name="analyze_headers",
        name="set_cookie_httponly",
    )
    SET_COOKIE_SAMESITE = SkimsMethodInfo(
        developer="asalgado@fluidattacks.com",
        file_name="analyze_headers",
        name="set_cookie_samesite",
    )
    SET_COOKIE_SECURE = SkimsMethodInfo(
        developer="asalgado@fluidattacks.com",
        file_name="analyze_headers",
        name="set_cookie_secure",
    )
    STRICT_TRANSPORT_SECURITY = SkimsMethodInfo(
        developer="machine@fluidattacks.com",
        file_name="analyze_headers",
        name="strict_transport_security",
    )
    CHECK_DEFAULT_USEHSTS = SkimsMethodInfo(
        developer="jecheverri@fluidattacks.com",
        file_name="c_sharp",
        name="check_default_usehsts",
    )
    X_CONTENT_TYPE_OPTIONS = SkimsMethodInfo(
        developer="machine@fluidattacks.com",
        file_name="analyze_headers",
        name="x_content_type_options",
    )
    PFS_DISABLED = SkimsMethodInfo(
        developer="asalgado@fluidattacks.com",
        file_name="analyze_protocol",
        name="pfs_disabled",
    )
    CS_INSECURE_CORS = SkimsMethodInfo(
        developer="jecheverri@fluidattacks.com",
        file_name="c_sharp",
        name="csharp_insecure_cors",
    )
    CS_INSECURE_CORS_ORIGIN = SkimsMethodInfo(
        developer="jecheverri@fluidattacks.com",
        file_name="c_sharp",
        name="csharp_insecure_cors_origin",
    )
    JS_USES_EVAL = SkimsMethodInfo(
        developer="lsaavedra@fluidattacks.com",
        file_name="javascript",
        name="js_uses_eval",
    )
    TFM_AZURE_UNRESTRICTED_ACCESS = SkimsMethodInfo(
        developer="jecheverri@fluidattacks.com",
        file_name="terraform",
        name="tfm_azure_unrestricted_access_network_segments",
    )
    TFM_AZURE_SA_DEFAULT_ACCESS = SkimsMethodInfo(
        developer="jecheverri@fluidattacks.com",
        file_name="terraform",
        name="tfm_azure_sa_default_network_access",
    )
    TFM_AZURE_KV_DEFAULT_ACCESS = SkimsMethodInfo(
        developer="jecheverri@fluidattacks.com",
        file_name="terraform",
        name="tfm_azure_kv_default_network_access",
    )
    TFM_AZURE_KV_DANGER_BYPASS = SkimsMethodInfo(
        developer="jecheverri@fluidattacks.com",
        file_name="terraform",
        name="tfm_azure_kv_danger_bypass",
    )
    TFM_AWS_ACL_BROAD_NETWORK_ACCESS = SkimsMethodInfo(
        developer="jecheverri@fluidattacks.com",
        file_name="terraform",
        name="tfm_aws_acl_broad_network_access",
    )
    CS_CREATE_TEMP_FILE = SkimsMethodInfo(
        developer="jecheverri@fluidattacks.com",
        file_name="c_sharp",
        name="c_sharp_file_create_temp_file",
    )
    JAVA_CREATE_TEMP_FILE = SkimsMethodInfo(
        developer="drestrepo@fluidattacks.com",
        file_name="java",
        name="java_file_create_temp_file",
    )
    CONTAINER_USING_SSHPASS = SkimsMethodInfo(
        developer="jecheverri@fluidattacks.com",
        file_name="docker",
        name="container_using_sshpass",
    )
    BASH_USING_SSHPASS = SkimsMethodInfo(
        developer="jecheverri@fluidattacks.com",
        file_name="bash",
        name="bash_using_sshpass",
    )
    EC2_DEFAULT_SEC_GROUP = SkimsMethodInfo(
        developer="jecheverri@fluidattacks.com",
        file_name="terraform",
        name="ec2_use_default_security_group",
    )
    CFN_PUBLIC_BUCKETS = SkimsMethodInfo(
        developer="acuberos@fluidattacks.com",
        file_name="cloudformation",
        name="cfn_public_buckets",
    )
    TFM_PUBLIC_BUCKETS = SkimsMethodInfo(
        developer="atrujillo@fluidattacks.com",
        file_name="terraform",
        name="tfm_public_buckets",
    )
    HAS_FRIDA = SkimsMethodInfo(
        developer="lsaavedra@fluidattacks.com",
        file_name="analyze_bytecodes",
        name="has_frida",
    )
    NO_CERTS_PINNING = SkimsMethodInfo(
        developer="machine@fluidattacks.com",
        file_name="analyze_bytecodes",
        name="no_certs_pinning",
    )
    CS_VULN_REGEX = SkimsMethodInfo(
        developer="jecheverri@fluidattacks.com",
        file_name="c_sharp",
        name="csharp_vuln_regular_expression",
    )
    CS_REGEX_INJETCION = SkimsMethodInfo(
        developer="jecheverri@fluidattacks.com",
        file_name="csharp",
        name="csharp_regex_injection",
    )
    JAVA_LEAK_STACKTRACE = SkimsMethodInfo(
        developer="jecheverri@fluidattacks.com",
        file_name="java",
        name="java_info_leak_stacktrace",
    )
    JAVA_INSECURE_LOGGING = SkimsMethodInfo(
        developer="lsaavedra@fluidattacks.com",
        file_name="java",
        name="java_insecure_logging",
    )
    TSCONFIG_SOURCEMAP_ENABLED = SkimsMethodInfo(
        developer="jecheverri@fluidattacks.com",
        file_name="tsconfig",
        name="tsconfig_sourcemap_enabled",
    )
    CS_INFO_LEAK_ERRORS = SkimsMethodInfo(
        developer="jecheverri@fluidattacks.com",
        file_name="csharp",
        name="csharp_info_leak_errors",
    )
    CFN_RDS_UNENCRYPTED_STORAGE = SkimsMethodInfo(
        developer="atrujillo@fluidattacks.com",
        file_name="cloudformation",
        name="cfn_rds_has_unencrypted_storage",
    )
    TFM_RDS_UNENCRYPTED_STORAGE = SkimsMethodInfo(
        developer="jecheverri@fluidattacks.com",
        file_name="terraform",
        name="tfm_rds_has_unencrypted_storage",
    )
    TFM_DB_UNENCRYPTED_STORAGE = SkimsMethodInfo(
        developer="jecheverri@fluidattacks.com",
        file_name="terraform",
        name="tfm_db_has_unencrypted_storage",
    )
    TFM_EBS_UNENCRYPTED_VOLUMES = SkimsMethodInfo(
        developer="jecheverri@fluidattacks.com",
        file_name="terraform",
        name="tfm_ebs_unencrypted_volumes",
    )
    TFM_EC2_UNENCRYPTED_BLOCK_DEVICES = SkimsMethodInfo(
        developer="jecheverri@fluidattacks.com",
        file_name="terraform",
        name="tfm_ec2_instance_unencrypted_ebs_block_devices",
    )
    TFM_EBS_UNENCRYPTED_DEFAULT = SkimsMethodInfo(
        developer="jecheverri@fluidattacks.com",
        file_name="terraform",
        name="tfm_ebs_unencrypted_by_default",
    )
    TFM_ELB2_NOT_DELETION_PROTEC = SkimsMethodInfo(
        developer="atrujillo@fluidattacks.com",
        file_name="terraform",
        name="tfm_elb2_has_not_deletion_protection",
    )
    CFN_EC2_UNENCRYPTED_VOLUMES = SkimsMethodInfo(
        developer="atrujillo@fluidattacks.com",
        file_name="cloudformation",
        name="cfn_ec2_has_unencrypted_volumes",
    )
    CFN_EC2_UNENCRYPTED_BLOCK_DEVICES = SkimsMethodInfo(
        developer="atrujillo@fluidattacks.com",
        file_name="cloudformation",
        name="cfn_ec2_instance_unencrypted_ebs_block_devices",
    )
    CFN_S3_VERSIONING_DISABLED = SkimsMethodInfo(
        developer="atrujillo@fluidattacks.com",
        file_name="cloudformation",
        name="cfn_s3_bucket_versioning_disabled",
    )
    CFN_RDS_NOT_AUTO_BACKUPS = SkimsMethodInfo(
        developer="atrujillo@fluidattacks.com",
        file_name="cloudformation",
        name="cfn_rds_has_not_automated_backups",
    )
    CFN_RDS_NOT_TERMINATION_PROTEC = SkimsMethodInfo(
        developer="atrujillo@fluidattacks.com",
        file_name="cloudformation",
        name="cfn_rds_has_not_termination_protection",
    )
    TFM_DB_NO_DELETION_PROTEC = SkimsMethodInfo(
        developer="jecheverri@fluidattacks.com",
        file_name="terraform",
        name="tfm_db_no_deletion_protection",
    )
    TFM_RDS_NO_DELETION_PROTEC = SkimsMethodInfo(
        developer="jecheverri@fluidattacks.com",
        file_name="terraform",
        name="tfm_rds_no_deletion_protection",
    )
    TFM_DB_NOT_AUTO_BACKUPS = SkimsMethodInfo(
        developer="jecheverri@fluidattacks.com",
        file_name="terraform",
        name="tfm_db_has_not_automated_backups",
    )
    TFM_RDS_NOT_AUTO_BACKUPS = SkimsMethodInfo(
        developer="jecheverri@fluidattacks.com",
        file_name="terraform",
        name="tfm_rds_has_not_automated_backups",
    )
    CFN_EC2_NOT_TERMINATION_PROTEC = SkimsMethodInfo(
        developer="atrujillo@fluidattacks.com",
        file_name="cloudformation",
        name="cfn_ec2_has_not_termination_protection",
    )
    EC2_NOT_TERMINATION_PROTEC = SkimsMethodInfo(
        developer="jecheverri@fluidattacks.com",
        file_name="terraform",
        name="ec2_has_not_termination_protection",
    )
    CFN_ELB2_NOT_DELETION_PROTEC = SkimsMethodInfo(
        developer="atrujillo@fluidattacks.com",
        file_name="cloudformation",
        name="cfn_elb2_has_not_deletion_protection",
    )
    CFN_NOT_POINT_TIME_RECOVERY = SkimsMethodInfo(
        developer="atrujillo@fluidattacks.com",
        file_name="cloudformation",
        name="cfn_has_not_point_in_time_recovery",
    )
    TFM_DB_NO_POINT_TIME_RECOVERY = SkimsMethodInfo(
        developer="jecheverri@fluidattacks.com",
        file_name="terraform",
        name="tfm_db_no_point_in_time_recovery",
    )
    CONTAINER_WITHOUT_USER = SkimsMethodInfo(
        developer="jecheverri@fluidattacks.com",
        file_name="docker",
        name="container_without_user",
    )
    DOCKER_COMPOSE_WITHOUT_USER = SkimsMethodInfo(
        developer="jecheverri@fluidattacks.com",
        file_name="docker",
        name="docker_compose_without_user",
    )
    K8S_CHECK_ADD_CAPABILITY = SkimsMethodInfo(
        developer="jecheverri@fluidattacks.com",
        file_name="kubernetes",
        name="k8s_check_add_capability",
    )
    K8S_PRIVILEGE_ESCALATION_ENABLED = SkimsMethodInfo(
        developer="jecheverri@fluidattacks.com",
        file_name="kubernetes",
        name="k8s_allow_privilege_escalation_enabled",
    )
    K8S_ROOT_CONTAINER = SkimsMethodInfo(
        developer="jecheverri@fluidattacks.com",
        file_name="kubernetes",
        name="k8s_root_container",
    )
    K8S_ROOT_FILESYSTEM_READ_ONLY = SkimsMethodInfo(
        developer="jecheverri@fluidattacks.com",
        file_name="kubernetes",
        name="k8s_root_filesystem_read_only",
    )
    K8S_CHECK_RUN_AS_USER = SkimsMethodInfo(
        developer="jecheverri@fluidattacks.com",
        file_name="kubernetes",
        name="k8s_check_run_as_user",
    )
    K8S_CHECK_SECCOMP_PROFILE = SkimsMethodInfo(
        developer="jecheverri@fluidattacks.com",
        file_name="kubernetes",
        name="k8s_check_seccomp_profile",
    )
    K8S_CHECK_PRIVILEGED_USED = SkimsMethodInfo(
        developer="jecheverri@fluidattacks.com",
        file_name="kubernetes",
        name="k8s_check_privileged_used",
    )
    K8S_CHECK_DROP_CAPABILITY = SkimsMethodInfo(
        developer="jecheverri@fluidattacks.com",
        file_name="kubernetes",
        name="k8s_check_drop_capability",
    )
    CFN_BUCKET_POLICY_SEC_TRANSPORT = SkimsMethodInfo(
        developer="atrujillo@fluidattacks.com",
        file_name="cloudformation",
        name="cfn_bucket_policy_has_secure_transport",
    )
    TFM_AZURE_APP_AUTH_OFF = SkimsMethodInfo(
        developer="jecheverri@fluidattacks.com",
        file_name="terraform",
        name="tfm_azure_app_authentication_off",
    )
    TFM_AZURE_CLIENT_CERT_ENABLED = SkimsMethodInfo(
        developer="jecheverri@fluidattacks.com",
        file_name="terraform",
        name="tfm_azure_as_client_certificates_enabled",
    )
    IMPROPER_CERTIFICATE_VALIDATION = SkimsMethodInfo(
        developer="lsaavedra@fluidattacks.com",
        file_name="analyze_bytecodes",
        name="improper_certificate_validation",
    )
    CS_LDAP_CONN_AUTH = SkimsMethodInfo(
        developer="jecheverri@fluidattacks.com",
        file_name="c_sharp",
        name="csharp_ldap_connections_authenticated",
    )
    QUERY_F320 = SkimsMethodInfo(
        developer="drestrepo@fluidattacks.com",
        file_name="query",
        name="query_f320",
    )
    CFN_KMS_MASTER_KEYS_EXPOSED = SkimsMethodInfo(
        developer="atrujillo@fluidattacks.com",
        file_name="cloudformation",
        name="cfn_kms_key_has_master_keys_exposed_to_everyone",
    )
    CFN_IAM_WILDCARD_WRITE = SkimsMethodInfo(
        developer="atrujillo@fluidattacks.com",
        file_name="cloudformation",
        name="cfn_iam_has_wildcard_resource_on_write_action",
    )
    CFN_IAM_POLICY_MISS_CONFIG = SkimsMethodInfo(
        developer="atrujillo@fluidattacks.com",
        file_name="cloudformation",
        name="cfn_iam_is_policy_miss_configured",
    )
    CFN_IAM_PRIVILEGES_OVER_IAM = SkimsMethodInfo(
        developer="atrujillo@fluidattacks.com",
        file_name="cloudformation",
        name="cfn_iam_has_privileges_over_iam",
    )
    TFM_IAM_WILDCARD_WRITE = SkimsMethodInfo(
        developer="atrujillo@fluidattacks.com",
        file_name="terraform",
        name="tfm_iam_has_wildcard_resource_on_write_action",
    )
    TFM_KMS_MASTER_KEYS_EXPOSED = SkimsMethodInfo(
        developer="atrujillo@fluidattacks.com",
        file_name="terraform",
        name="tfm_kms_key_has_master_keys_exposed_to_everyone",
    )
    TFM_BUCKET_POLICY_SEC_TRANSPORT = SkimsMethodInfo(
        developer="atrujillo@fluidattacks.com",
        file_name="terraform",
        name="tfm_bucket_policy_has_secure_transport",
    )
    TFM_IAM_ROLE_OVER_PRIVILEGED = SkimsMethodInfo(
        developer="atrujillo@fluidattacks.com",
        file_name="terraform",
        name="tfm_iam_role_is_over_privileged",
    )
    CFN_IAM_ROLE_OVER_PRIVILEGED = SkimsMethodInfo(
        developer="atrujillo@fluidattacks.com",
        file_name="cloudformation",
        name="cfn_iam_is_role_over_privileged",
    )
    WEBVIEW_VULNS = SkimsMethodInfo(
        developer="lsaavedra@fluidattacks.com",
        file_name="analyze_bytecodes",
        name="webview_vulnerabilities",
    )
    EC2_TERMINATE_SHUTDOWN_BEHAVIOR = SkimsMethodInfo(
        developer="atrujillo@fluidattacks.com",
        file_name="terraform",
        name="tfm_ec2_has_terminate_shutdown_behavior",
    )
    JAVA_CSRF_PROTECTIONS_DISABLED = SkimsMethodInfo(
        developer="jecheverri@fluidattacks.com",
        file_name="java",
        name="csrf_protections_disabled",
    )
    KUBERNETES_INSECURE_PORT = SkimsMethodInfo(
        developer="jecheverri@fluidattacks.com",
        file_name="kubernetes",
        name="kubernetes_insecure_port",
    )
    TFM_EC2_ASSOC_PUB_IP = SkimsMethodInfo(
        developer="jecheverri@fluidattacks.com",
        file_name="terraform",
        name="tfm_ec2_associate_public_ip_address",
    )
    TFM_AWS_S3_VERSIONING_DISABLED = SkimsMethodInfo(
        developer="jecheverri@fluidattacks.com",
        file_name="terraform",
        name="tfm_aws_s3_versioning_disabled",
    )
    TFM_CTRAIL_LOG_NOT_VALIDATED = SkimsMethodInfo(
        developer="atrujillo@fluidattacks.com",
        file_name="terraform",
        name="tfm_aws_s3_versioning_disabled",
    )
    TFM_KMS_KEY_ROTATION_DISABLED = SkimsMethodInfo(
        developer="atrujillo@fluidattacks.com",
        file_name="terraform",
        name="tfm_kms_key_is_key_rotation_absent_or_disabled",
    )
    CS_CHECK_HASHES_SALT = SkimsMethodInfo(
        developer="jecheverri@fluidattacks.com",
        file_name="c_sharp",
        name="csharp_check_hashes_salt",
    )
    DANGEROUS_PERMISSIONS = SkimsMethodInfo(
        developer="lsaavedra@fluidattacks.com",
        file_name="android",
        name="has_dangerous_permissions",
    )
    CFN_INSEC_GEN_SECRET = SkimsMethodInfo(
        developer="atrujillo@fluidattacks.com",
        file_name="cloudformation",
        name="cfn_insecure_generate_secret_string",
    )
    CS_CONFLICTING_ANNOTATIONS = SkimsMethodInfo(
        developer="jecheverri@fluidattacks.com",
        file_name="c_sharp",
        name="csharp_conflicting_annotations",
    )
    JAVA_HOST_KEY_CHECKING = SkimsMethodInfo(
        developer="machine@fluidattacks.com",
        file_name="java",
        name="java_host_key_checking",
    )
    HTML_IS_HEADER_CONTENT_TYPE_MISSING = SkimsMethodInfo(
        developer="lsaavedra@fluidattacks.com",
        file_name="html",
        name="html_is_header_content_type_missing",
    )
    CFN_CONTENT_HTTP = SkimsMethodInfo(
        developer="acuberos@fluidattacks.com",
        file_name="cloudformation",
        name="cfn_serves_content_over_http",
    )
    CFN_ELB2_INSEC_PROTO = SkimsMethodInfo(
        developer="acuberos@fluidattacks.com",
        file_name="cloudformation",
        name="cfn_elb2_uses_insecure_protocol",
    )
    TFM_CONTENT_HTTP = SkimsMethodInfo(
        developer="jecheverri@fluidattacks.com",
        file_name="terraform",
        name="tfm_serves_content_over_http",
    )
    TFM_ELB2_INSEC_PROTO = SkimsMethodInfo(
        developer="atrujillo@fluidattacks.com",
        file_name="terraform",
        name="tfm_elb2_uses_insecure_protocol",
    )
    TFM_AZURE_KV_ONLY_ACCESS_HTTPS = SkimsMethodInfo(
        developer="jecheverri@fluidattacks.com",
        file_name="terraform",
        name="tfm_azure_kv_only_accessible_over_https",
    )
    TFM_AZURE_SA_INSEC_TRANSFER = SkimsMethodInfo(
        developer="jecheverri@fluidattacks.com",
        file_name="terraform",
        name="tfm_azure_sa_insecure_transfer",
    )
    TFM_AWS_SEC_GROUP_USING_HTTP = SkimsMethodInfo(
        developer="jecheverri@fluidattacks.com",
        file_name="terraform",
        name="tfm_aws_sec_group_using_http",
    )
    UNPINNED_DOCKER_IMAGE = SkimsMethodInfo(
        developer="jecheverri@fluidattacks.com",
        file_name="docker",
        name="unpinned_docker_image",
    )
    CHECK_REQUIRED_VERSION = SkimsMethodInfo(
        developer="jecheverri@fluidattacks.com",
        file_name="terraform",
        name="check_required_version",
    )
    USES_HTTP_RESOURCES = SkimsMethodInfo(
        developer="lsaavedra@fluidattacks.com",
        file_name="analyze_bytecodes",
        name="uses_http_resources",
    )
    GEM_GEMFILE_DEV = SkimsMethodInfo(
        developer="lcontreras@fluidattacks.com",
        file_name="gem",
        name="gem_gemfile_dev",
    )
    NPM_PKG_JSON = SkimsMethodInfo(
        developer="machine@fluidattacks.com",
        file_name="npm",
        name="npm_pkg_json",
    )
    NPM_PKG_LOCK_JSON = SkimsMethodInfo(
        developer="machine@fluidattacks.com",
        file_name="npm",
        name="npm_pkg_lock_json",
    )
    NPM_YARN_LOCK_DEV = SkimsMethodInfo(
        developer="lsaavedra@fluidattacks.com",
        file_name="yarn",
        name="npm_yarn_lock_dev",
    )
    CFN_LOG_NOT_VALIDATED = SkimsMethodInfo(
        developer="atrujillo@fluidattacks.com",
        file_name="cloudformation",
        name="cfn_log_files_not_validated",
    )
    CFN_KMS_KEY_ROTATION_DISABLED = SkimsMethodInfo(
        developer="atrujillo@fluidattacks.com",
        file_name="cloudformation",
        name="cfn_kms_key_is_key_rotation_absent_or_disabled",
    )
    CFN_AWS_EFS_UNENCRYPTED = SkimsMethodInfo(
        developer="atrujillo@fluidattacks.com",
        file_name="cloudformation",
        name="cfn_aws_efs_unencrypted",
    )
    CFN_AWS_EBS_VOLUMES_UNENCRYPTED = SkimsMethodInfo(
        developer="atrujillo@fluidattacks.com",
        file_name="cloudformation",
        name="cfn_aws_ebs_volumes_unencrypted",
    )
    CFN_API_GATEWAY_LOGGING_DISABLED = SkimsMethodInfo(
        developer="atrujillo@fluidattacks.com",
        file_name="cloudformation",
        name="cfn_api_gateway_access_logging_disabled",
    )
    CFN_AWS_DYNAMODB_TABLE_UNENCRYPTED = SkimsMethodInfo(
        developer="atrujillo@fluidattacks.com",
        file_name="cloudformation",
        name="cfn_dynamodb_table_unencrypted",
    )
    CFN_AWS_SECRET_WITHOUT_KMS_KEY = SkimsMethodInfo(
        developer="atrujillo@fluidattacks.com",
        file_name="cloudformation",
        name="cfn_aws_secret_encrypted_without_kms_key",
    )
    FRAGMENT_INJECTION = SkimsMethodInfo(
        developer="lsaavedra@fluidattacks.com",
        file_name="analyze_bytecodes",
        name="has_fragment_injection",
    )
    CFN_LOG_CONF_DISABLED = SkimsMethodInfo(
        developer="atrujillo@fluidattacks.com",
        file_name="cloudformation",
        name="cfn_bucket_has_logging_conf_disabled",
    )
    CFN_ELB_ACCESS_LOG_DISABLED = SkimsMethodInfo(
        developer="atrujillo@fluidattacks.com",
        file_name="cloudformation",
        name="cfn_elb_has_access_logging_disabled",
    )
    CFN_CF_DISTR_LOG_DISABLED = SkimsMethodInfo(
        developer="atrujillo@fluidattacks.com",
        file_name="cloudformation",
        name="cfn_cf_distribution_has_logging_disabled",
    )
    CFN_TRAILS_NOT_MULTIREGION = SkimsMethodInfo(
        developer="atrujillo@fluidattacks.com",
        file_name="cloudformation",
        name="cfn_trails_not_multiregion",
    )
    CFN_EC2_MONITORING_DISABLED = SkimsMethodInfo(
        developer="atrujillo@fluidattacks.com",
        file_name="cloudformation",
        name="cfn_ec2_monitoring_disabled",
    )
    CFN_ELB2_LOGS_S3_DISABLED = SkimsMethodInfo(
        developer="atrujillo@fluidattacks.com",
        file_name="cloudformation",
        name="cfn_elb2_has_access_logs_s3_disabled",
    )
    TFM_ELB_LOGGING_DISABLED = SkimsMethodInfo(
        developer="jecheverri@fluidattacks.com",
        file_name="terraform",
        name="tfm_elb_logging_disabled",
    )
    TFM_S3_LOGGING_DISABLED = SkimsMethodInfo(
        developer="jecheverri@fluidattacks.com",
        file_name="terraform",
        name="tfm_s3_bucket_logging_disabled",
    )
    TFM_EC2_MONITORING_DISABLED = SkimsMethodInfo(
        developer="jecheverri@fluidattacks.com",
        file_name="terraform",
        name="tfm_ec2_monitoring_disabled",
    )
    TFM_CF_DISTR_LOG_DISABLED = SkimsMethodInfo(
        developer="atrujillo@fluidattacks.com",
        file_name="terraform",
        name="tfm_distribution_has_logging_disabled",
    )
    TFM_TRAILS_NOT_MULTIREGION = SkimsMethodInfo(
        developer="atrujillo@fluidattacks.com",
        file_name="terraform",
        name="tfm_trails_not_multiregion",
    )
    TFM_LAMBDA_TRACING_DISABLED = SkimsMethodInfo(
        developer="fcalderon@fluidattacks.com",
        file_name="terraform",
        name="tfm_lambda_tracing_disabled",
    )
    TFM_AZURE_KV_SECRET_NO_EXPIRATION = SkimsMethodInfo(
        developer="jecheverri@fluidattacks.com",
        file_name="terraform",
        name="tfm_azure_kv_secret_no_expiration_date",
    )
    TFM_AZURE_STORAGE_LOG_DISABLED = SkimsMethodInfo(
        developer="jecheverri@fluidattacks.com",
        file_name="terraform",
        name="tfm_azure_storage_logging_disabled",
    )
    TFM_AZURE_APP_LOG_DISABLED = SkimsMethodInfo(
        developer="jecheverri@fluidattacks.com",
        file_name="terraform",
        name="tfm_azure_app_service_logging_disabled",
    )
    TFM_AZURE_SQL_LOG_RETENT = SkimsMethodInfo(
        developer="jecheverri@fluidattacks.com",
        file_name="terraform",
        name="tfm_azure_sql_server_audit_log_retention",
    )
    TFM_AWS_EFS_UNENCRYPTED = SkimsMethodInfo(
        developer="jecheverri@fluidattacks.com",
        file_name="terraform",
        name="tfm_aws_efs_unencrypted",
    )
    TFM_AWS_EBS_VOLUMES_UNENCRYPTED = SkimsMethodInfo(
        developer="jecheverri@fluidattacks.com",
        file_name="terraform",
        name="tfm_aws_ebs_volumes_unencrypted",
    )
    TFM_API_GATEWAY_LOGGING_DISABLED = SkimsMethodInfo(
        developer="jecheverri@fluidattacks.com",
        file_name="terraform",
        name="tfm_api_gateway_access_logging_disabled",
    )
    TFM_AZURE_KEY_VAULT_NOT_RECOVER = SkimsMethodInfo(
        developer="jecheverri@fluidattacks.com",
        file_name="terraform",
        name="tfm_azure_key_vault_not_recoverable",
    )
    CS_INSECURE_ASSEMBLY_LOAD = SkimsMethodInfo(
        developer="jecheverri@fluidattacks.com",
        file_name="csharp",
        name="csharp_insecure_assembly_load",
    )
    CS_DISABLED_HTTP_HEADER_CHECK = SkimsMethodInfo(
        developer="jecheverri@fluidattacks.com",
        file_name="csharp",
        name="csharp_disabled_http_header_check",
    )
    CS_XAML_INJECTION = SkimsMethodInfo(
        developer="jecheverri@fluidattacks.com",
        file_name="csharp",
        name="csharp_xaml_injection",
    )
    DOCKER_COMPOSE_READ_ONLY = SkimsMethodInfo(
        developer="jecheverri@fluidattacks.com",
        file_name="docker",
        name="docker_compose_read_only",
    )
    DOCKER_USING_ADD_COMMAND = SkimsMethodInfo(
        developer="jecheverri@fluidattacks.com",
        file_name="docker",
        name="docker_using_add_command",
    )
    DOCKER_PORT_22_EXPOSED = SkimsMethodInfo(
        developer="jecheverri@fluidattacks.com",
        file_name="docker",
        name="docker_port_22_exposed",
    )
    JAVA_USES_SYSTEM_EXIT = SkimsMethodInfo(
        developer="lsaavedra@fluidattacks.com",
        file_name="java",
        name="java_uses_exit_method",
    )
    JAVA_HAS_PRINT_STATEMENTS = SkimsMethodInfo(
        developer="lpatino@fluidattacks.com",
        file_name="java",
        name="java_has_print_statements",
    )
    # Legacy methods that were renamed
    CONTAINER_WHITOUR_USER = SkimsMethodInfo(
        developer="jecheverri@fluidattacks.com",
        file_name="docker",
        name="container_whitout_user",
    )
    DOCKER_COMPOSE_WHITOUR_USER = SkimsMethodInfo(
        developer="jecheverri@fluidattacks.com",
        file_name="docker",
        name="docker_compose_whitout_user",
    )
    QUERY_F001_2 = SkimsMethodInfo(
        developer="drestrepo@fluidattacks.com",
        file_name="query",
        name="query_f001",
    )


async def main() -> None:
    loaders: Dataloaders = get_new_context()
    methods_developers: Dict[str, str] = {
        f"{method.value.file_name}.{method.value.name}": method.value.developer
        for method in SkimsMethods
    }
    groups = await orgs_domain.get_all_active_group_names(loaders=loaders)
    total_groups: int = len(groups)
    for idx, group in enumerate(groups):
        print(f"Processing group {group} ({idx+1}/{total_groups})...")
        findings = await loaders.group_drafts_and_findings.load(group)
        vulns = await loaders.finding_vulnerabilities.load_many_chained(
            [fin.id for fin in findings]
        )
        machine_vulns: List[Vulnerability] = [
            vuln
            for vuln in vulns
            if (vuln.state.source == Source.MACHINE) or vuln.skims_method
        ]
        if machine_vulns:
            vulns_developers: List[Optional[str]] = [
                methods_developers.get(vuln.skims_method)
                if vuln.skims_method
                else None
                for vuln in machine_vulns
            ]
            vulns_to_update: List[Tuple[Vulnerability, Optional[str]]] = [
                (vuln, developer)
                for vuln, developer in zip(machine_vulns, vulns_developers)
                if (
                    vuln.hacker_email != "machine@fluidattacks.com"
                    or vuln.developer != developer
                )
            ]
            if vulns_to_update:
                print(
                    f"{len(vulns_to_update)} vulnerabilities will be updated"
                )
                await collect(
                    (
                        update_metadata(
                            finding_id=vuln.finding_id,
                            metadata=VulnerabilityMetadataToUpdate(
                                created_by="machine@fluidattacks.com",
                                hacker_email="machine@fluidattacks.com",
                                developer=developer,
                            ),
                            vulnerability_id=vuln.id,
                        )
                        for vuln, developer in vulns_to_update
                    ),
                    workers=15,
                )


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:    %Y-%m-%d at %H:%M:%S %Z"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S %Z"
    )
    print(f"{execution_time}\n{finalization_time}")
