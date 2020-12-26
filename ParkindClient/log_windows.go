package main

import (
	"fmt"
	"time"
)

func log(a []string) {
	t := time.Now()
	fmt.Printf("[%s]: ", t.Format("02/01/2006 15:04:05"))
	for _, foo := range a {
		fmt.Print(foo)
	}
	fmt.Println()
}

func normalLog(a ...string) {
	log(a)
}

func infoLog(a ...string) {
	log(a)
}

func warningLog(a ...string) {
	log(a)
}

func errorLog(a ...string) {
	log(a)
}
