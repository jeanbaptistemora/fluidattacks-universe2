# -*- coding: utf-8 -*-

import cf_creator

STACK_FILE = "/tmp/stackname_old.txt"

lines = open(STACK_FILE, "r")
stackname = lines.readlines()[0]

cf_creator.delete_stackcf(stackname)
