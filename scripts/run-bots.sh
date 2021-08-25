#!/bin/bash

BASEDIR=$(dirname $0)
INPUT="${BASEDIR}/bot-info.csv"

while getopts o: opt; do
  case $opt in
    o)
      OUTDIR=$OPTARG
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      exit 1
      ;;
    :)
      echo "Option -$OPTARG requires an argument." >&2
      exit 1
      ;;
  esac
done

while IFS="," read -r field1 field2
do
    bazel run //bot:app -- --bot_username="$field1" --bot_password="$field2" --bot_output_directory="$OUTDIR" > /dev/null 2>&1 &
done < "${INPUT}"