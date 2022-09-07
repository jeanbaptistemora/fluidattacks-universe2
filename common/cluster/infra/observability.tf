# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

variable "newRelicLicenseKey" {}

resource "helm_release" "newrelic" {
  name       = "newrelic"
  repository = "https://helm-charts.newrelic.com"
  chart      = "nri-bundle"
  version    = "3.6.1"
  namespace  = "kube-system"

  set_sensitive {
    name  = "global.licenseKey"
    value = var.newRelicLicenseKey
  }

  set {
    name  = "global.cluster"
    value = local.cluster_name
  }

  set {
    name  = "newrelic-infrastructure.privileged"
    value = "true"
  }

  set {
    name  = "ksm.enabled"
    value = "true"
  }

  set {
    name  = "kubeEvents.enabled"
    value = "true"
  }

  set {
    name  = "logging.enabled"
    value = "true"
  }
}
