#!/bin/bash

# Assuming your Condor submission files are located in a directory named "condor_files"
condor_dir="./runFit_differential_y/asimov/"

# Check if the directory exists
if [ ! -d "$condor_dir" ]; then
  echo "Directory $condor_dir not found."
  exit 1
fi

# Change to the directory containing the Condor submission files
cd "$condor_dir" || exit

# Iterate over each file in the directory
for file in *.sub; do
  # Submit the Condor job
  condor_submit -spool "$file"
done
