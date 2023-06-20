package main

import "github.com/aerogo/aero"

func getRoot(ctx aero.Context) error {
	ctx.SetStatus(200)
	return ctx.String("")
}

func main() {
	app := aero.New()
	app.Get("/", getRoot)
	app.Run()
}
