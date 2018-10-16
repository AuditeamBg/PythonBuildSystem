#!/bin/sh

#this script populates the flash directory, but should not be used as an entry point, use /plugins/MR2/populate_results.py

cd ${WORKSPACE}

date1=$(date +"%s")

echo "#Additional population this should be fixed someday"

date2=$(date +"%s")
diff=$(($date2-$date1))

echo "Result population took $(($diff / 60)) minutes and $(($diff % 60)) seconds."

