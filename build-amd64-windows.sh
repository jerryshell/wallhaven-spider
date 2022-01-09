#!/usr/bin/env bash
CGO_ENABLED=0 GOOS=windows GOARCH=amd64 go build -ldflags "-s -w" -o wallhaven-spider-amd64-windows
