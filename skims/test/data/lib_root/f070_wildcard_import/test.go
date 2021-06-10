package main

import "package1"
import pkg2 "package2"
import .    "package3"

import (
	"math/rand"
	"fmt"
	pkg4 "package4"
	.    "package5"
	_    "package6"
)

func main() {
    fmt.Println(rand.Int())
}
