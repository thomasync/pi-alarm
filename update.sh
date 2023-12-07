#!/bin/bash

get_version() {
	file_path="pialarm/__init__.py"
    local result=$(grep -o '"[^"]*"' "$file_path" | sed 's/"//g')
    echo $result
}

version_before=$(get_version)
git pull https://github.com/thomasync/pi-alarm
version_after=$(get_version)

if [ "$version_before" != "$version_after" ]; then
	echo "Updated from $version_before to $version_after"
	pm2 restart pi-alarm
fi