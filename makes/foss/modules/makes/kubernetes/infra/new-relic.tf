variable "newRelicLicenseKey" {}

variable "pixie_crd_commit" {
  default = "eea8fff0ec9032ef47bc862baae6470812352d44"
}

data "http" "pixie_viziers_yaml" {
  url = "https://raw.githubusercontent.com/pixie-io/pixie/${var.pixie_crd_commit}/k8s/operator/crd/base/px.dev_viziers.yaml"
}

data "http" "pixie_olm_yaml" {
  url = "https://raw.githubusercontent.com/pixie-io/pixie/${var.pixie_crd_commit}/k8s/operator/helm/crds/olm_crd.yaml"
}

resource "kubectl_manifest" "pixie_viziers_crd" {
  yaml_body = data.http.pixie_viziers_yaml.body
}

resource "kubectl_manifest" "pixie_olm_crd" {
  yaml_body = data.http.pixie_olm_yaml.body
}

resource "helm_release" "newrelic" {
  name       = "newrelic"
  repository = "https://helm-charts.newrelic.com"
  chart      = "nri-bundle"
  version    = "3.3.2"
  namespace  = "kube-system"

  set_sensitive {
    name  = "global.licenseKey"
    value = var.newRelicLicenseKey
  }

  set {
    name  = "global.cluster"
    value = var.cluster_name
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
    name  = "prometheus.enabled"
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
