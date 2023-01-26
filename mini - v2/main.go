package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"os/exec"
	"time"

	"github.com/gorilla/mux"
	"github.com/gorilla/websocket"
)

// ------------------------------------------------------------------------
// Logger is a middleware handler that does request logging
// ------------------------------------------------------------------------
type Logger struct {
	handler http.Handler
}

// ------------------------------------------------------------------------
// ServeHTTP handles the request by passing it to the real
// handler and logging the request details
// ------------------------------------------------------------------------
func (l *Logger) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	//Allow CORS here By * or specific origin
	w.Header().Set("Access-Control-Allow-Origin", "*")
	w.Header().Set("Access-Control-Allow-Headers", "Content-Type,Content-Length, Authorization, Accept,X-Requested-With")
	w.Header().Set("Access-Control-Allow-Methods", "PUT,POST,GET,DELETE,OPTIONS")
	w.Header().Set("Access-Control-Allow-Credentials", "true")

	start := time.Now()
	fmt.Printf("%s %s %v\n", r.Method, r.URL.Path, time.Since(start))
	l.handler.ServeHTTP(w, r)
}

// ------------------------------------------------------------------------
// NewLogger constructs a new Logger middleware handler
// ------------------------------------------------------------------------
func NewLogger(handlerToWrap http.Handler) *Logger {
	return &Logger{handlerToWrap}
}

// main function of the program
func main() {
	fmt.Println("webserver started!!")

	addr := ":3333"
	//init new router
	mux := mux.NewRouter()
	// request middleware for the request processing
	wapmux := NewLogger(mux)
	// add mux router the router path
	mux.HandleFunc("/", Root).Methods("GET")
	mux.HandleFunc("/ws", WsEndpoint)

	fmt.Println("server is listening on port", addr)
	//servser listening on specified port as we configured
	log.Fatal(http.ListenAndServe(addr, wapmux))
}

// --------------------------------------------------------------------------
// API root msg
func Root(res http.ResponseWriter, req *http.Request) {
	// cmd := exec.Command("python", "./eye_mouse.py")
	// stdout, err := cmd.StdoutPipe()

	// if err != nil {
	// 	log.Fatal(err)
	// }

	// if err := cmd.Start(); err != nil {
	// 	log.Fatal(err)
	// }

	// data, err := ioutil.ReadAll(stdout)

	// if err != nil {
	// 	log.Fatal(err)
	// }

	// if err := cmd.Wait(); err != nil {
	// 	log.Fatal(err)
	// }

	// fmt.Printf("%s\n", data)

	Result(res, Message{Message: "welcome to the AI Desktop API service", Status: true, Data: nil})
}

var upgrader = websocket.Upgrader{
	ReadBufferSize:  1024,
	WriteBufferSize: 1024,
	CheckOrigin: func(r *http.Request) bool {
		return true
	},
}

type wsMessage struct {
	Event string      `json:"event"`
	Data  interface{} `json:"data"`
}

func WsEndpoint(w http.ResponseWriter, r *http.Request) {
	// upgrade this connection to a WebSocket
	// connection
	ws, err := upgrader.Upgrade(w, r, nil)
	if err != nil {
		log.Println(err)
	}
	log.Println("Client Connected")
	err = ws.WriteMessage(1, []byte("welcome to the AI Desktop ws service"))
	if err != nil {
		log.Println(err)
	}
	// listen indefinitely for new messages coming
	// through on our WebSocket connection
	reader(ws)
}

// main reader for the lab container access and authentication
func reader(conn *websocket.Conn) {
	for {
		// read the message from the user
		_, p, err := conn.ReadMessage()
		if err != nil {
			log.Println(err)
			return
		}
		var data wsMessage
		json.Unmarshal(p, &data)

		go func() {
			switch data.Event {
			case "eye":
				fmt.Println("eye")
				cmd := exec.Command("python", "./eye.py")
				if stdout, err := cmd.StdoutPipe(); err != nil {
					log.Fatal(err)
				} else {
					if err := cmd.Start(); err != nil {
						log.Fatal(err)
					}
					if data, err := ioutil.ReadAll(stdout); err != nil {
						log.Fatal(err)
					} else {
						if err := cmd.Wait(); err != nil {
							log.Fatal(err)
						}
						d := fmt.Sprintf("%s\n", data)
						sendData(conn, "eye", d)
					}
				}
			case "hand":
				fmt.Println("hand")
				cmd := exec.Command("python", "./hand.py")
				if stdout, err := cmd.StdoutPipe(); err != nil {
					log.Fatal(err)
				} else {
					if err := cmd.Start(); err != nil {
						log.Fatal(err)
					}
					if data, err := ioutil.ReadAll(stdout); err != nil {
						log.Fatal(err)
					} else {
						if err := cmd.Wait(); err != nil {
							log.Fatal(err)
						}
						d := fmt.Sprintf("%s\n", data)
						sendData(conn, "eye", d)
					}
				}
			case "voice":
				fmt.Println("voice")
				cmd := exec.Command("python", "./voice.py")
				if stdout, err := cmd.StdoutPipe(); err != nil {
					log.Fatal(err)
				} else {
					if err := cmd.Start(); err != nil {
						log.Fatal(err)
					}
					if data, err := ioutil.ReadAll(stdout); err != nil {
						log.Fatal(err)
					} else {
						if err := cmd.Wait(); err != nil {
							log.Fatal(err)
						}
						d := fmt.Sprintf("%s\n", data)
						sendData(conn, "eye", d)
					}
				}
			}
		}()
	}
}

// for sending data throught the web socket
// func sendData(conn *websocket.Conn, event, msg string) {

// 	if err := conn.WriteMessage(1, []byte(fmt.Sprint("{\"event\":\"", event, "\",\"msg\":\"", msg, "\"}"))); err != nil {
// 		log.Println(err)
// 		return
// 	}
// }

type Message struct {
	Message string      `json:"message"`
	Status  bool        `json:"status"`
	Data    interface{} `json:"data"`
}

func Result(w http.ResponseWriter, msg Message) {
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(msg)
}

// for sending data throught the web socket
func sendData(conn *websocket.Conn, event, msg string) {
	if err := conn.WriteMessage(1, []byte(fmt.Sprint("{\"event\":\"", event, "\",\"msg\":\"", msg, "\"}"))); err != nil {
		log.Println(err)
		return
	}
}
