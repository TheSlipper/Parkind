package main

import (
	"flag"
	"os"
)

// singleton of the runtimeArgs
var args runtimeArgs

// Runtime arguments of the parkind client
type runtimeArgs struct {
	verbosity bool
	config    string
	login     string
	password  string
}

// Load the command line and environment arguments into the args singleton
func setUpRuntimeArgs() {
	flag.BoolVar(&args.verbosity, "verbose", false, "defines how much information should be printed out")
	flag.StringVar(&args.config, "config", "config.json", "path to the configuration file")
	flag.Parse()

	args.login = os.Getenv("LOGIN")
	args.password = os.Getenv("PASSWORD")
	if args.login == "" || args.password == "" {
		errorLog("LOGIN or PASSWORD was not provided")
		os.Exit(1)
	}
}

func main() {
	// Set up runtime arguments or stop execution if not satisfied
	setUpRuntimeArgs()
	// Set up a server and start it
	server := createHttpServer()
	err := server.ListenAndServe()
	if err != nil {
		errorLog(err.Error())
		os.Exit(2)
	}
}
