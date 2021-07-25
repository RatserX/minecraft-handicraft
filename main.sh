#!/bin/sh
[ "$UID" -eq 0 ] || exec sudo bash "$0" "$@"

# Python
pip3 install -r "requirements.txt"
python "./src/main.py"
# Finish
read -rsn1 -p "Press any key to continue . . ."
echo ""
