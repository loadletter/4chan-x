// ==UserScript==
// @name        Inverted /a/
// @namespace   loadletter
// @description Board title on /a/ becomes /ɐ/ - Animu & Mango
// @match       *://boards.4chan.org/a/*
// @version     1
// @grant       none
// ==/UserScript==

document.getElementsByClassName("boardTitle")[0].innerHTML = "/ɐ/ - Animu & Mango";
