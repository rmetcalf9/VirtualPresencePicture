#!/bin/bash

echo "Waiting to allow other container to start..."
sleep 3
echo "Wait over"
nosetests --rednose /ext_volume
exit $?
