# SHORTCUT FOR RUNNING DOCKER COMMANDS
# author: umurkaragoz
# version: 1.3

import os
from dotenv import load_dotenv
import argparse
from argparse import RawTextHelpFormatter
from slugify import slugify


# create a help text formatter to reduce help text indentation
# otherwise it gets indented too much
# https://stackoverflow.com/a/46554318
# https://stackoverflow.com/a/25010243
def less_indent_formatter(prog): return argparse.RawTextHelpFormatter(prog, max_help_position=2)


# setup script arguments to accept
parser = argparse.ArgumentParser(description='`d`: Docker Helper Script', formatter_class=less_indent_formatter)
parser.add_argument('method', type=str, choices=['u', 'd', 'r', 'c', 's', 'l', 'b', 'a'], help="""
b : BUILD     (re)builds project images
u : UP        starts the project containers in detached mode
d : DOWN      stops the project containers and clears volumes
r : RESTART   runs UP and DOWN routines mentioned above
c : COMMAND   runs specified command in `web` container
a : ARTISAN   runs Laravel's artisan command in `web` container
s : SSH       starts SSH session on `web` container
l : LOGS      shows `web` container logs

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

if args.method == 'b':
	print("BUILD: BUILDING containers")
	print('-------------')
	os.system("docker-compose build")
	print('-------------')

elif args.method == 'u':
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

elif args.method == 's':
	print("SH: SSH into the web container")
	print('-------------')
	os.system(f"docker exec -ti {APP_SLUG} sh")
	print('-------------')

elif args.method == 'c':
	print("COMMAND: running COMMAND on web container")
	command: str = ' '.join(args.arguments)
	print(f'COMMAND: running COMMAND "{command}" on web container')
	print('-------------')
	os.system(f"docker-compose exec web {command}")
	print('-------------')

elif args.method == 'a':
	print("ARTISAN: running ARTISAN COMMAND on web container")
	command: str = ' '.join(args.arguments)
	print(f'ARTISAN: running COMMAND "php artisan {command}" on web container')
	print('-------------')
	os.system(f"docker-compose exec web php artisan {command}")
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
