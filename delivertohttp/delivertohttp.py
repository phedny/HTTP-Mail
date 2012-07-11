from email.parser import Parser
from sys import stdin
from json import dumps
from hashlib import sha256

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

m = Parser().parse(stdin)
print m.get_unixfrom()
print dumps(handle_part(m), indent=4)

