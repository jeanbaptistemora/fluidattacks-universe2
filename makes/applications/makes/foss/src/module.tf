module "github_makes" {
  source = "../../../../../makes/applications/makes/foss/modules/github"

  token = var.GITHUB_API_TOKEN
}
