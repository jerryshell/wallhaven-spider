#!/usr/bin/env bash
CGO_ENABLED=0 GOOS=darwin GOARCH=amd64 go build -ldflags "-s -w" -o wallhaven-spider-amd64-darwin
