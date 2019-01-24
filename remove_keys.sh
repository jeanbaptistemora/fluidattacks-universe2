#!/bin/bash

for i in {1..10}; do
	for pattern in bwapp unittesting oneshottest; do
		for key in $(redis-cli -c -h ${FI_REDIS_SERVER} --scan --pattern *${pattern}*); do
			echo "Removing key ${key}..."
			redis-cli -c -h ${FI_REDIS_SERVER} unlink ${key}
		done
	done
done
