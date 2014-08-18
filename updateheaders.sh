#!/bin/bash
echo "======meta.js======="
head -26 4chan_x.user.js | tee 4chan_x.meta.js

echo "=====latest.js======"
vers=$(head -26 4chan_x.meta.js | grep "// @version" | awk '{print $3}')
versline=$(grep -n "^    version: .$vers.," 4chan_x.user.js | cut -f1 -d':')
echo -n "postMessage({version:'"$vers"'},'*')" | tee latest.js
echo
echo -e "\e[0;31mREMEMBER TO CHANGE version @ LINE $versline (before CSS) and TO TAG THE RELEASE and to have utils/config in .git/config\e[0m"
