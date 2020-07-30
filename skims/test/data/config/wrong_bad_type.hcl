resource "skims" "worcester" {
    language = "EN"

    path {
        include = "test"
        exclude = ["test"]
    }
}
