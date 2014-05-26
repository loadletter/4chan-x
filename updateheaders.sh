#!/bin/bash
echo -e "\e[0;31mREMEMBER TO CHANGE version: @ LINE 5991 (before CSS) and TO TAG THE RELEASE\e[0m"
echo "======meta.js======="
head -26 4chan_x.user.js | tee 4chan_x.meta.js

echo "=====latest.js======"
vers=$(head -26 4chan_x.meta.js | grep "// @version" | awk '{print $3}')
echo -n "postMessage({version:'"$vers"'},'*')" | tee latest.js
echo
