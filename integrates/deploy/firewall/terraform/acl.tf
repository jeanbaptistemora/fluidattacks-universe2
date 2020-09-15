module "waf_acl" {
  source               = "umotif-public/waf-webaclv2/aws"
  version              = "~> 1.4.0"
  name_prefix          = "integrates-firewall"
  allow_default_action = true

  visibility_config = {
    cloudwatch_metrics_enabled = true
    metric_name                = "integrates-firewall-main-metrics"
    sampled_requests_enabled   = true
  }

  rules = [
    {
      name            = "AWSManagedRulesAmazonIpReputationList"
      priority        = "1"
      override_action = "count"

      visibility_config = {
        cloudwatch_metrics_enabled = true
        metric_name                = "AWSManagedRulesAmazonIpReputationList-metric"
        sampled_requests_enabled   = true
      }

      managed_rule_group_statement = {
        name        = "AWSManagedRulesAmazonIpReputationList"
        vendor_name = "AWS"
      }
    },
    {
      name            = "AWSManagedRulesUnixRuleSet"
      priority        = "2"
      override_action = "count"

      visibility_config = {
        cloudwatch_metrics_enabled = true
        metric_name                = "AWSManagedRulesUnixRuleSet-metric"
        sampled_requests_enabled   = true
      }

      managed_rule_group_statement = {
        name        = "AWSManagedRulesUnixRuleSet"
        vendor_name = "AWS"
      }
    },
    {
      name            = "AWSManagedRulesKnownBadInputsRuleSet"
      priority        = "3"
      override_action = "count"

      visibility_config = {
        cloudwatch_metrics_enabled = true
        metric_name                = "AWSManagedRulesKnownBadInputsRuleSet-metric"
        sampled_requests_enabled   = true
      }

      managed_rule_group_statement = {
        name        = "AWSManagedRulesKnownBadInputsRuleSet"
        vendor_name = "AWS"
      }
    },
    {
      name            = "AWSManagedRulesLinuxRuleSet"
      priority        = "4"
      override_action = "count"

      visibility_config = {
        cloudwatch_metrics_enabled = true
        metric_name                = "AWSManagedRulesLinuxRuleSet-metric"
        sampled_requests_enabled   = true
      }

      managed_rule_group_statement = {
        name        = "AWSManagedRulesLinuxRuleSet"
        vendor_name = "AWS"
      }
    },
    {
      name            = "AWSManagedRulesWindowsRuleSet"
      priority        = "5"
      override_action = "count"

      visibility_config = {
        cloudwatch_metrics_enabled = true
        metric_name                = "AWSManagedRulesWindowsRuleSet-metric"
        sampled_requests_enabled   = true
      }

      managed_rule_group_statement = {
        name        = "AWSManagedRulesWindowsRuleSet"
        vendor_name = "AWS"
      }
    },
    {
      name            = "AWSManagedRulesCommonRuleSet"
      priority        = "5"
      override_action = "count"

      visibility_config = {
        cloudwatch_metrics_enabled = true
        metric_name                = "AWSManagedRulesCommonRuleSet-metric"
        sampled_requests_enabled   = true
      }

      managed_rule_group_statement = {
        name        = "AWSManagedRulesCommonRuleSet"
        vendor_name = "AWS"
      }
    },
  ]
}
