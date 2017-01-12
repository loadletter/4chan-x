#!/bin/bash
echo "======meta.js======="
head -30 4chan_x.user.js | tee 4chan_x.meta.js

echo "=====latest.js======"
vers=$(head -26 4chan_x.meta.js | grep "// @version" | awk '{print $3}')
versline=$(grep -n "^    version: .$vers.," 4chan_x.user.js | cut -f1 -d':')
echo -n "postMessage({version:'"$vers"'},'*')" | tee latest.js
echo

if [[ -z $versline ]]; then
	echo -e "\e[0;31mERROR: change version in Main (before CSS)\e[0m"
	exit 1
fi

echo -e "\nRemember TO TAG THE RELEASE and to have utils/config in .git/config"
