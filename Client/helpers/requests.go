// Functions for making GET and POST requests to server
package helpers

// Import http requests
import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net/http"
	"net/url"
	"strings"
)

// Set server hostname and port
var server = "http://localhost:6969"

// LoginRequest makes a POST request to the server with the given username and password
func LoginRequest(username string, password string) (bool, error) {
	// Create a new form
	form := url.Values{}
	// Add username and password to form
	form.Add("username", username)
	form.Add("password", password)
	// Create a new request
	req, err := http.NewRequest("POST", server+"/login", strings.NewReader(form.Encode()))
	// Check for error
	if err != nil {
		return false, err
	}
	// Set the content type to application/x-www-form-urlencoded
	req.Header.Set("Content-Type", "application/x-www-form-urlencoded")
	// Make the request and get the response
	resp, err := http.DefaultClient.Do(req)
	// Check for error
	if err != nil {
		return false, err
	}
	// Parse response as json
	var response map[string]interface{}
	err = json.NewDecoder(resp.Body).Decode(&response)
	// Check for error
	if err != nil {
		return false, err
	}
	// Check if the response json contails error field
	if response["error"] != nil {
		return false, fmt.Errorf(response["error"].(string))
	}
	// Check if the response json contains permissions and username field. Else return false
	if response["permissions"] != nil && response["username"] != nil {
		return true, nil
	} else {
		return false, nil
	}
}

// GetDevicesRequest makes a POST request with start time and end times
func GetDevicesRequest(start string, end string) (string, error) {
	// Create a new form
	form := url.Values{}
	// Add start and end times to form
	form.Add("start_time", start)
	form.Add("end_time", end)
	// Create a new request
	req, err := http.NewRequest("POST", server+"/devices", strings.NewReader(form.Encode()))
	// Check for error
	if err != nil {
		return "error", err
	}
	// Set the content type to application/x-www-form-urlencoded
	req.Header.Set("Content-Type", "application/x-www-form-urlencoded")
	// Make the request and get the response
	resp, err := http.DefaultClient.Do(req)
	// Check for error
	if err != nil {
		return "error", err
	}
	// Get response body as string
	body, err := ioutil.ReadAll(resp.Body)
	// Check for error
	if err != nil {
		return "error", err
	}
	// Return response body as string pointer
	return string(body), nil
}

// ReserveRequest makes a POST request to the server with username, password, and reservation data (item, start, end)
func ReserveRequest(username string, password string, item string, start string, end string) (bool, error) {
	// Create a new form
	form := url.Values{}
	// Add username, password, item, start, and end to form
	form.Add("username", username)
	form.Add("password", password)
	form.Add("item", item)
	form.Add("start_time", start)
	form.Add("end_time", end)
	// Create a new request
	req, err := http.NewRequest("POST", server+"/reserve", strings.NewReader(form.Encode()))
	// Check for error
	if err != nil {
		return false, err
	}
	// Set the content type to application/x-www-form-urlencoded
	req.Header.Set("Content-Type", "application/x-www-form-urlencoded")
	// Make the request and get the response
	resp, err := http.DefaultClient.Do(req)
	// Check for error
	if err != nil {
		return false, err
	}
	// Parse response as json
	var response map[string]interface{}
	err = json.NewDecoder(resp.Body).Decode(&response)
	// Check for error
	if err != nil {
		return false, err
	}
	// Check if the response json contails error field
	if response["error"] != nil {
		return false, fmt.Errorf(response["error"].(string))
	}
	// Check if the response json contains username field. Else return false
	if response["username"] != nil {
		return true, nil
	} else {
		return false, nil
	}
}
