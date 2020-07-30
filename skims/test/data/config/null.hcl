resource "skims" "unittesting" {
    language = "EN"
}

resource "skims" "worcester" {
    language = "EN"

    path {
        include = []
        exclude = []
    }
}
