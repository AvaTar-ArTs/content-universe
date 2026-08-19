package main

import (
  "net/http"
  "net/http/httptest"
  "testing"
)

func TestHealth(t *testing.T) {
  response := httptest.NewRecorder()
  health(response, httptest.NewRequest(http.MethodGet, "/health", nil))
  if response.Code != http.StatusOK {
    t.Fatalf("expected 200, got %d", response.Code)
  }
  if response.Header().Get("Content-Type") != "application/json" {
    t.Fatalf("expected JSON content type")
  }
}
