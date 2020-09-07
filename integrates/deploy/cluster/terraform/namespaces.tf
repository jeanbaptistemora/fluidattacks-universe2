resource "kubernetes_namespace" "ephemeral" {
  metadata {
    name = "ephemeral"
  }
}
