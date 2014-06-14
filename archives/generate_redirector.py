#!/usr/bin/env python2
import urllib2, json, os, sys

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

ARCHIVES_URL = "https://github.com/MayhemYDG/4chan-x/raw/v3/json/archives.json"
ARCHIVES_JSON = os.path.join(os.path.dirname(os.path.abspath(__file__)), "archives.json")
PRIORITIES_JSON = os.path.join(os.path.dirname(os.path.abspath(__file__)), "priorities.json")


def jsonloadf(filename):
	with open(filename) as f:
		data = json.load(f, 'utf-8')
	return data

def jsonsavef(filename, data):
	with open(filename, 'wb') as f:
		json.dump(data, f, sort_keys=True, indent=4, separators=(',', ': '), encoding='utf-8')

class Build:
	def __init__(self, outstream=sys.stdout, msgstream=sys.stderr):
		self.out = outstream
		self.msg = msgstream
		self.files = {}
		self.boards = {}
	
	def page_dl(self):
		request = urllib2.Request(ARCHIVES_URL)
		response = urllib2.urlopen(request)
		data = response.read()
		response.close()
		self.data = json.loads(data)
	
	def boards_list(self):
		f = []
		b = []
		for a in self.data:
			f += a['files']
			b += a['boards']
		self.archivedfiles = list(set(f))
		self.archivedboards = list(set(b))
	
	def find_redundant(self):
		f = {}
		b = {}
		for n, a in enumerate(self.data):
			for e in a['files']:
				if e in f:
					f[e].append(n)
				else:
					f[e] = []
			for e in a['boards']:	
				if e in b:
					b[e].append(n)
				else:
					b[e] = []
		self.singleboards = {k: v for k, v in b.iteritems() if len(v) == 1}
		self.singlefiles = {k: v for k, v in f.iteritems() if len(v) == 1}
		self.redundantboards = {k: v for k, v in b.iteritems() if len(v) > 1}
		self.redundantfiles = {k: v for k, v in f.iteritems() if len(v) > 1}
	
	def pprint(self, t):
		print >>self.msg, "%s:" % t
		for k, v in self.redundantboards.iteritems():
			#print >>self.msg, "%s --> %s" % (k, repr([(self.data[x]['name'] + " (%i)" % self.data[x]['uid']) for x in v]))
			print >>self.msg, "%s --> ", k,
			sel = None
			if k in priorities[t]:
				sel = priorities[t][k]
			for x in v:
				if sel x == sel:
					forstr = "{%s}"
				else
					forstr = '"%s"'
				print >>self.msg, forstr % self.data[x]['name'],
			if sel == None:
				print >>self.msg, "NOT SELECTED!"
			else:
				print >>self.msg
				if t == 'files':
					self.files[k] = v
				else:
					self.boards[k] = v
	
	def prioprint(self):
		separator()
		print >>self.msg, "archives:"
		for a in self.data:
			print >>self.msg, a['uid'], a['name']
		separator()
		pprint('boards')
		separator()
		pprint('files')
		separator()
					
	def merge(self):
		self.boards.update(self.singleboards)
		self.files.update(self.singlefiles)
					
	def separator(self):
		if self.msg == sys.sterr:
			print >>self.msg, "-" * 80
		
	def build(self):
		self.page_dl()
		self.boards_list()
		self.find_redundant()
		self.prioprint()
		self.merge()
		self.out.write(HEADER)
		for a in self.data:
			boardfound = False
			filefound = False
			for b in a['boards']:
				if b in self.boards and self.boards[b]['uid'] == a['uid']:
					boardfound = True
					#TODO
			for f in a['files']:
				if f in self.files and self.files[f]['uid'] == a['uid']:
					filefound = True
					#TODO
		#TODO
		
if __name__ == "__main__":
	builder = Build()
	builder.build()
