resource "aws_wafv2_web_acl" "integrates_firewall" {
  name        = var.name
  description = "Firewall for Integrates ephemeral and production environments"
  scope       = "REGIONAL"

  default_action {
    allow {}
  }

  visibility_config {
    cloudwatch_metrics_enabled = true
    metric_name                = "${var.name}-main-metrics"
    sampled_requests_enabled   = true
  }

  rule {
    name     = "AWSManagedRulesAmazonIpReputationList"
    priority = 1
    override_action {
      none {}
    }
    statement {
      managed_rule_group_statement {
        name        = "AWSManagedRulesAmazonIpReputationList"
        vendor_name = "AWS"
      }
    }
    visibility_config {
      cloudwatch_metrics_enabled = true
      metric_name                = "${var.name}-AWSManagedRulesAmazonIpReputationList-metrics"
      sampled_requests_enabled   = true
    }
  }

  rule {
    name     = "AWSManagedRulesUnixRuleSet"
    priority = 2
    override_action {
      none {}
    }
    statement {
      managed_rule_group_statement {
        name        = "AWSManagedRulesUnixRuleSet"
        vendor_name = "AWS"
        excluded_rule {
          name = "UNIXShellCommandsVariables_BODY"
        }
      }
    }
    visibility_config {
      cloudwatch_metrics_enabled = true
      metric_name                = "${var.name}-AWSManagedRulesUnixRuleSet-metrics"
      sampled_requests_enabled   = true
    }
  }

  rule {
    name     = "AWSManagedRulesKnownBadInputsRuleSet"
    priority = 3
    override_action {
      none {}
    }
    statement {
      managed_rule_group_statement {
        name        = "AWSManagedRulesKnownBadInputsRuleSet"
        vendor_name = "AWS"
        excluded_rule {
          name = "Host_localhost_HEADER"
        }
      }
    }
    visibility_config {
      cloudwatch_metrics_enabled = true
      metric_name                = "${var.name}-AWSManagedRulesKnownBadInputsRuleSet-metrics"
      sampled_requests_enabled   = true
    }
  }

  rule {
    name     = "AWSManagedRulesLinuxRuleSet"
    priority = 4
    override_action {
      none {}
    }
    statement {
      managed_rule_group_statement {
        name        = "AWSManagedRulesLinuxRuleSet"
        vendor_name = "AWS"
        excluded_rule {
          name = "LFI_BODY"
        }
      }
    }
    visibility_config {
      cloudwatch_metrics_enabled = true
      metric_name                = "${var.name}-AWSManagedRulesLinuxRuleSet-metrics"
      sampled_requests_enabled   = true
    }
  }

  rule {
    name     = "AWSManagedRulesCommonRuleSet"
    priority = 5
    override_action {
      none {}
    }
    statement {
      managed_rule_group_statement {
        name        = "AWSManagedRulesCommonRuleSet"
        vendor_name = "AWS"
        excluded_rule {
          name = "NoUserAgent_HEADER"
        }
        excluded_rule {
          name = "SizeRestrictions_BODY"
        }
        excluded_rule {
          name = "GenericRFI_QUERYARGUMENTS"
        }
        excluded_rule {
          name = "UserAgent_BadBots_HEADER"
        }
        excluded_rule {
          name = "GenericRFI_BODY"
        }
        excluded_rule {
          name = "RestrictedExtensions_QUERYARGUMENTS"
        }
        excluded_rule {
          name = "CrossSiteScripting_BODY"
        }
        excluded_rule {
          name = "EC2MetaDataSSRF_BODY"
        }
        excluded_rule {
          name = "GenericLFI_BODY"
        }
      }
    }
    visibility_config {
      cloudwatch_metrics_enabled = true
      metric_name                = "${var.name}-AWSManagedRulesCommonRuleSet-metrics"
      sampled_requests_enabled   = true
    }
  }
}
