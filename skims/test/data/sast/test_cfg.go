package main

import (
	"errors"
	"fmt"
	"log"
	"net/http"

	"github.com/julienschmidt/httprouter"
)

type Class struct{}

func (this *Class) CapturePanic(h httprouter.Handle) {
	r := recover()
	if r != nil {
		switch t := r.(type) {
		case string:
			err = errors.New(t)
		case error:
			err = t
		default:
			err = errors.New("Unknown error")
		}
		log.Println(err.Error())
		http.Error(w, err.Error(), http.StatusInternalServerError)
	}
}

func CheckLevel(r *http.Request) bool {
	level := GetCookie(r, "Level")
	if level == "" || level == "low" {
		return false //set default level to low
	} else if level == "high" {
		return true //level == high
	} else {
		return false // level == low
	}
}

func DeleteCookie(w http.ResponseWriter, cookies []string){
	for _,name := range cookies{
		cookie := &http.Cookie{
			Name:     name,
			Value:    "",
			Expires: time.Unix(0, 0),
		}
		http.SetCookie(w, cookie)
	}
}

func getOSVersion() string {
	switch os := runtime.GOOS; os{
	case "darwin":
		return "OS X"
	case "linux":
		return "Linux"
	default:
		fmt.Printf("%s.", os)
	}
	return ""
}
