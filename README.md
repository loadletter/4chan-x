4chan-x
=======

Fork of 4chan X 2.x (MayhemYDG) made to keep it working.

##Installation
Link: ['4chan_x.user.js'](https://github.com/loadletter/4chan-x/raw/master/4chan_x.user.js)


### Firefox:

Make sure you have greasemonkey installed and just click on the previous link.

### Chrome/Chromium/Opera:

Install tampermonkey or equivalent and then just click on the previuos link.


##Changelog
- 2.40.15: Add webm support to image hover
- 2.40.13/14: Remove the video from memory when closed
- 2.40.12: Implemented support for inline webm video expansion and uploading
- 2.40.10/11: The final captcha fix (Thanks to WhatIsThisImNotGoodWithComputers)
- 2.40.9: Temporary fix to get the captcha working at least once (doesn't refresh)
- 2.40.8: Fix QR captcha load again again, fuck it
- 2.40.7: Fix #4 (/jp/ cooldown and image limit) and switched boards that used installgentoo.net to warosu.org
- 2.40.6: Remove exclude rule for catalog, add /biz/
- 2.40.5: Add exclude rule for catalog
- 2.40.4: Fix QR load again, this time because of mimetype stuff (from a diff of MayhemYDG's 3.x)
- 2.40.3: Replace the thread updater with a normal one that doesn't increment the delay for inactive threads (from ahodesuka fork)
- 2.40.2: Fixed to support new captcha loading function in the Quick Response
- 2.40.1: Fixed code tags
- 2.40.0: Fixed a change in the html that caused errors with the file info and updated to support 4cdn
- 2.39.7: Latest 2.x version from MayhemYDG


### My setup:
- Linkify: http://userscripts.org/scripts/show/87750
- Youtube link title: http://userscripts.org/scripts/show/83584
- Highlight sage: https://github.com/loadletter/resage-ext
- Inverted /a/: https://github.com/loadletter/4chan-x/raw/master/utils/inverted_a.user.js
