package main

import (
	"log"

	"github.com/fasthttp/router"
	"github.com/valyala/fasthttp"
)

func getRoot(ctx *fasthttp.RequestCtx) {
	ctx.SetStatusCode(200)
}

func main() {
	mux := router.New()
	mux.GET("/", getRoot)
	if err := fasthttp.ListenAndServe("localhost:8000", getRoot); err != nil {
		log.Fatalf("Error in ListenAndServe: %v", err)
	}
}
