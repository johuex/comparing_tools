package main

import (
	"net/http"

	"github.com/labstack/echo/v4"
	"github.com/labstack/echo/v4/middleware"
)

func getRoot(c echo.Context) error {
	return c.String(http.StatusOK, "")
}

func main() {
	e := echo.New()

	e.Use(middleware.Logger())
	//e.Use(middleware.Recover())

	e.GET("/", getRoot)

	e.Logger.Fatal(e.Start("localhost:8000"))
}
