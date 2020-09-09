resource "kubernetes_namespace" "ephemeral" {
  metadata {
    name = "ephemeral"
  }
}

resource "kubernetes_namespace" "production" {
  metadata {
    name = "production"
  }
}
