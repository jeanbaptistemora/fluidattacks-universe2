resource "kubernetes_namespace" "development" {
  metadata {
    name = "development"
  }
}

resource "kubernetes_namespace" "production" {
  metadata {
    name = "production"
  }
}
