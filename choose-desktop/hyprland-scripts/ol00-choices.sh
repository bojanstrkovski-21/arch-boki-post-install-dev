#!/bin/bash
 

 # Get the current directory 
 
 DIR="$( cd "$( dirname "${BASH\_SOURCE\[0\]}" )" >/dev/null 2>&1 && pwd )" 
 
 # Iterate over all .sh files in the current directory 

for script in "$DIR"/\*.sh; do
 
 # Make sure the file is a regular file (not a directory) and ends with .sh 
 
  if [[ -f "$script" && "$script" != "$0" ]]; then 
 
 # Ensure the script is executable 
 
  		if [[ ! -x "$script" ]]; then 
  	   		
          echo "Making script executable: $script" 

  	   		chmod +x "$script" 

  		fi 
  	
  		echo "Running script: $script" 
  	
    # Execute the script 

  		"$script" 
  	
  	echo "Script $script finished with exit code $?" 
  
  	echo "-------------------------------------" 
  fi
done