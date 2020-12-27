package main

import (
	"fmt"
	"net/http"
	"os"
	"time"

	"github.com/google/uuid"
)

// Handler of the client's http server
type parkindClientHandler struct {
	token uuid.UUID
}

// Implementation of the http.Handler interface. Used as a simple router that calls handlers that correspond to given urls
func (p parkindClientHandler) ServeHTTP(rw http.ResponseWriter, req *http.Request) {
	url := req.URL.String()
	infoLog(url)

	if url == "/check/" {
		connectionTestHandle(rw, req)
	} else {
		invalidUrlHandle(rw, req)
	}
}

// Sets up the http server of the parkind client and returns it
func createHttpServer() (s *http.Server) {
	// Create an http handler
	handler := parkindClientHandler{}

	// Generate a connection token for this session
	var err error
	handler.token, err = uuid.NewRandom()
	if err != nil {
		errorLog(err.Error())
		os.Exit(3)
	} else {
		infoLog("Successfully generated a new connection token:", token.String())
	}

	// Set up the server
	s = &http.Server{
		Addr:           ":8080",
		Handler:        handler,
		ReadTimeout:    10 * time.Second,
		WriteTimeout:   time.Second,
		MaxHeaderBytes: 1 << 20,
	}
	infoLog("Server listening at 127.0.0.1:8080")

	return s
}

// Url handle that handles all of the invalid incoming requests
func invalidUrlHandle(rw http.ResponseWriter, req *http.Request) {
	errorLog("invalid", req.Method, "request for URL:", req.URL.String())
	rw.WriteHeader(http.StatusBadRequest)
	fmt.Fprintf(rw, "<h1>Error 400: Bad request</h1>")
}

// Url handle that checks if the connection can be established with the given data
func connectionTestHandle(rw http.ResponseWriter, req *http.Request) {
	// TODO: Change this to if token is not true (implement the condition)
	// as of now it'll be the default until token generation is implemented
	if true {
		rw.WriteHeader(http.StatusForbidden)
		fmt.Fprintf(rw, "<h1>Error 403: Forbidden</h1>")
	} else {
		// TODO:
	}
}
