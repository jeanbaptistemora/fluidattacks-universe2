resource "skims" "worcester" {
    language = "EN"

    path {
        include = ["test", "test"]
        exclude = ["test/data/config", "test/data/config"]
    }
}
