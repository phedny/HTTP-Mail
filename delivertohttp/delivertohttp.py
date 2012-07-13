from email.parser import Parser
from hashlib import sha256
import couchdb
import json
import sys

if len(sys.argv) < 3:
	sys.exit()

def handle_part(part):
	headers = {}
	for h in part.keys():
		this_header = []
		for v in part.get_all(h):
			this_header.append(v)
		headers[h] = this_header
	part_obj = {'headers': headers}
	if part.is_multipart():
		parts = []
		for p in part.get_payload():
			parts.append(handle_part(p))
		part_obj['parts'] = parts
	else:
		payload = part.get_payload(decode = True)
		f = sha256(payload).hexdigest()
		with open("out/" + f, "w") as ff:
			ff.write(payload)
		part_obj['content'] = 'http://localhost/~mark/httpmail/' + f
	return part_obj

s = couchdb.Server(sys.argv[1])
db = s[sys.argv[2]]

m = Parser().parse(sys.stdin)
print m.get_unixfrom()
db.save(handle_part(m))

