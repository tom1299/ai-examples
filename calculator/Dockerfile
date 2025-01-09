# Use the official Golang image to create a build artifact.
FROM golang:1.23-alpine AS builder

# Set the Current Working Directory inside the container
WORKDIR /app

# Copy go mod and sum files
COPY go.mod ./

# Download all dependencies. Dependencies will be cached if the go.mod and go.sum files are not changed
RUN go mod download

# Copy the source from the current directory to the Working Directory inside the container
COPY . .

# Build the Go app
RUN go build -o calculator ./cmd/main.go

# Start a new stage from scratch
FROM alpine:latest

# Add a non-root user
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

# Copy the Pre-built binary file from the previous stage
COPY --from=builder /app/calculator /usr/local/bin/calculator

# Change ownership and permissions
RUN chown -R appuser:appgroup /usr/local/bin/calculator

# Switch to the non-root user
USER appuser

# Command to run the executable
ENTRYPOINT ["calculator"]