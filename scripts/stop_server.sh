#!/bin/bash

process_id=$(pgrep 'start_server.sh')
# pkill -15 -P ${process_id}
# echo "Server stopped"

list_descendants ()
{
    for var in "$@"
    do
        local children=$(ps -o pid= --ppid "$var")

        for pid in $children
        do
            list_descendants "$pid"
        done

        echo "$children"
    done
}

kill $(list_descendants ${process_id})