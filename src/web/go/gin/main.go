package main

import (
	"net/http"

	"github.com/gin-gonic/gin"
)

func getRoot(c *gin.Context) {
	c.JSON(http.StatusOK, gin.H{})
}

func main() {
	gin.SetMode(gin.ReleaseMode)
	r := gin.Default()
	r.GET("/", getRoot)
	r.Run("localhost:8000")
}
