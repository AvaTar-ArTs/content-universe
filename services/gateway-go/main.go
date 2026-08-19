package main

import (
  "encoding/json"
  "net/http"
)

func health(w http.ResponseWriter, _ *http.Request) {
  w.Header().Set("Content-Type", "application/json")
  _ = json.NewEncoder(w).Encode(map[string]string{"service":"creativeos-gateway","status":"ready"})
}

func main() {
  http.HandleFunc("/health", health)
  _ = http.ListenAndServe(":8080", nil)
}
