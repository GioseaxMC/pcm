#!/usr/bin/env bash

FILE="required.txt"

while IFS= read -r pkg; do
    [[ -z "$pkg" || "$pkg" == \#* ]] &&
continue

    pip install --only-binary=all "$pkg" || pip install "$pkg" || {
        echo "failed $pkg" 
}
done < "$FILE"
