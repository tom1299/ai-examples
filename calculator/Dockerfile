# Use the official Golang image to create a build artifact.
FROM golang:1.23-alpine AS builder

# Set the Current Working Directory inside the container
WORKDIR /app

# Copy go mod and sum files
COPY go.mod ./
COPY go.sum ./

# Download all dependencies. Dependencies will be cached if the go.mod and go.sum files are not changed
RUN go mod download

# Copy the source from the current directory to the Working Directory inside the container
COPY . .

# Build the Go app
RUN go build -o calculator-app ./main.go

# Start a new stage from scratch
FROM alpine:latest

# Add a non-root user with GID > 10000
RUN addgroup -g 10001 calc-group && adduser -D -u 10001 -G calc-group -D calc-user

# Copy the Pre-built binary file from the previous stage
COPY --from=builder /app/calculator-app /usr/local/bin/calculator

# Change ownership and permissions
RUN chown -R calc-user:calc-group /usr/local/bin/calculator && chmod +x /usr/local/bin/calculator

# Switch to the non-root user
USER calc-user

# Command to run the executable
ENTRYPOINT ["calculator"]