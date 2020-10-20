# SHORTCUT FOR RUNNING DOCKER COMMANDS
# author: umurkaragoz
# version: 1.2

import os
from dotenv import load_dotenv
import argparse
from argparse import RawTextHelpFormatter
from slugify import slugify

# setup script arguments to accept
parser = argparse.ArgumentParser(description='`d`: Docker Helper Script', formatter_class=RawTextHelpFormatter)
parser.add_argument('method', type=str, choices=['u', 'd', 'r', 'c', 's', 'l', 'b'], help="""
u: up
d: down
r: restart
c: run command
s: ssh into the container
l: show container logs
b: re/build the image
""")
parser.add_argument('arguments', type=str, nargs='*', default='')

# parse arguments
args = parser.parse_args()

# get working directory, i.e. where you call the script from
cwd = os.getcwd()

# path to `.env` file for the project
# this assumed to be on the working directory, i.e. where you call the script from.
env_path = os.path.join(cwd, '.env')
# load `.env` variables to `os`
load_dotenv(dotenv_path=env_path)

# get relevant env values to constants
APP_URL: str = os.getenv("APP_URL")
APP_NAME: str = os.getenv("APP_NAME")
APP_SLUG: str = slugify(APP_NAME, separator="_")

print('DOCKER HELPER')
# execute one code block according to `method` argument
if args.method == 'u':
	print(f"UP: running {APP_NAME} project docker containers")
	print('-------------')
	os.system("docker-compose up -d")
	print('-------------')
	print(f"development server is now live on {APP_URL}")

elif args.method == 'd':
	print("DOWN: shutting project's docker containers down")
	print('-------------')
	os.system("docker-compose down -v")
	print('-------------')

elif args.method == 'r':
	print("RESTART: restarting project's docker containers")
	print('-------------')
	os.system("docker-compose down -v && docker-compose up -d")
	print('-------------')
	print(f"development server is now live on {APP_URL}")

elif args.method == 'c':
	print("COMMAND: running COMMAND on web container")
	command: str = ' '.join(args.arguments)
	print(f'COMMAND: running COMMAND "{command}" on web container')
	print('-------------')
	os.system(f"docker-compose exec web {command}")
	print('-------------')

elif args.method == 's':
	print("SH: SSH into the web container")
	print('-------------')
	os.system(f"docker exec -ti {APP_SLUG} sh")
	print('-------------')

elif args.method == 'b':
	print("BUILD: BUILDING containers")
	print('-------------')
	os.system("docker-compose build")
	print('-------------')

elif args.method == 'l':
	print("LOGS: show web container LOGS")
	print('-------------')
	command: str = ' '.join(args.arguments)
	
	# clear preceding quotes
	if command[0] == '"' or command[0] == "'":
		command = command[1:]
	# clear tailing quotes
	if command[-1] == '"' or command[-1] == "'":
		command = command[:-1]
		
	os.system(f"docker-compose logs {command} web")
	print('-------------')

# let the user know that the script execution has finished
print('done')
