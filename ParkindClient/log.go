// +build linux darwin freebsd netbsd openbsd

package main

import (
	"fmt"
	"time"
)

const (
	colorDefault = "\033[0m"
	colorRed     = "\033[31m"
	colorGreen   = "\033[32m"
	colorYellow  = "\033[33m"
	colorPurple  = "\033[35m"
)

func log(a []string) {
	t := time.Now()
	fmt.Printf("[%s]:", t.Format("02/01/2006 15:04:05"))
	for _, foo := range a {
		fmt.Print(" ", foo)
	}
	fmt.Println()
}

func normalLog(a ...string) {
	fmt.Printf(colorDefault)
	log(a)
}

func infoLog(a ...string) {
	if !args.verbosity {
		return
	}

	fmt.Printf(colorPurple)
	log(a)
}

func successLog(a ...string) {
	fmt.Printf(colorGreen)
	log(a)
}

func warningLog(a ...string) {
	fmt.Printf(colorYellow)
	log(a)
}

func errorLog(a ...string) {
	fmt.Printf(colorRed)
	log(a)
}
