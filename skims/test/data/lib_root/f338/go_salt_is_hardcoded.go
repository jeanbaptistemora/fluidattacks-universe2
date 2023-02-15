package main

import (
	"crypto/sha256"
	"encoding/hex"
	"math/rand"
	"time"
)



var salt string = "HARDCODED_SALT"

func hashPasswordHardcoded(password string) string {
	h := sha256.New()
	h.Write([]byte(password + salt))
	return hex.EncodeToString(h.Sum(nil))
}
