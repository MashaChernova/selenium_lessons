#!/bin/sh
BROWSER=""
CONCURRENCY_NUMBER=""

while [ $# -gt 0 ]
do
	case $1 in
	  --browser)
		BROWSER=$2
		shift
		shift
		;;
	  --concurrency)
		CONCURRENCY_NUMBER=$2
		shift
		shift
		;;
  	  *)
		shift
		;;
	esac
done

pytest -n $CONCURRENCY_NUMBER --browser $BROWSER
