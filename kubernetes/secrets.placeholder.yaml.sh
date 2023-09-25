# This file is left blank purposefully.
# Secrets will only be available on local dev and/or via KeyVault

# to load env file, a script might be helpful

#!/bin/bash
# k8cmd="kubectl create secret generic app-secrets-001"

# while read line; do
#     # Skip empty lines
#     if [[ -z $line ]]; then
#         continue
#     fi

#     name=$(echo $line | cut -d'=' -f1)
#     value=$(echo $line | cut -d'=' -f2-)

#     # Check name and value are not empty
#     if [[ -z $name || -z $value ]]; then
#         continue
#     fi

#     k8cmd="$k8cmd\\n--from-literal=$name=$value"
# done < env.prod.env

# echo $k8cmd
