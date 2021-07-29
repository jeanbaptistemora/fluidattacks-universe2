package main

import (
	"crypto/des"
	"crypto/md4"
	"crypto/md5"
	"golang.org/x/crypto/ripemd160"
	"crypto/sha1"
	"crypto/sha512"
)

func main() {

	Hripemd:= ripemd160.New()
	Hmd4 = md4.New()
	Hmd5 = md5.New()
	Hsha1 := sha1.New()
	Hsha512 := sha512.New()

	ede2Key := []byte("example key 1234")

	Cdes, _ := des.NewTripleDESCipher(ede2Key)
}
