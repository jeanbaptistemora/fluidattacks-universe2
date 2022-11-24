resource "checkly_trigger_group" "main" {
  group_id = checkly_check_group.fluidattacks.id
}
