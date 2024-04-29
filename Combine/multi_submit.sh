#!/bin/bash

# Check if differential_variable is provided as an argument
# Check if both variables are provided as arguments
if [ $# -ne 2 ]; then
  echo "Usage: $0 <differential_variable> <sub_dir>"
  exit 1
fi
# Assign the provided argument to differential_variable
differential_variable="$1"
sub_dir="$2"

# Assuming your Condor submission files are located in a directory named "condor_files"
condor_dir="./runFits_${differential_variable}/${sub_dir}/"

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
