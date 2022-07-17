package main

import (
	"context"
	"fmt"

	helper "github.com/acheong08/SimpleResv/Client/helpers"
	runtime "github.com/wailsapp/wails/v2/pkg/runtime"
)

// App struct
type App struct {
	ctx      context.Context
	username string
	password string
}

// NewApp creates a new App application struct
func NewApp() *App {
	return &App{}
}

// startup is called when the app starts. The context is saved
// so we can call the runtime methods
func (a *App) startup(ctx context.Context) {
	// Set context
	a.ctx = ctx
}

// Greet returns a greeting for the given name
func (a *App) Greet(name string) string {
	return fmt.Sprintf("Hello %s, It's show time!", name)
}

// Login takes a username and password and returns a bool indicating if the login was successful
func (a *App) Login(username string, password string) bool {
	loginStatus, err := helper.LoginRequest(username, password)
	if err != nil {
		return false
	}
	// If successful, store username and password and return true
	if loginStatus {
		// Store username and password
		a.username = username
		a.password = password
		// Change screen dimensions to prepare for home page
		runtime.WindowSetSize(a.ctx, 1280, 800)
		return true
	}
	// If not successful, return false
	return false
}

// Devices takes a start and end time and returns a json list of devices
func (a *App) Devices(start string, end string) string {
	devices, err := helper.GetDevicesRequest(start, end)
	if err != nil {
		fmt.Println(err)
		// Return error as json
		return `{"error": "` + err.Error() + `"}`
	}
	return devices
}
