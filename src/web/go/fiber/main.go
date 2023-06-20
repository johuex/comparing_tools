package main

import (
	"github.com/gofiber/fiber/v2"
)

func getRoot(c *fiber.Ctx) error {
	return c.SendStatus(200)
}

func main() {
	app := fiber.New()
	app.Get("/", getRoot)

	app.Listen("localhost:8000")
}
