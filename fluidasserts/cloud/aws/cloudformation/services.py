# pylint: disable=too-many-lines

"""Actions and privileges for AWS Services in cloudformation templates."""

ACTIONS = {
    "rds": {
        "write": [
            "AddRoleToDBCluster", "AddRoleToDBInstance",
            "AddSourceIdentifierToSubscription",
            "ApplyPendingMaintenanceAction", "BacktrackDBCluster",
            "CopyDBClusterParameterGroup", "CopyDBClusterSnapshot",
            "CopyDBParameterGroup", "CopyDBSnapshot", "CopyOptionGroup",
            "CreateDBClusterEndpoint", "CreateGlobalCluster",
            "DeleteDBCluster", "DeleteDBClusterEndpoint",
            "DeleteDBClusterParameterGroup", "DeleteDBClusterSnapshot",
            "DeleteDBInstance", "DeleteDBInstanceAutomatedBackup",
            "DeleteDBParameterGroup", "DeleteDBSecurityGroup",
            "DeleteDBSnapshot", "DeleteDBSubnetGroup",
            "DeleteEventSubscription", "DeleteGlobalCluster",
            "DeleteOptionGroup", "FailoverDBCluster",
            "ModifyCurrentDBClusterCapacity", "ModifyDBCluster",
            "ModifyDBClusterEndpoint", "ModifyDBClusterParameterGroup",
            "ModifyDBClusterSnapshotAttribute", "ModifyDBInstance",
            "ModifyDBParameterGroup", "ModifyDBSnapshot",
            "ModifyDBSnapshotAttribute", "ModifyDBSubnetGroup",
            "ModifyEventSubscription", "ModifyGlobalCluster",
            "ModifyOptionGroup", "PromoteReadReplica",
            "PromoteReadReplicaDBCluster",
            "PurchaseReservedDBInstancesOffering", "RebootDBInstance",
            "RemoveFromGlobalCluster", "RemoveRoleFromDBCluster",
            "RemoveRoleFromDBInstance",
            "RemoveSourceIdentifierFromSubscription",
            "ResetDBClusterParameterGroup", "ResetDBParameterGroup",
            "RestoreDBClusterFromS3", "RestoreDBClusterFromSnapshot",
            "RestoreDBClusterToPointInTime", "RestoreDBInstanceFromDBSnapshot",
            "RestoreDBInstanceFromS3", "RestoreDBInstanceToPointInTime",
            "RevokeDBSecurityGroupIngress", "StartActivityStream",
            "StartDBCluster", "StartDBInstance", "StopActivityStream",
            "StopDBCluster", "StopDBInstance"
        ],
        "tagging": [
            "AddTagsToResource", "CreateDBCluster",
            "CreateDBClusterParameterGroup", "CreateDBClusterSnapshot",
            "CreateDBInstance", "CreateDBInstanceReadReplica",
            "CreateDBParameterGroup", "CreateDBSecurityGroup",
            "CreateDBSnapshot", "CreateDBSubnetGroup",
            "CreateEventSubscription", "CreateOptionGroup",
            "RemoveTagsFromResource"
        ],
        "permissions_management": ["AuthorizeDBSecurityGroupIngress"],
        "list": [
            "DescribeAccountAttributes", "DescribeCertificates",
            "DescribeDBClusterBacktracks", "DescribeDBClusterEndpoints",
            "DescribeDBClusterParameterGroups", "DescribeDBClusterParameters",
            "DescribeDBClusterSnapshotAttributes", "DescribeDBClusters",
            "DescribeDBEngineVersions", "DescribeDBInstanceAutomatedBackups",
            "DescribeDBInstances", "DescribeDBLogFiles",
            "DescribeDBParameterGroups", "DescribeDBParameters",
            "DescribeDBSecurityGroups", "DescribeDBSnapshotAttributes",
            "DescribeDBSnapshots", "DescribeDBSubnetGroups",
            "DescribeEngineDefaultClusterParameters",
            "DescribeEngineDefaultParameters", "DescribeEventCategories",
            "DescribeEventSubscriptions", "DescribeEvents",
            "DescribeGlobalClusters", "DescribeOptionGroupOptions",
            "DescribeOptionGroups", "DescribeOrderableDBInstanceOptions",
            "DescribePendingMaintenanceActions", "DescribeReservedDBInstances",
            "DescribeReservedDBInstancesOfferings", "DescribeSourceRegions",
            "DescribeValidDBInstanceModifications"
        ],
        "read": [
            "DescribeDBClusterSnapshots", "DownloadCompleteDBLogFile",
            "DownloadDBLogFilePortion", "ListTagsForResource"
        ]
    },
    "logs": {
        "write": [
            "AssociateKmsKey", "CancelExportTask", "CreateExportTask",
            "CreateLogGroup", "CreateLogStream", "DeleteDestination",
            "DeleteLogGroup", "DeleteLogStream", "DeleteMetricFilter",
            "DeleteResourcePolicy", "DeleteRetentionPolicy",
            "DeleteSubscriptionFilter", "DisassociateKmsKey", "PutDestination",
            "PutDestinationPolicy", "PutLogEvents", "PutMetricFilter",
            "PutResourcePolicy", "PutRetentionPolicy", "PutSubscriptionFilter",
            "TagLogGroup", "UntagLogGroup"
        ],
        "list": [
            "DescribeDestinations", "DescribeExportTasks", "DescribeLogGroups",
            "DescribeLogStreams", "DescribeMetricFilters", "DescribeQueries",
            "DescribeResourcePolicies", "DescribeSubscriptionFilters",
            "ListTagsLogGroup"
        ],
        "read": [
            "FilterLogEvents", "GetLogEvents", "GetLogGroupFields",
            "GetLogRecord", "GetQueryResults", "StartQuery", "StopQuery",
            "TestMetricFilter"
        ]
    },
    "ec2": {
        "write": [
            "AcceptReservedInstancesExchangeQuote",
            "AcceptTransitGatewayVpcAttachment",
            "AcceptVpcEndpointConnections", "AcceptVpcPeeringConnection",
            "AdvertiseByoipCidr", "AllocateAddress", "AllocateHosts",
            "ApplySecurityGroupsToClientVpnTargetNetwork",
            "AssignIpv6Addresses", "AssignPrivateIpAddresses",
            "AssociateAddress", "AssociateClientVpnTargetNetwork",
            "AssociateDhcpOptions", "AssociateIamInstanceProfile",
            "AssociateRouteTable", "AssociateSubnetCidrBlock",
            "AssociateTransitGatewayRouteTable", "AssociateVpcCidrBlock",
            "AttachClassicLinkVpc", "AttachInternetGateway",
            "AttachNetworkInterface", "AttachVolume", "AttachVpnGateway",
            "AuthorizeClientVpnIngress", "AuthorizeSecurityGroupEgress",
            "AuthorizeSecurityGroupIngress", "BundleInstance",
            "CancelBundleTask", "CancelCapacityReservation",
            "CancelConversionTask", "CancelExportTask", "CancelImportTask",
            "CancelReservedInstancesListing", "CancelSpotFleetRequests",
            "CancelSpotInstanceRequests", "ConfirmProductInstance",
            "CopyFpgaImage", "CopyImage", "CopySnapshot",
            "CreateCapacityReservation", "CreateClientVpnEndpoint",
            "CreateClientVpnRoute", "CreateCustomerGateway",
            "CreateDefaultSubnet", "CreateDefaultVpc", "CreateDhcpOptions",
            "CreateEgressOnlyInternetGateway", "CreateFleet", "CreateFlowLogs",
            "CreateFpgaImage", "CreateImage", "CreateInstanceExportTask",
            "CreateInternetGateway", "CreateKeyPair", "CreateLaunchTemplate",
            "CreateLaunchTemplateVersion", "CreateNatGateway",
            "CreateNetworkAcl", "CreateNetworkAclEntry",
            "CreateNetworkInterface", "CreatePlacementGroup",
            "CreateReservedInstancesListing", "CreateRoute",
            "CreateRouteTable", "CreateSecurityGroup", "CreateSnapshot",
            "CreateSnapshots", "CreateSpotDatafeedSubscription",
            "CreateSubnet", "CreateTrafficMirrorFilter",
            "CreateTrafficMirrorFilterRule", "CreateTrafficMirrorSession",
            "CreateTrafficMirrorTarget", "CreateTransitGateway",
            "CreateTransitGatewayRoute", "CreateTransitGatewayRouteTable",
            "CreateTransitGatewayVpcAttachment", "CreateVolume", "CreateVpc",
            "CreateVpcEndpoint", "CreateVpcEndpointConnectionNotification",
            "CreateVpcEndpointServiceConfiguration",
            "CreateVpcPeeringConnection", "CreateVpnConnection",
            "CreateVpnConnectionRoute", "CreateVpnGateway",
            "DeleteClientVpnEndpoint", "DeleteClientVpnRoute",
            "DeleteCustomerGateway", "DeleteDhcpOptions",
            "DeleteEgressOnlyInternetGateway", "DeleteFleets",
            "DeleteFlowLogs", "DeleteFpgaImage", "DeleteInternetGateway",
            "DeleteKeyPair", "DeleteLaunchTemplate",
            "DeleteLaunchTemplateVersions", "DeleteNatGateway",
            "DeleteNetworkAcl", "DeleteNetworkAclEntry",
            "DeleteNetworkInterface", "DeletePlacementGroup", "DeleteRoute",
            "DeleteRouteTable", "DeleteSecurityGroup", "DeleteSnapshot",
            "DeleteSpotDatafeedSubscription", "DeleteSubnet",
            "DeleteTrafficMirrorFilter", "DeleteTrafficMirrorFilterRule",
            "DeleteTrafficMirrorSession", "DeleteTrafficMirrorTarget",
            "DeleteTransitGateway", "DeleteTransitGatewayRoute",
            "DeleteTransitGatewayRouteTable",
            "DeleteTransitGatewayVpcAttachment", "DeleteVolume", "DeleteVpc",
            "DeleteVpcEndpointConnectionNotifications",
            "DeleteVpcEndpointServiceConfigurations", "DeleteVpcEndpoints",
            "DeleteVpcPeeringConnection", "DeleteVpnConnection",
            "DeleteVpnConnectionRoute", "DeleteVpnGateway",
            "DeprovisionByoipCidr", "DeregisterImage", "DetachClassicLinkVpc",
            "DetachInternetGateway", "DetachNetworkInterface", "DetachVolume",
            "DetachVpnGateway", "DisableEbsEncryptionByDefault",
            "DisableFastSnapshotRestores",
            "DisableTransitGatewayRouteTablePropagation",
            "DisableVgwRoutePropagation", "DisableVpcClassicLink",
            "DisableVpcClassicLinkDnsSupport", "DisassociateAddress",
            "DisassociateClientVpnTargetNetwork",
            "DisassociateIamInstanceProfile", "DisassociateRouteTable",
            "DisassociateSubnetCidrBlock",
            "DisassociateTransitGatewayRouteTable", "DisassociateVpcCidrBlock",
            "EnableEbsEncryptionByDefault", "EnableFastSnapshotRestores",
            "EnableTransitGatewayRouteTablePropagation",
            "EnableVgwRoutePropagation", "EnableVolumeIO",
            "EnableVpcClassicLink", "EnableVpcClassicLinkDnsSupport",
            "ExportImage", "ExportTransitGatewayRoutes",
            "ImportClientVpnClientCertificateRevocationList", "ImportImage",
            "ImportInstance", "ImportKeyPair", "ImportSnapshot",
            "ImportVolume", "ModifyCapacityReservation",
            "ModifyClientVpnEndpoint", "ModifyEbsDefaultKmsKeyId",
            "ModifyFleet", "ModifyFpgaImageAttribute", "ModifyHosts",
            "ModifyIdFormat", "ModifyIdentityIdFormat", "ModifyImageAttribute",
            "ModifyInstanceAttribute",
            "ModifyInstanceCapacityReservationAttributes",
            "ModifyInstanceCreditSpecification",
            "ModifyInstanceEventStartTime", "ModifyInstanceMetadataOptions",
            "ModifyInstancePlacement", "ModifyLaunchTemplate",
            "ModifyNetworkInterfaceAttribute", "ModifyReservedInstances",
            "ModifySpotFleetRequest", "ModifySubnetAttribute",
            "ModifyTrafficMirrorFilterNetworkServices",
            "ModifyTrafficMirrorFilterRule", "ModifyTrafficMirrorSession",
            "ModifyTransitGatewayVpcAttachment", "ModifyVolume",
            "ModifyVolumeAttribute", "ModifyVpcAttribute", "ModifyVpcEndpoint",
            "ModifyVpcEndpointConnectionNotification",
            "ModifyVpcEndpointServiceConfiguration",
            "ModifyVpcPeeringConnectionOptions", "ModifyVpcTenancy",
            "ModifyVpnConnection", "ModifyVpnTunnelOptions",
            "MonitorInstances", "MoveAddressToVpc", "ProvisionByoipCidr",
            "PurchaseHostReservation", "PurchaseReservedInstancesOffering",
            "PurchaseScheduledInstances", "RebootInstances", "RegisterImage",
            "RejectTransitGatewayVpcAttachment",
            "RejectVpcEndpointConnections", "RejectVpcPeeringConnection",
            "ReleaseAddress", "ReleaseHosts",
            "ReplaceIamInstanceProfileAssociation",
            "ReplaceNetworkAclAssociation", "ReplaceNetworkAclEntry",
            "ReplaceRoute", "ReplaceRouteTableAssociation",
            "ReplaceTransitGatewayRoute", "ReportInstanceStatus",
            "RequestSpotFleet", "RequestSpotInstances",
            "ResetEbsDefaultKmsKeyId", "ResetFpgaImageAttribute",
            "ResetImageAttribute", "ResetInstanceAttribute",
            "ResetNetworkInterfaceAttribute", "RestoreAddressToClassic",
            "RevokeClientVpnIngress", "RevokeSecurityGroupEgress",
            "RevokeSecurityGroupIngress", "RunInstances",
            "RunScheduledInstances", "SendDiagnosticInterrupt",
            "StartInstances", "StopInstances", "TerminateClientVpnConnections",
            "TerminateInstances", "UnassignIpv6Addresses",
            "UnassignPrivateIpAddresses", "UnmonitorInstances",
            "UpdateSecurityGroupRuleDescriptionsEgress",
            "UpdateSecurityGroupRuleDescriptionsIngress", "WithdrawByoipCidr"
        ],
        "permissions_management": [
            "CreateNetworkInterfacePermission",
            "DeleteNetworkInterfacePermission", "ModifySnapshotAttribute",
            "ModifyVpcEndpointServicePermissions", "ResetSnapshotAttribute"
        ],
        "tagging": ["CreateTags", "DeleteTags"],
        "list": [
            "DescribeAccountAttributes", "DescribeAddresses",
            "DescribeAggregateIdFormat", "DescribeAvailabilityZones",
            "DescribeBundleTasks", "DescribeByoipCidrs",
            "DescribeCapacityReservations", "DescribeClassicLinkInstances",
            "DescribeClientVpnAuthorizationRules",
            "DescribeClientVpnConnections", "DescribeClientVpnEndpoints",
            "DescribeClientVpnRoutes", "DescribeClientVpnTargetNetworks",
            "DescribeConversionTasks", "DescribeCustomerGateways",
            "DescribeDhcpOptions", "DescribeEgressOnlyInternetGateways",
            "DescribeExportImageTasks", "DescribeExportTasks",
            "DescribeFleetHistory", "DescribeFleetInstances", "DescribeFleets",
            "DescribeFlowLogs", "DescribeFpgaImageAttribute",
            "DescribeFpgaImages", "DescribeHostReservationOfferings",
            "DescribeHostReservations", "DescribeHosts",
            "DescribeIamInstanceProfileAssociations", "DescribeIdFormat",
            "DescribeIdentityIdFormat", "DescribeImageAttribute",
            "DescribeImages", "DescribeImportImageTasks",
            "DescribeImportSnapshotTasks", "DescribeInstanceAttribute",
            "DescribeInstanceCreditSpecifications", "DescribeInstanceStatus",
            "DescribeInstances", "DescribeInternetGateways",
            "DescribeKeyPairs", "DescribeLaunchTemplateVersions",
            "DescribeLaunchTemplates", "DescribeMovingAddresses",
            "DescribeNatGateways", "DescribeNetworkAcls",
            "DescribeNetworkInterfaceAttribute",
            "DescribeNetworkInterfacePermissions", "DescribeNetworkInterfaces",
            "DescribePlacementGroups", "DescribePrefixLists",
            "DescribePrincipalIdFormat", "DescribePublicIpv4Pools",
            "DescribeRegions", "DescribeReservedInstances",
            "DescribeReservedInstancesListings",
            "DescribeReservedInstancesModifications",
            "DescribeReservedInstancesOfferings", "DescribeRouteTables",
            "DescribeSecurityGroupReferences", "DescribeSecurityGroups",
            "DescribeSnapshotAttribute", "DescribeSnapshots",
            "DescribeSpotDatafeedSubscription", "DescribeSpotFleetInstances",
            "DescribeSpotFleetRequestHistory", "DescribeSpotFleetRequests",
            "DescribeSpotInstanceRequests", "DescribeSpotPriceHistory",
            "DescribeStaleSecurityGroups", "DescribeSubnets",
            "DescribeTrafficMirrorFilters", "DescribeTrafficMirrorSessions",
            "DescribeTrafficMirrorTargets",
            "DescribeTransitGatewayAttachments",
            "DescribeTransitGatewayRouteTables",
            "DescribeTransitGatewayVpcAttachments", "DescribeTransitGateways",
            "DescribeVolumeAttribute", "DescribeVolumeStatus",
            "DescribeVolumes", "DescribeVpcAttribute",
            "DescribeVpcClassicLink", "DescribeVpcClassicLinkDnsSupport",
            "DescribeVpcEndpointConnectionNotifications",
            "DescribeVpcEndpointConnections",
            "DescribeVpcEndpointServiceConfigurations",
            "DescribeVpcEndpointServicePermissions",
            "DescribeVpcEndpointServices", "DescribeVpcEndpoints",
            "DescribeVpcPeeringConnections", "DescribeVpcs",
            "DescribeVpnGateways",
            "ExportClientVpnClientCertificateRevocationList",
            "ExportClientVpnClientConfiguration",
            "GetTransitGatewayAttachmentPropagations",
            "GetTransitGatewayRouteTableAssociations",
            "GetTransitGatewayRouteTablePropagations",
            "SearchTransitGatewayRoutes"
        ],
        "read": [
            "DescribeElasticGpus", "DescribeFastSnapshotRestores",
            "DescribeScheduledInstanceAvailability",
            "DescribeScheduledInstances", "DescribeTags",
            "DescribeVolumesModifications", "DescribeVpnConnections",
            "GetCapacityReservationUsage", "GetConsoleOutput",
            "GetConsoleScreenshot", "GetEbsDefaultKmsKeyId",
            "GetEbsEncryptionByDefault", "GetHostReservationPurchasePreview",
            "GetLaunchTemplateData", "GetPasswordData",
            "GetReservedInstancesExchangeQuote"
        ]
    },
    "cloudwatch": {
        "write": [
            "DeleteAlarms", "DeleteAnomalyDetector", "DeleteDashboards",
            "DeleteInsightRules", "DisableAlarmActions", "DisableInsightRules",
            "EnableAlarmActions", "EnableInsightRules", "PutAnomalyDetector",
            "PutDashboard", "PutInsightRule", "PutMetricAlarm",
            "PutMetricData", "SetAlarmState"
        ],
        "read": [
            "DescribeAlarmHistory", "DescribeAlarms",
            "DescribeAlarmsForMetric", "DescribeAnomalyDetectors",
            "DescribeInsightRules", "GetDashboard", "GetInsightRuleReport",
            "GetMetricData", "GetMetricStatistics", "GetMetricWidgetImage"
        ],
        "list": ["ListDashboards", "ListMetrics", "ListTagsForResource"],
        "tagging": ["TagResource", "UntagResource"]
    },
    "application-autoscaling": {
        "write": [
            "DeleteScalingPolicy", "DeleteScheduledAction",
            "DeregisterScalableTarget", "PutScalingPolicy",
            "PutScheduledAction", "RegisterScalableTarget"
        ],
        "read": [
            "DescribeScalableTargets", "DescribeScalingActivities",
            "DescribeScalingPolicies", "DescribeScheduledActions"
        ]
    },
    "secretsmanager": {
        "write": [
            "CancelRotateSecret", "DeleteSecret", "PutSecretValue",
            "RestoreSecret", "RotateSecret", "UpdateSecret",
            "UpdateSecretVersionStage"
        ],
        "tagging": ["CreateSecret", "TagResource", "UntagResource"],
        "permissions_management":
        ["DeleteResourcePolicy", "PutResourcePolicy"],
        "read": [
            "DescribeSecret", "GetRandomPassword", "GetResourcePolicy",
            "GetSecretValue", "ListSecretVersionIds"
        ],
        "list": ["ListSecrets"]
    },
    "cloudformation": {
        "write": [
            "CancelUpdateStack", "ContinueUpdateRollback", "CreateChangeSet",
            "CreateStack", "CreateStackInstances", "CreateStackSet",
            "DeleteChangeSet", "DeleteStack", "DeleteStackInstances",
            "DeleteStackSet", "ExecuteChangeSet", "SignalResource",
            "StopStackSetOperation", "UpdateStack", "UpdateStackInstances",
            "UpdateStackSet", "UpdateTerminationProtection", "ValidateTemplate"
        ],
        "read": [
            "DescribeAccountLimits", "DescribeChangeSet",
            "DescribeStackDriftDetectionStatus", "DescribeStackEvents",
            "DescribeStackInstance", "DescribeStackResource",
            "DescribeStackResourceDrifts", "DescribeStackResources",
            "DescribeStackSet", "DescribeStackSetOperation",
            "DetectStackDrift", "DetectStackResourceDrift",
            "EstimateTemplateCost", "GetStackPolicy", "GetTemplate",
            "GetTemplateSummary"
        ],
        "list": [
            "DescribeStacks", "ListChangeSets", "ListExports", "ListImports",
            "ListStackInstances", "ListStackResources",
            "ListStackSetOperationResults", "ListStackSetOperations",
            "ListStackSets", "ListStacks"
        ],
        "permissions_management": ["SetStackPolicy"]
    },
    "lambda": {
        "permissions_management": [
            "AddLayerVersionPermission", "AddPermission",
            "RemoveLayerVersionPermission", "RemovePermission"
        ],
        "write": [
            "CreateAlias", "CreateEventSourceMapping", "CreateFunction",
            "DeleteAlias", "DeleteEventSourceMapping", "DeleteFunction",
            "DeleteFunctionConcurrency", "DeleteLayerVersion", "InvokeAsync",
            "InvokeFunction", "PublishLayerVersion", "PublishVersion",
            "PutFunctionConcurrency", "TagResource", "UntagResource",
            "UpdateAlias", "UpdateEventSourceMapping", "UpdateFunctionCode",
            "UpdateFunctionConfiguration"
        ],
        "read": [
            "GetAccountSettings", "GetAlias", "GetEventSourceMapping",
            "GetFunction", "GetFunctionConfiguration", "GetLayerVersion",
            "GetLayerVersionPolicy", "GetPolicy", "ListTags"
        ],
        "list": [
            "ListAliases", "ListEventSourceMappings", "ListFunctions",
            "ListLayerVersions", "ListLayers", "ListVersionsByFunction"
        ]
    },
    "tag": {
        "read": [
            "DescribeReportCreation", "GetComplianceSummary", "GetResources",
            "GetTagKeys", "GetTagValues"
        ],
        "write": ["StartReportCreation"],
        "tagging": ["TagResources", "UntagResources"]
    },
    "sts": {
        "write": [
            "AssumeRole", "AssumeRoleWithSAML", "AssumeRoleWithWebIdentity",
            "DecodeAuthorizationMessage"
        ],
        "read": [
            "GetAccessKeyInfo", "GetCallerIdentity", "GetFederationToken",
            "GetSessionToken"
        ],
        "tagging": ["TagSession"]
    },
    "s3": {
        "write": [
            "AbortMultipartUpload", "CreateBucket", "CreateJob",
            "DeleteBucket", "DeleteBucketWebsite", "DeleteObject",
            "DeleteObjectVersion", "GetBucketObjectLockConfiguration",
            "GetObjectLegalHold", "GetObjectRetention",
            "PutAccelerateConfiguration", "PutAnalyticsConfiguration",
            "PutBucketCORS", "PutBucketLogging", "PutBucketNotification",
            "PutBucketObjectLockConfiguration", "PutBucketRequestPayment",
            "PutBucketVersioning", "PutBucketWebsite",
            "PutEncryptionConfiguration", "PutInventoryConfiguration",
            "PutLifecycleConfiguration", "PutMetricsConfiguration",
            "PutObject", "PutObjectLegalHold", "PutObjectRetention",
            "PutReplicationConfiguration", "RestoreObject",
            "UpdateJobPriority", "UpdateJobStatus"
        ],
        "permissions_management": [
            "DeleteBucketPolicy", "PutAccountPublicAccessBlock",
            "PutBucketAcl", "PutBucketPolicy", "PutBucketPublicAccessBlock",
            "PutObjectAcl", "PutObjectVersionAcl"
        ],
        "tagging": [
            "DeleteObjectTagging", "DeleteObjectVersionTagging",
            "PutBucketTagging", "PutObjectTagging", "PutObjectVersionTagging"
        ],
        "read": [
            "DescribeJob", "GetAccelerateConfiguration",
            "GetAccountPublicAccessBlock", "GetAnalyticsConfiguration",
            "GetBucketAcl", "GetBucketCORS", "GetBucketLocation",
            "GetBucketLogging", "GetBucketNotification", "GetBucketPolicy",
            "GetBucketPolicyStatus", "GetBucketPublicAccessBlock",
            "GetBucketRequestPayment", "GetBucketTagging",
            "GetBucketVersioning", "GetBucketWebsite",
            "GetEncryptionConfiguration", "GetInventoryConfiguration",
            "GetLifecycleConfiguration", "GetMetricsConfiguration",
            "GetObject", "GetObjectAcl", "GetObjectTagging",
            "GetObjectTorrent", "GetObjectVersion", "GetObjectVersionAcl",
            "GetObjectVersionTagging", "GetObjectVersionTorrent",
            "GetReplicationConfiguration", "ListBucketMultipartUploads",
            "ListBucketVersions", "ListJobs", "ListMultipartUploadParts"
        ],
        "list": ["ListAllMyBuckets", "ListBucket"]
    },
    "kms": {
        "write": [
            "CancelKeyDeletion", "ConnectCustomKeyStore", "CreateAlias",
            "CreateCustomKeyStore", "CreateKey", "Decrypt", "DeleteAlias",
            "DeleteCustomKeyStore", "DeleteImportedKeyMaterial", "DisableKey",
            "DisableKeyRotation", "DisconnectCustomKeyStore", "EnableKey",
            "EnableKeyRotation", "Encrypt", "GenerateDataKey",
            "GenerateDataKeyPair", "GenerateDataKeyPairWithoutPlaintext",
            "GenerateDataKeyWithoutPlaintext", "GenerateRandom",
            "ImportKeyMaterial", "ReEncryptFrom", "ReEncryptTo",
            "ScheduleKeyDeletion", "Sign", "UpdateAlias",
            "UpdateCustomKeyStore", "UpdateKeyDescription", "Verify"
        ],
        "permissions_management":
        ["CreateGrant", "PutKeyPolicy", "RetireGrant", "RevokeGrant"],
        "read": [
            "DescribeCustomKeyStores", "DescribeKey", "GetKeyPolicy",
            "GetKeyRotationStatus", "GetParametersForImport", "GetPublicKey",
            "ListResourceTags"
        ],
        "list": [
            "ListAliases", "ListGrants", "ListKeyPolicies", "ListKeys",
            "ListRetirableGrants"
        ],
        "tagging": ["TagResource", "UntagResource"]
    },
    "sns": {
        "permissions_management": ["AddPermission", "RemovePermission"],
        "read": [
            "CheckIfPhoneNumberIsOptedOut", "GetEndpointAttributes",
            "GetPlatformApplicationAttributes", "GetSMSAttributes",
            "GetSubscriptionAttributes", "GetTopicAttributes",
            "ListPhoneNumbersOptedOut", "ListTagsForResource"
        ],
        "write": [
            "ConfirmSubscription", "CreatePlatformApplication",
            "CreatePlatformEndpoint", "CreateTopic", "DeleteEndpoint",
            "DeletePlatformApplication", "DeleteTopic", "OptInPhoneNumber",
            "Publish", "SetEndpointAttributes",
            "SetPlatformApplicationAttributes", "SetSubscriptionAttributes",
            "SetTopicAttributes", "Subscribe", "Unsubscribe"
        ],
        "list": [
            "ListEndpointsByPlatformApplication", "ListPlatformApplications",
            "ListSubscriptions", "ListSubscriptionsByTopic", "ListTopics"
        ],
        "tagging": ["TagResource", "UntagResource"]
    },
    "route53": {
        "write": [
            "AssociateVPCWithHostedZone", "ChangeResourceRecordSets",
            "CreateHealthCheck", "CreateHostedZone",
            "CreateQueryLoggingConfig", "CreateReusableDelegationSet",
            "CreateTrafficPolicy", "CreateTrafficPolicyInstance",
            "CreateTrafficPolicyVersion", "CreateVPCAssociationAuthorization",
            "DeleteHealthCheck", "DeleteHostedZone",
            "DeleteQueryLoggingConfig", "DeleteReusableDelegationSet",
            "DeleteTrafficPolicy", "DeleteTrafficPolicyInstance",
            "DeleteVPCAssociationAuthorization",
            "DisassociateVPCFromHostedZone", "UpdateHealthCheck",
            "UpdateHostedZoneComment", "UpdateTrafficPolicyComment",
            "UpdateTrafficPolicyInstance"
        ],
        "tagging": ["ChangeTagsForResource"],
        "read": [
            "GetAccountLimit", "GetHealthCheck", "GetHostedZoneLimit",
            "GetQueryLoggingConfig", "GetReusableDelegationSetLimit",
            "GetTrafficPolicy", "GetTrafficPolicyInstance",
            "GetTrafficPolicyInstanceCount", "ListTagsForResource",
            "ListTagsForResources", "ListTrafficPolicies",
            "ListTrafficPolicyInstances",
            "ListTrafficPolicyInstancesByHostedZone",
            "ListTrafficPolicyInstancesByPolicy", "ListTrafficPolicyVersions",
            "ListVPCAssociationAuthorizations", "TestDNSAnswer"
        ],
        "list": [
            "GetChange", "GetCheckerIpRanges", "GetGeoLocation",
            "GetHealthCheckCount", "GetHealthCheckLastFailureReason",
            "GetHealthCheckStatus", "GetHostedZone", "GetHostedZoneCount",
            "GetReusableDelegationSet", "ListGeoLocations", "ListHealthChecks",
            "ListHostedZones", "ListHostedZonesByName",
            "ListQueryLoggingConfigs", "ListResourceRecordSets",
            "ListReusableDelegationSets"
        ]
    },
    "eks": {
        "write": [
            "CreateCluster", "CreateFargateProfile", "CreateNodegroup",
            "DeleteCluster", "DeleteFargateProfile", "DeleteNodegroup",
            "UpdateClusterConfig", "UpdateClusterVersion",
            "UpdateNodegroupConfig", "UpdateNodegroupVersion"
        ],
        "read": [
            "DescribeCluster", "DescribeFargateProfile", "DescribeNodegroup",
            "DescribeUpdate"
        ],
        "list": [
            "ListClusters", "ListFargateProfiles", "ListNodegroups",
            "ListTagsForResource", "ListUpdates"
        ],
        "tagging": ["TagResource", "UntagResource"]
    },
    "sqs": {
        "permissions_management": ["AddPermission", "RemovePermission"],
        "write": [
            "ChangeMessageVisibility", "ChangeMessageVisibilityBatch",
            "CreateQueue", "DeleteMessage", "DeleteMessageBatch",
            "DeleteQueue", "PurgeQueue", "SendMessage", "SendMessageBatch",
            "SetQueueAttributes"
        ],
        "read": [
            "GetQueueAttributes", "GetQueueUrl", "ListDeadLetterSourceQueues",
            "ListQueueTags", "ReceiveMessage"
        ],
        "list": ["ListQueues"],
        "tagging": ["TagQueue", "UntagQueue"]
    },
    "pi": {},
    "ses": {
        "write": [
            "CloneReceiptRuleSet", "CreateConfigurationSet",
            "CreateConfigurationSetEventDestination",
            "CreateConfigurationSetTrackingOptions",
            "CreateCustomVerificationEmailTemplate", "CreateReceiptFilter",
            "CreateReceiptRule", "CreateReceiptRuleSet", "CreateTemplate",
            "DeleteConfigurationSet", "DeleteConfigurationSetEventDestination",
            "DeleteConfigurationSetTrackingOptions",
            "DeleteCustomVerificationEmailTemplate", "DeleteIdentity",
            "DeleteIdentityPolicy", "DeleteReceiptFilter", "DeleteReceiptRule",
            "DeleteReceiptRuleSet", "DeleteTemplate",
            "DeleteVerifiedEmailAddress", "PutIdentityPolicy",
            "ReorderReceiptRuleSet", "SendBounce", "SendBulkTemplatedEmail",
            "SendCustomVerificationEmail", "SendEmail", "SendRawEmail",
            "SendTemplatedEmail", "SetActiveReceiptRuleSet",
            "SetIdentityDkimEnabled", "SetIdentityFeedbackForwardingEnabled",
            "SetIdentityHeadersInNotificationsEnabled",
            "SetIdentityMailFromDomain", "SetIdentityNotificationTopic",
            "SetReceiptRulePosition", "TestRenderTemplate",
            "UpdateAccountSendingEnabled",
            "UpdateConfigurationSetEventDestination",
            "UpdateConfigurationSetReputationMetricsEnabled",
            "UpdateConfigurationSetSendingEnabled",
            "UpdateConfigurationSetTrackingOptions",
            "UpdateCustomVerificationEmailTemplate", "UpdateReceiptRule",
            "UpdateTemplate"
        ],
        "read": [
            "DescribeActiveReceiptRuleSet", "DescribeConfigurationSet",
            "DescribeReceiptRule", "DescribeReceiptRuleSet",
            "GetAccountSendingEnabled", "GetCustomVerificationEmailTemplate",
            "GetIdentityDkimAttributes", "GetIdentityMailFromDomainAttributes",
            "GetIdentityNotificationAttributes", "GetIdentityPolicies",
            "GetIdentityVerificationAttributes", "GetSendQuota",
            "GetSendStatistics", "GetTemplate", "VerifyDomainDkim",
            "VerifyDomainIdentity", "VerifyEmailAddress", "VerifyEmailIdentity"
        ],
        "list": [
            "ListConfigurationSets", "ListCustomVerificationEmailTemplates",
            "ListIdentities", "ListIdentityPolicies", "ListReceiptFilters",
            "ListReceiptRuleSets", "ListTemplates",
            "ListVerifiedEmailAddresses"
        ]
    },
    "dynamodb": {
        "read": [
            "BatchGetItem", "ConditionCheckItem", "DescribeBackup",
            "DescribeContinuousBackups", "DescribeGlobalTable",
            "DescribeGlobalTableSettings", "DescribeLimits", "DescribeStream",
            "DescribeTable", "DescribeTableReplicaAutoScaling",
            "DescribeTimeToLive", "GetItem", "GetRecords", "GetShardIterator",
            "ListStreams", "ListTagsOfResource", "Query", "Scan"
        ],
        "write": [
            "BatchWriteItem", "CreateBackup", "CreateGlobalTable",
            "CreateTable", "CreateTableReplica", "DeleteBackup", "DeleteItem",
            "DeleteTable", "DeleteTableReplica", "PutItem",
            "RestoreTableFromBackup", "RestoreTableToPointInTime",
            "UpdateContinuousBackups", "UpdateGlobalTable",
            "UpdateGlobalTableSettings", "UpdateItem", "UpdateTable",
            "UpdateTableReplicaAutoScaling", "UpdateTimeToLive"
        ],
        "list": ["ListBackups", "ListGlobalTables", "ListTables"],
        "tagging": ["TagResource", "UntagResource"]
    },
    "glue": {
        "write": [
            "BatchCreatePartition", "BatchDeleteConnection",
            "BatchDeletePartition", "BatchDeleteTable", "BatchStopJobRun",
            "CancelMLTaskRun", "CreateClassifier", "CreateConnection",
            "CreateCrawler", "CreateDatabase", "CreateDevEndpoint",
            "CreateJob", "CreateMLTransform", "CreatePartition",
            "CreateScript", "CreateSecurityConfiguration", "CreateTable",
            "CreateTrigger", "CreateUserDefinedFunction", "CreateWorkflow",
            "DeleteClassifier", "DeleteConnection", "DeleteCrawler",
            "DeleteDatabase", "DeleteDevEndpoint", "DeleteJob",
            "DeleteMLTransform", "DeletePartition", "DeleteResourcePolicy",
            "DeleteSecurityConfiguration", "DeleteTable", "DeleteTrigger",
            "DeleteUserDefinedFunction", "DeleteWorkflow", "GetMapping",
            "ImportCatalogToGlue", "PutDataCatalogEncryptionSettings",
            "PutResourcePolicy", "PutWorkflowRunProperties",
            "ResetJobBookmark", "StartCrawler", "StartCrawlerSchedule",
            "StartExportLabelsTaskRun", "StartImportLabelsTaskRun",
            "StartJobRun", "StartMLEvaluationTaskRun",
            "StartMLLabelingSetGenerationTaskRun", "StartTrigger",
            "StartWorkflowRun", "StopCrawler", "StopCrawlerSchedule",
            "StopTrigger", "UpdateClassifier", "UpdateConnection",
            "UpdateCrawler", "UpdateCrawlerSchedule", "UpdateDatabase",
            "UpdateDevEndpoint", "UpdateJob", "UpdateMLTransform",
            "UpdatePartition", "UpdateTable", "UpdateTrigger",
            "UpdateUserDefinedFunction", "UpdateWorkflow", "UseMLTransforms"
        ],
        "read": [
            "BatchDeleteTableVersion", "BatchGetCrawlers",
            "BatchGetDevEndpoints", "BatchGetJobs", "BatchGetPartition",
            "BatchGetTriggers", "BatchGetWorkflows", "DeleteTableVersion",
            "GetCatalogImportStatus", "GetClassifier", "GetClassifiers",
            "GetConnection", "GetConnections", "GetCrawler",
            "GetCrawlerMetrics", "GetCrawlers",
            "GetDataCatalogEncryptionSettings", "GetDatabase", "GetDatabases",
            "GetDataflowGraph", "GetDevEndpoint", "GetDevEndpoints", "GetJob",
            "GetJobBookmark", "GetJobRun", "GetJobRuns", "GetJobs",
            "GetMLTaskRun", "GetMLTransform", "GetPartition", "GetPartitions",
            "GetPlan", "GetResourcePolicy", "GetSecurityConfiguration",
            "GetSecurityConfigurations", "GetTable", "GetTableVersion",
            "GetTableVersions", "GetTables", "GetTags", "GetTrigger",
            "GetTriggers", "GetUserDefinedFunction", "GetUserDefinedFunctions",
            "GetWorkflow", "GetWorkflowRun", "GetWorkflowRunProperties",
            "GetWorkflowRuns", "SearchTables"
        ],
        "list": [
            "GetMLTaskRuns", "GetMLTransforms", "ListCrawlers",
            "ListDevEndpoints", "ListJobs", "ListTriggers", "ListWorkflows"
        ],
        "tagging": ["TagResource", "UntagResource"]
    },
    "ssm": {
        "tagging": ["AddTagsToResource", "RemoveTagsFromResource"],
        "write": [
            "CancelCommand", "CancelMaintenanceWindowExecution",
            "CreateActivation", "CreateAssociation", "CreateAssociationBatch",
            "CreateDocument", "CreateMaintenanceWindow", "CreateOpsItem",
            "CreatePatchBaseline", "CreateResourceDataSync",
            "DeleteActivation", "DeleteAssociation", "DeleteDocument",
            "DeleteInventory", "DeleteMaintenanceWindow", "DeleteParameter",
            "DeleteParameters", "DeletePatchBaseline",
            "DeleteResourceDataSync", "DeregisterManagedInstance",
            "DeregisterPatchBaselineForPatchGroup",
            "DeregisterTargetFromMaintenanceWindow",
            "DeregisterTaskFromMaintenanceWindow", "LabelParameterVersion",
            "ModifyDocumentPermission", "PutComplianceItems", "PutInventory",
            "PutParameter", "RegisterDefaultPatchBaseline",
            "RegisterPatchBaselineForPatchGroup",
            "RegisterTargetWithMaintenanceWindow",
            "RegisterTaskWithMaintenanceWindow", "ResetServiceSetting",
            "ResumeSession", "SendAutomationSignal", "SendCommand",
            "StartAssociationsOnce", "StartAutomationExecution",
            "StartSession", "StopAutomationExecution", "TerminateSession",
            "UpdateAssociation", "UpdateAssociationStatus", "UpdateDocument",
            "UpdateDocumentDefaultVersion", "UpdateInstanceInformation",
            "UpdateMaintenanceWindow", "UpdateMaintenanceWindowTarget",
            "UpdateMaintenanceWindowTask", "UpdateManagedInstanceRole",
            "UpdateOpsItem", "UpdatePatchBaseline", "UpdateResourceDataSync",
            "UpdateServiceSetting"
        ],
        "read": [
            "DescribeActivations", "DescribeAssociation",
            "DescribeAssociationExecutionTargets",
            "DescribeAssociationExecutions", "DescribeAutomationExecutions",
            "DescribeAutomationStepExecutions", "DescribeAvailablePatches",
            "DescribeDocument", "DescribeDocumentParameters",
            "DescribeDocumentPermission",
            "DescribeEffectiveInstanceAssociations",
            "DescribeEffectivePatchesForPatchBaseline",
            "DescribeInstanceAssociationsStatus",
            "DescribeInstanceInformation", "DescribeInstancePatchStates",
            "DescribeInstancePatchStatesForPatchGroup",
            "DescribeInstancePatches", "DescribeInstanceProperties",
            "DescribeInventoryDeletions", "DescribeOpsItems",
            "DescribePatchGroupState", "GetAutomationExecution",
            "GetCommandInvocation", "GetConnectionStatus",
            "GetDefaultPatchBaseline", "GetDeployablePatchSnapshotForInstance",
            "GetDocument", "GetInventory", "GetInventorySchema",
            "GetMaintenanceWindow", "GetMaintenanceWindowExecution",
            "GetMaintenanceWindowExecutionTask",
            "GetMaintenanceWindowExecutionTaskInvocation",
            "GetMaintenanceWindowTask", "GetOpsItem", "GetOpsSummary",
            "GetParameter", "GetParameterHistory", "GetParameters",
            "GetParametersByPath", "GetPatchBaseline",
            "GetPatchBaselineForPatchGroup", "GetServiceSetting",
            "ListCommandInvocations", "ListCommands", "ListTagsForResource"
        ],
        "list": [
            "DescribeMaintenanceWindowExecutionTaskInvocations",
            "DescribeMaintenanceWindowExecutionTasks",
            "DescribeMaintenanceWindowExecutions",
            "DescribeMaintenanceWindowSchedule",
            "DescribeMaintenanceWindowTargets",
            "DescribeMaintenanceWindowTasks", "DescribeMaintenanceWindows",
            "DescribeMaintenanceWindowsForTarget", "DescribeParameters",
            "DescribePatchBaselines", "DescribePatchGroups",
            "DescribePatchProperties", "DescribeSessions",
            "ListAssociationVersions", "ListAssociations",
            "ListComplianceItems", "ListComplianceSummaries",
            "ListDocumentVersions", "ListDocuments",
            "ListInstanceAssociations", "ListInventoryEntries",
            "ListResourceComplianceSummaries", "ListResourceDataSync"
        ]
    },
    "comprehend": {
        "read": [
            "BatchDetectDominantLanguage", "BatchDetectEntities",
            "BatchDetectKeyPhrases", "BatchDetectSentiment",
            "BatchDetectSyntax", "ClassifyDocument",
            "DescribeDocumentClassificationJob", "DescribeDocumentClassifier",
            "DescribeDominantLanguageDetectionJob", "DescribeEndpoint",
            "DescribeEntitiesDetectionJob", "DescribeEntityRecognizer",
            "DescribeKeyPhrasesDetectionJob", "DescribeSentimentDetectionJob",
            "DescribeTopicsDetectionJob", "DetectDominantLanguage",
            "DetectEntities", "DetectKeyPhrases", "DetectSentiment",
            "DetectSyntax"
        ],
        "write": [
            "CreateDocumentClassifier", "CreateEndpoint",
            "CreateEntityRecognizer", "DeleteDocumentClassifier",
            "DeleteEndpoint", "DeleteEntityRecognizer",
            "StartDocumentClassificationJob",
            "StartDominantLanguageDetectionJob", "StartEntitiesDetectionJob",
            "StartKeyPhrasesDetectionJob", "StartSentimentDetectionJob",
            "StartTopicsDetectionJob", "StopDominantLanguageDetectionJob",
            "StopEntitiesDetectionJob", "StopKeyPhrasesDetectionJob",
            "StopSentimentDetectionJob", "StopTrainingDocumentClassifier",
            "StopTrainingEntityRecognizer", "UpdateEndpoint"
        ],
        "list": [
            "ListDocumentClassificationJobs", "ListDocumentClassifiers",
            "ListDominantLanguageDetectionJobs", "ListEndpoints",
            "ListEntitiesDetectionJobs", "ListEntityRecognizers",
            "ListKeyPhrasesDetectionJobs", "ListSentimentDetectionJobs",
            "ListTagsForResource", "ListTopicsDetectionJobs"
        ],
        "tagging": ["TagResource", "UntagResource"]
    },
    "transcribe": {
        "write": [
            "CreateVocabulary", "DeleteTranscriptionJob", "DeleteVocabulary",
            "StartStreamTranscription", "StartTranscriptionJob",
            "UpdateVocabulary"
        ],
        "read": ["GetTranscriptionJob", "GetVocabulary"],
        "list": ["ListTranscriptionJobs", "ListVocabularies"]
    },
    "firehose": {
        "write": [
            "CreateDeliveryStream", "DeleteDeliveryStream", "PutRecord",
            "PutRecordBatch", "StartDeliveryStreamEncryption",
            "StopDeliveryStreamEncryption", "TagDeliveryStream",
            "UntagDeliveryStream", "UpdateDestination"
        ],
        "list": [
            "DescribeDeliveryStream", "ListDeliveryStreams",
            "ListTagsForDeliveryStream"
        ]
    },
    "kinesis": {
        "tagging": ["AddTagsToStream", "RemoveTagsFromStream"],
        "write": [
            "CreateStream", "DecreaseStreamRetentionPeriod", "DeleteStream",
            "DeregisterStreamConsumer", "DisableEnhancedMonitoring",
            "EnableEnhancedMonitoring", "IncreaseStreamRetentionPeriod",
            "MergeShards", "PutRecord", "PutRecords", "RegisterStreamConsumer",
            "SplitShard", "UpdateShardCount"
        ],
        "read": [
            "DescribeLimits", "DescribeStream", "DescribeStreamConsumer",
            "DescribeStreamSummary", "GetRecords", "GetShardIterator",
            "ListTagsForStream", "SubscribeToShard"
        ],
        "list": ["ListShards", "ListStreamConsumers", "ListStreams"]
    },
    "dms": {
        "tagging": ["AddTagsToResource", "RemoveTagsFromResource"],
        "write": [
            "ApplyPendingMaintenanceAction", "CreateEndpoint",
            "CreateEventSubscription", "CreateReplicationInstance",
            "CreateReplicationSubnetGroup", "CreateReplicationTask",
            "DeleteCertificate", "DeleteEndpoint", "DeleteEventSubscription",
            "DeleteReplicationInstance", "DeleteReplicationSubnetGroup",
            "DeleteReplicationTask", "ImportCertificate", "ModifyEndpoint",
            "ModifyEventSubscription", "ModifyReplicationInstance",
            "ModifyReplicationSubnetGroup", "ModifyReplicationTask",
            "RebootReplicationInstance", "RefreshSchemas", "ReloadTables",
            "StartReplicationTask", "StartReplicationTaskAssessment",
            "StopReplicationTask"
        ],
        "read": [
            "DescribeAccountAttributes", "DescribeCertificates",
            "DescribeConnections", "DescribeEndpointTypes",
            "DescribeEndpoints", "DescribeEventCategories",
            "DescribeEventSubscriptions", "DescribeEvents",
            "DescribeOrderableReplicationInstances",
            "DescribeRefreshSchemasStatus",
            "DescribeReplicationInstanceTaskLogs",
            "DescribeReplicationInstances", "DescribeReplicationSubnetGroups",
            "DescribeReplicationTaskAssessmentResults",
            "DescribeReplicationTasks", "DescribeSchemas",
            "DescribeTableStatistics", "TestConnection"
        ],
        "list": ["ListTagsForResource"]
    },
    "autoscaling": {
        "write": [
            "AttachInstances", "AttachLoadBalancerTargetGroups",
            "AttachLoadBalancers", "BatchDeleteScheduledAction",
            "BatchPutScheduledUpdateGroupAction", "CompleteLifecycleAction",
            "CreateLaunchConfiguration", "DeleteAutoScalingGroup",
            "DeleteLaunchConfiguration", "DeleteLifecycleHook",
            "DeleteNotificationConfiguration", "DeletePolicy",
            "DeleteScheduledAction", "DetachInstances",
            "DetachLoadBalancerTargetGroups", "DetachLoadBalancers",
            "DisableMetricsCollection", "EnableMetricsCollection",
            "EnterStandby", "ExecutePolicy", "ExitStandby", "PutLifecycleHook",
            "PutNotificationConfiguration", "PutScalingPolicy",
            "PutScheduledUpdateGroupAction", "RecordLifecycleActionHeartbeat",
            "ResumeProcesses", "SetDesiredCapacity", "SetInstanceHealth",
            "SetInstanceProtection", "SuspendProcesses",
            "TerminateInstanceInAutoScalingGroup", "UpdateAutoScalingGroup"
        ],
        "tagging":
        ["CreateAutoScalingGroup", "CreateOrUpdateTags", "DeleteTags"],
        "list": [
            "DescribeAccountLimits", "DescribeAdjustmentTypes",
            "DescribeAutoScalingGroups", "DescribeAutoScalingInstances",
            "DescribeAutoScalingNotificationTypes",
            "DescribeLaunchConfigurations", "DescribeLifecycleHookTypes",
            "DescribeLifecycleHooks", "DescribeLoadBalancerTargetGroups",
            "DescribeLoadBalancers", "DescribeMetricCollectionTypes",
            "DescribeNotificationConfigurations", "DescribePolicies",
            "DescribeScalingActivities", "DescribeScalingProcessTypes",
            "DescribeScheduledActions", "DescribeTerminationPolicyTypes"
        ],
        "read": ["DescribeTags"]
    },
    "cognito-idp": {
        "write": [
            "AddCustomAttributes", "AdminAddUserToGroup", "AdminConfirmSignUp",
            "AdminCreateUser", "AdminDeleteUser", "AdminDeleteUserAttributes",
            "AdminDisableProviderForUser", "AdminDisableUser",
            "AdminEnableUser", "AdminForgetDevice", "AdminInitiateAuth",
            "AdminLinkProviderForUser", "AdminRemoveUserFromGroup",
            "AdminResetUserPassword", "AdminRespondToAuthChallenge",
            "AdminSetUserMFAPreference", "AdminSetUserPassword",
            "AdminSetUserSettings", "AdminUpdateAuthEventFeedback",
            "AdminUpdateDeviceStatus", "AdminUpdateUserAttributes",
            "AdminUserGlobalSignOut", "AssociateSoftwareToken",
            "ChangePassword", "ConfirmDevice", "ConfirmForgotPassword",
            "ConfirmSignUp", "CreateGroup", "CreateIdentityProvider",
            "CreateResourceServer", "CreateUserImportJob", "CreateUserPool",
            "CreateUserPoolClient", "CreateUserPoolDomain", "DeleteGroup",
            "DeleteIdentityProvider", "DeleteResourceServer", "DeleteUser",
            "DeleteUserAttributes", "DeleteUserPool", "DeleteUserPoolClient",
            "DeleteUserPoolDomain", "ForgetDevice", "ForgotPassword",
            "GlobalSignOut", "InitiateAuth", "ResendConfirmationCode",
            "RespondToAuthChallenge", "SetRiskConfiguration",
            "SetUICustomization", "SetUserMFAPreference",
            "SetUserPoolMfaConfig", "SetUserSettings", "SignUp",
            "StartUserImportJob", "StopUserImportJob",
            "UpdateAuthEventFeedback", "UpdateDeviceStatus", "UpdateGroup",
            "UpdateIdentityProvider", "UpdateResourceServer",
            "UpdateUserAttributes", "UpdateUserPool", "UpdateUserPoolClient",
            "UpdateUserPoolDomain", "VerifySoftwareToken",
            "VerifyUserAttribute"
        ],
        "read": [
            "AdminGetDevice", "AdminGetUser", "AdminListUserAuthEvents",
            "DescribeIdentityProvider", "DescribeResourceServer",
            "DescribeRiskConfiguration", "DescribeUserImportJob",
            "DescribeUserPool", "DescribeUserPoolClient",
            "DescribeUserPoolDomain", "GetCSVHeader", "GetDevice", "GetGroup",
            "GetIdentityProviderByIdentifier", "GetSigningCertificate",
            "GetUICustomization", "GetUser",
            "GetUserAttributeVerificationCode", "GetUserPoolMfaConfig"
        ],
        "list": [
            "AdminListDevices", "AdminListGroupsForUser", "ListDevices",
            "ListGroups", "ListIdentityProviders", "ListResourceServers",
            "ListTagsForResource", "ListUserImportJobs", "ListUserPoolClients",
            "ListUserPools", "ListUsers", "ListUsersInGroup"
        ],
        "tagging": ["TagResource", "UntagResource"]
    },
    "waf-regional": {
        "write": [
            "AssociateWebACL", "CreateByteMatchSet", "CreateGeoMatchSet",
            "CreateIPSet", "CreateRateBasedRule", "CreateRegexMatchSet",
            "CreateRegexPatternSet", "CreateRule", "CreateRuleGroup",
            "CreateSizeConstraintSet", "CreateSqlInjectionMatchSet",
            "CreateXssMatchSet", "DeleteByteMatchSet", "DeleteGeoMatchSet",
            "DeleteIPSet", "DeleteLoggingConfiguration", "DeleteRateBasedRule",
            "DeleteRegexMatchSet", "DeleteRegexPatternSet", "DeleteRule",
            "DeleteRuleGroup", "DeleteSizeConstraintSet",
            "DeleteSqlInjectionMatchSet", "DeleteXssMatchSet",
            "DisassociateWebACL", "PutLoggingConfiguration",
            "UpdateByteMatchSet", "UpdateGeoMatchSet", "UpdateIPSet",
            "UpdateRateBasedRule", "UpdateRegexMatchSet",
            "UpdateRegexPatternSet", "UpdateRule", "UpdateRuleGroup",
            "UpdateSizeConstraintSet", "UpdateSqlInjectionMatchSet",
            "UpdateXssMatchSet"
        ],
        "permissions_management": [
            "CreateWebACL", "DeletePermissionPolicy", "DeleteWebACL",
            "PutPermissionPolicy", "UpdateWebACL"
        ],
        "read": [
            "GetByteMatchSet", "GetChangeToken", "GetChangeTokenStatus",
            "GetGeoMatchSet", "GetIPSet", "GetLoggingConfiguration",
            "GetPermissionPolicy", "GetRateBasedRule",
            "GetRateBasedRuleManagedKeys", "GetRegexMatchSet",
            "GetRegexPatternSet", "GetRule", "GetRuleGroup",
            "GetSampledRequests", "GetSizeConstraintSet",
            "GetSqlInjectionMatchSet", "GetWebACL", "GetWebACLForResource",
            "GetXssMatchSet", "ListTagsForResource"
        ],
        "list": [
            "ListActivatedRulesInRuleGroup", "ListByteMatchSets",
            "ListGeoMatchSets", "ListIPSets", "ListLoggingConfigurations",
            "ListRateBasedRules", "ListRegexMatchSets", "ListRegexPatternSets",
            "ListResourcesForWebACL", "ListRuleGroups", "ListRules",
            "ListSizeConstraintSets", "ListSqlInjectionMatchSets",
            "ListSubscribedRuleGroups", "ListWebACLs", "ListXssMatchSets"
        ],
        "tagging": ["TagResource", "UntagResource"]
    },
    "waf": {
        "write": [
            "CreateByteMatchSet", "CreateGeoMatchSet", "CreateIPSet",
            "CreateRateBasedRule", "CreateRegexMatchSet",
            "CreateRegexPatternSet", "CreateRule", "CreateRuleGroup",
            "CreateSizeConstraintSet", "CreateSqlInjectionMatchSet",
            "CreateXssMatchSet", "DeleteByteMatchSet", "DeleteGeoMatchSet",
            "DeleteIPSet", "DeleteLoggingConfiguration", "DeleteRateBasedRule",
            "DeleteRegexMatchSet", "DeleteRegexPatternSet", "DeleteRule",
            "DeleteRuleGroup", "DeleteSizeConstraintSet",
            "DeleteSqlInjectionMatchSet", "DeleteXssMatchSet",
            "PutLoggingConfiguration", "UpdateByteMatchSet",
            "UpdateGeoMatchSet", "UpdateIPSet", "UpdateRateBasedRule",
            "UpdateRegexMatchSet", "UpdateRegexPatternSet", "UpdateRule",
            "UpdateRuleGroup", "UpdateSizeConstraintSet",
            "UpdateSqlInjectionMatchSet", "UpdateXssMatchSet"
        ],
        "permissions_management": [
            "CreateWebACL", "DeletePermissionPolicy", "DeleteWebACL",
            "PutPermissionPolicy", "UpdateWebACL"
        ],
        "read": [
            "GetByteMatchSet", "GetChangeToken", "GetChangeTokenStatus",
            "GetGeoMatchSet", "GetIPSet", "GetLoggingConfiguration",
            "GetPermissionPolicy", "GetRateBasedRule",
            "GetRateBasedRuleManagedKeys", "GetRegexMatchSet",
            "GetRegexPatternSet", "GetRule", "GetRuleGroup",
            "GetSampledRequests", "GetSizeConstraintSet",
            "GetSqlInjectionMatchSet", "GetWebACL", "GetXssMatchSet",
            "ListTagsForResource"
        ],
        "list": [
            "ListActivatedRulesInRuleGroup", "ListByteMatchSets",
            "ListGeoMatchSets", "ListIPSets", "ListLoggingConfigurations",
            "ListRateBasedRules", "ListRegexMatchSets", "ListRegexPatternSets",
            "ListRuleGroups", "ListRules", "ListSizeConstraintSets",
            "ListSqlInjectionMatchSets", "ListSubscribedRuleGroups",
            "ListWebACLs", "ListXssMatchSets"
        ],
        "tagging": ["TagResource", "UntagResource"]
    },
    "events": {
        "write": [
            "ActivateEventSource", "CreateEventBus",
            "CreatePartnerEventSource", "DeactivateEventSource",
            "DeleteEventBus", "DeletePartnerEventSource", "DeleteRule",
            "DisableRule", "EnableRule", "PutEvents", "PutPartnerEvents",
            "PutPermission", "PutTargets", "RemovePermission", "RemoveTargets"
        ],
        "read": [
            "DescribeEventBus", "DescribeEventSource",
            "DescribePartnerEventSource", "DescribeRule", "TestEventPattern"
        ],
        "list": [
            "ListEventBuses", "ListEventSources",
            "ListPartnerEventSourceAccounts", "ListPartnerEventSources",
            "ListRuleNamesByTarget", "ListRules", "ListTagsForResource",
            "ListTargetsByRule"
        ],
        "tagging": ["PutRule", "TagResource", "UntagResource"]
    },
    "acm": {
        "write": []
    },
    "elasticloadbalancing": {
        "tagging": ["AddTags", "RemoveTags"],
        "write": [
            "ApplySecurityGroupsToLoadBalancer", "AttachLoadBalancerToSubnets",
            "ConfigureHealthCheck", "CreateAppCookieStickinessPolicy",
            "CreateLBCookieStickinessPolicy", "CreateLoadBalancer",
            "CreateLoadBalancerListeners", "CreateLoadBalancerPolicy",
            "DeleteLoadBalancer", "DeleteLoadBalancerListeners",
            "DeleteLoadBalancerPolicy", "DeregisterInstancesFromLoadBalancer",
            "DetachLoadBalancerFromSubnets",
            "DisableAvailabilityZonesForLoadBalancer",
            "EnableAvailabilityZonesForLoadBalancer",
            "ModifyLoadBalancerAttributes",
            "RegisterInstancesWithLoadBalancer",
            "SetLoadBalancerListenerSSLCertificate",
            "SetLoadBalancerPoliciesForBackendServer",
            "SetLoadBalancerPoliciesOfListener"
        ],
        "read": [
            "DescribeInstanceHealth", "DescribeLoadBalancerAttributes",
            "DescribeLoadBalancerPolicies", "DescribeLoadBalancerPolicyTypes",
            "DescribeTags"
        ],
        "list": ["DescribeLoadBalancers"]
    }
}  # noqa
