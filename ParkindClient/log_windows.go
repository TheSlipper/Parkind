package main

import "fmt"

func log(a []string) {
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
