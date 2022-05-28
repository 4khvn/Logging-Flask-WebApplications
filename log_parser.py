import argparse
import re
import os

def launch_access_logger(logfifo_name):
	if os.fork() > 0:
		return
	os.system(f'tail -n0 -F logs/access.log > { logfifo_name }')
	exit()

def launch_error_logger(errfifo_name):
	if os.fork() > 0:
		return
	os.system(f'tail -n0 -F logs/error.log > { errfifo_name }')
	exit()

def find_value(regex, entry, idx = 0):
	value = re.search(regex, entry)
	if value:
		return value.group(idx).strip()
	return '-'

def parse_log(entry, errfifo_name):
	ip_addr = find_value(r'(\d{1,3}\.){3}\d{1,3}', entry)
	ts = find_value(r'\d+\/\S+\/\d+(\:\d{1,2}){3}', entry)
	req_type = find_value(r'(GET|POST)', entry)
	req = find_value(r'(GET|POST) (\/[\d|\S]*)+', entry)
	link = find_value(r'(http|https)\:\/\/(localhost|(([\d|\S]+\.)+[\d|\S]+))(\/[\d|\S]+)*\/{0,1}', entry)
	s_code = find_value(r' [0-9]{3} ', entry)

	data = '-'
	#if req == "POST /site/form":
	#	err_fifo = open(errfifo_name)
	#	print(err_fifo.readable())
	#	err = err_fifo.readlines()
	#	print(err[0])
	#	data = find_value(r"Latom=.*", err)

	# printing to console for now
	# replace this part with inserting it into the db
	print('ip: ' + ip_addr + ' ts: ' + ts + ' r: ' + req + ' s_code: ' + s_code + ' link: ' + link + ' data: ' + data, end=' ')

	#if req_type.group(0).strip() == 'POST' and link:
	#	line = open(err_fifo).readline()
	#	latom = re.search(r'Latom=.*', line)
	#	print(latom)

	print('')

if __name__ == "__main__":
	parser =  argparse.ArgumentParser()
	parser.add_argument('logfifo_name')
	parser.add_argument('errfifo_name')
	args = parser.parse_args()
	logfifo_name = args.logfifo_name
	errfifo_name = args.errfifo_name

	launch_access_logger(logfifo_name)
	launch_error_logger(errfifo_name)

	log_fifo = open(logfifo_name)
	while True:
		entry = log_fifo.readline()
		if entry:
			#print(entry)
			parse_log(entry, 'err_fifo')
