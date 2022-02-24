variable "newRelicLicenseKey" {}
variable "newRelicPixieApiKey" {}
variable "newRelicPixieDeployKey" {}

variable "pixie_crd_commit" {
  default = "eea8fff0ec9032ef47bc862baae6470812352d44"
}

data "http" "pixie_viziers_yaml" {
  url = "https://raw.githubusercontent.com/pixie-io/pixie/${var.pixie_crd_commit}/k8s/operator/crd/base/px.dev_viziers.yaml"
}

data "http" "pixie_olm_yaml" {
  url = "https://raw.githubusercontent.com/pixie-io/pixie/${var.pixie_crd_commit}/k8s/operator/helm/crds/olm_crd.yaml"
}

data "kubectl_file_documents" "pixie_viziers_documents" {
  content = data.http.pixie_viziers_yaml.body
}

data "kubectl_file_documents" "pixie_olm_documents" {
  content = data.http.pixie_olm_yaml.body
}

resource "kubectl_manifest" "pixie_viziers_crd" {
  for_each  = data.kubectl_file_documents.pixie_viziers_documents.manifests
  yaml_body = each.value
}

resource "kubectl_manifest" "pixie_olm_crd" {
  for_each  = data.kubectl_file_documents.pixie_olm_documents.manifests
  yaml_body = each.value
}

resource "helm_release" "newrelic" {
  name       = "newrelic"
  repository = "https://helm-charts.newrelic.com"
  chart      = "nri-bundle"
  version    = "3.4.0"
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
    name  = "kubeEvents.enabled"
    value = "true"
  }

  set {
    name  = "logging.enabled"
    value = "true"
  }

  set_sensitive {
    name  = "newrelic-pixie.apiKey"
    value = var.newRelicPixieApiKey
  }

  set_sensitive {
    name  = "pixie-chart.deployKey"
    value = var.newRelicPixieDeployKey
  }

  set {
    name  = "newrelic-pixie.enabled"
    value = "true"
  }

  set {
    name  = "pixie-chart.enabled"
    value = "true"
  }

  set {
    name  = "pixie-chart.clusterName"
    value = var.cluster_name
  }

  set {
    name  = "pixie-chart.pemMemoryLimit"
    value = "1Gi"
  }

  set {
    name  = "newrelic-pixie.excludeNamespacesRegex"
    value = "default|development|kube-system"
  }
}
