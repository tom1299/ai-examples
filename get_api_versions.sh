#!/bin/bash

# Check if the correct number of arguments are provided
if [ "$#" -ne 2 ]; then
  echo "Usage: $0 <resource> <group>"
  exit 1
fi

resource=$1
group=$2

# Get all API versions for the specified group
api_versions=$(kubectl api-versions | grep "$group")

# Initialize an empty array to store supported versions
supported_versions=()

# Loop through each API version and check if the resource exists
for version in $api_versions; do
  # Convert from group/v1 to v1.group
  api_version=$(echo $version | awk -F'/' '{print $2"."$1}')
  echo "Checking version: $api_version"
  if kubectl get "$resource.$api_version" &> /dev/null; then
    supported_versions+=("$version")
  fi
done

# Print the supported versions
if [ ${#supported_versions[@]} -eq 0 ]; then
  echo "No supported API versions found for $resource."
else
  echo "Supported API versions for $resource:"
  for version in "${supported_versions[@]}"; do
    echo "$version"
  done
fi