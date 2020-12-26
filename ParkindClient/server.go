package main

import (
	"fmt"
	"html"
	"net/http"
	"time"
)

// func httpRouter(w http.ResponseWriter, r *http.Request) {
// 	fmt.Fprintf(w, "Hello, %q", html.EscapeString(r.URL.Path))
// }

type parkindClientHandler struct {
	// ServeHTTP()
}

func (p parkindClientHandler) ServeHTTP(rw http.ResponseWriter, req *http.Request) {
	fmt.Fprintf(rw, "Hello, %q", html.EscapeString(req.URL.Path))
}

func createHttpServer() (s *http.Server) {
	handler := parkindClientHandler{}
	s = &http.Server{
		Addr:           ":8080",
		Handler:        handler,
		ReadTimeout:    10 * time.Second,
		WriteTimeout:   10 * time.Second,
		MaxHeaderBytes: 1 << 20,
	}
	return s
}
