package main

import (
	"net/http"
	"net/url"
	"testing"
	// "github.com/google/uuid"
)

// Tests the token verification mechanism
func TestTokenCheck(t *testing.T) {
	// Create and start server
	var token string
	go func() {
		server := createHttpServer()
		handler := server.Handler.(parkindClientHandler)
		token = handler.token.String()
		err := server.ListenAndServe()
		if err != nil {
			panic(err)
		}
	}()

	t.Log(token)
	_, err := http.PostForm("http://127.0.0.1:8080/check/", url.Values{
		"token": {token},
	})
	if err != nil {
		panic(err)
	}
}
