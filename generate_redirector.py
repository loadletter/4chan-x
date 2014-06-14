#!/usr/bin/env python2
import urllib2, json

HEADER = '''  Redirect = {
    image: function(board, filename) {
      switch (board) {
'''
POST = '''      }
    },
    post: function(board, postID) {
      switch (board) {
'''
TO = '''    to: function(data) {
      var board, threadID, url;
      if (!data.isSearch) {
        threadID = data.threadID;
      }
      board = data.board;
      switch (board) {
'''
BOTTOM = '''        default:
          if (threadID) {
            url = "//boards.4chan.org/" + board + "/";
          }
      }
      return url || null;
    },
'''

CASE = "        case '%s':"
RETURN_IMAGE = '          return "%s/" + board + "/full_image/" + filename;'
RETURN_POST = '          return "%s/_/api/chan/post/?board=" + board + "&num=" + postID;'
RETURN_REDIRECT = """         url = Redirect.path('%s', 'foolfuuka', data);
          break;
"""

JSONURL = "https://github.com/MayhemYDG/4chan-x/raw/v3/json/archives.json"



class Build:
	def __init__(self, outstream):
		self.out = outstream
		self.archivedboards = []
		self.archivedfiles = []
		self.data = None
	
	def page_dl(self):
		request = urllib2.Request(JSONURL)
		response = urllib2.urlopen(request)
		data = response.read()
		response.close()
		self.data = json.loads(data)
	
	def boards_list(self):
		f = []
		b = []
		for a in self.data:
			f += a['files']
			b += b['boards']
		self.archivedfiles = list(set(f))
		self.archivedboards = list(set(b))
	
	def build(self):
		self.page_dl()
		self.out.write(HEADER)
		
	
