#!/usr/bin/env python3

# Copyright 2015 Blake Dickie
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License

import sys
import os
import json
import getopt
import tempfile

def main(argv):
	DOCKER_ENV = os.environ.get('DOCKER_ENV_PROFILES')
	if DOCKER_ENV is None:
		print("DOCKER_ENV_PROFILES is not configured.", file=sys.stderr)
		return
	DOCKER_ENV = os.path.realpath(DOCKER_ENV)
	
	environment = os.environ.get('DOCKERENV_CURRENT_ENV')
	if environment is None:
		environment = 'develop'
	
	opts, args = getopt.gnu_getopt(argv, '', ["environment=", 'env='])
	for o, a in opts:
		if o in ("--environment", "--env"):
			environment = a
	
	env_dir = DOCKER_ENV + '/' + environment + '/'; 
	
	with open(env_dir + 'machines.json', 'r') as f:
		machine_data = json.load(f)
	
	print("export DOCKERENV_CURRENT_ENV=\"" + environment + '"')
	
	if len(args) == 0:
		currentenv = os.environ.get('DOCKERENV_CURRENT_MACHINE')
		sortedkeys = list(sorted(machine_data.keys()))
		for k in sortedkeys:
			if currentenv == k:
				print('*' + k, file=sys.stderr)
			else:
				print(k, file=sys.stderr)
	elif len(args) != 1:
		print("You must pass only one machine name.", file=sys.stderr)
	else:
		if args[0] in machine_data:
			data = machine_data[args[0]]
			socket = data.get('socket', 'false')
			hostname = data.get('host', '')
			port = data.get('port', '')
			
			if (socket == 'true'):
				print("export DOCKER_TLS_VERIFY=")
				print("export DOCKER_HOST=")
				print("export DOCKER_CERT_PATH=")
			else:
				tempdir = tempfile.mkdtemp(prefix='docker', suffix=environment)
				os.symlink(env_dir + 'ca.crt', tempdir + '/ca.pem')
				os.symlink(env_dir + 'personal.crt', tempdir + '/cert.pem')
				os.symlink(env_dir + 'personal.key', tempdir + '/key.pem')
				print("export DOCKER_TLS_VERIFY=\"1\"")
				print("export DOCKER_HOST=\"tcp://" + hostname + ":" + port + '"')
				print("export DOCKER_CERT_PATH=\"" + tempdir + '"')
			
			print("export DOCKERENV_CURRENT_MACHINE=\"" + args[0] + '"')
		else:
			print("Unknown machine name: " + args[0], file=sys.stderr)

if __name__ == '__main__':
    main(sys.argv[1:])
