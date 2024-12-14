#!/usr/bin/env python2
import requests, json, os, sys

HEADER = '''  Redirect = {
    image: function(board, filename) {
      switch (board) {
'''
POST = '''      }
    },
    post: function(board, postID) {
      switch (board) {
'''
TO = '''      }
    },
    to: function(data) {
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

CASE = "        case '%s':\n"
RETURN_IMAGE = '          return "%s/" + board + "/full_image/" + filename;\n'
RETURN_POST = '          return "%s/_/api/chan/post/?board=" + board + "&num=" + postID;\n'
RETURN_REDIRECT = """          url = Redirect.path('%s', '%s', data);
          break;
"""

#ARCHIVES_URL = "https://4chenz.github.io/archives.json/archives.json"
ARCHIVES_URL = "https://github.com/ccd0/4chan-x/raw/refs/heads/master/src/Archive/archives.json"
ARCHIVES_JSON = os.path.join(os.path.dirname(os.path.abspath(__file__)), "archives.json")
PRIORITIES_JSON = os.path.join(os.path.dirname(os.path.abspath(__file__)), "priorities.json")

ARCHIVE_HIDDEN = [29,32,35]

def jsonloadf(filename):
	with open(filename) as f:
		data = json.load(f)
	return data

def jsonsavef(filename, data):
	with open(filename, 'wb') as f:
		json.dump(data, f, sort_keys=True, indent=4, separators=(',', ': '), encoding='utf-8')

def http_protocol(a):
	dom = a['domain']
	if a['https'] and a['http']:
		return '//' + dom
	elif a['https']:
		return 'https://' + dom
	elif a['http']:
		return 'http://' + dom

class Build:
	def __init__(self, outstream=sys.stdout, msgstream=sys.stderr):
		self.out = outstream
		self.msg = msgstream
		self.files = {}
		self.boards = {}
		self.data = None
		self.priorities = jsonloadf(PRIORITIES_JSON)
	
	def page_dl(self):
		request = requests.get(ARCHIVES_URL)
		self.data = request.json()
	
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
					f[e] = [n]
			for e in a['boards']:	
				if e in b:
					b[e].append(n)
				else:
					b[e] = [n]
		def filterhidden(value):
			return filter(lambda x: not (self.data[x]['uid'] in ARCHIVE_HIDDEN and len(value) > 1), value)
		self.singleboards = {}
		self.redundantboards = {}
		for k, v in b.items():
			v2 = list(filterhidden(v))
			if len(v2) == 1:
				self.singleboards[k] = v2[0]
			if len(v2) > 1:
				self.redundantboards[k] = v2
		self.singlefiles = {}
		self.redundantfiles = {}
		for k, v in f.items():
			v2 = list(filterhidden(v))
			if len(v2) == 1:
				self.singlefiles[k] = v2[0]
			if len(v2) > 1:
				self.redundantfiles[k] = v2
	
	def pprint(self, t):
		print("%s:" % t, file=self.msg)
		if t == 'files':
			it = self.redundantfiles.items()
		else:
			it = self.redundantboards.items()
		for k, v in it:
			print("%s --> " % k, file=self.msg, end='')
			sel = None
			selfound = None
			if k in self.priorities[t]:
				sel = self.priorities[t][k]
			for x in v:
				if self.data[x]['uid'] == sel:
					forstr = "{%s}"
					selfound = x
				else:
					forstr = '"%s"'
				print(forstr % self.data[x]['name'],file=self.msg, end='')
			if sel == None or selfound == None:
				print(" NOT SELECTED!",file=self.msg)
			else:
				print('', file=self.msg)
				if t == 'files':
					self.files[k] = selfound
				else:
					self.boards[k] = selfound
	
	def prioprint(self):
		self.separator()
		print("archives:", file=self.msg)
		for a in self.data:
			if a['uid'] in ARCHIVE_HIDDEN:
				print("HIDDEN:", file=self.msg, end='')
			print(a['uid'], a['name'], file=self.msg)
		self.separator()
		self.pprint('boards')
		self.separator()
		self.pprint('files')
		self.separator()
					
	def merge(self):
		self.boards.update(self.singleboards)
		self.files.update(self.singlefiles)
					
	def separator(self):
		if self.msg == sys.stderr:
			print("-" * 80, file=self.msg)
		
	def build(self):
		if not self.data:
			self.page_dl()
		#add empty "files" if missing
		for d in self.data:
			if not "files" in d:
				d.update({"files" : []})
		#do stuff
		self.boards_list()
		self.find_redundant()
		self.prioprint()
		self.merge()
		#image
		self.out.write(HEADER)
		for n, a in enumerate(self.data):
			filefound = False
			for b in a['files']:
				if b in self.files and n == self.files[b]:
					filefound = True
					self.out.write(CASE % b)
			if filefound:
				self.out.write(RETURN_IMAGE % http_protocol(a))
		self.out.write(POST)
		#post		
		for n, a in enumerate(self.data):
			if a['software'] != 'foolfuuka':
				continue
			boardfound = False
			for b in a['boards']:
				if b in self.boards and n == self.boards[b]:
					boardfound = True
					self.out.write(CASE % b)
			if boardfound:
				self.out.write(RETURN_POST % http_protocol(a))
		self.out.write(TO)
		#redirect
		for n, a in enumerate(self.data):
			boardfound = False
			for b in a['boards']:
				if b in self.boards and n == self.boards[b]:
					boardfound = True
					self.out.write(CASE % b)
			if boardfound:
				self.out.write(RETURN_REDIRECT % (http_protocol(a), a['software']))
		self.out.write(BOTTOM)
		
		
if __name__ == "__main__":
	builder = Build()
	if len(sys.argv) == 2:
		builder.data = jsonloadf(sys.argv[1])
	builder.build()
