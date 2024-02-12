from jaiminho.commands.commons import request_file
import os
import subprocess


def run(args):
    request_path = request_file(args.home_folder, args.request_name)

    if not os.path.exists(request_path):
        print(f'Request not found: {args.request_name}')
        return 1

    command = [ os.environ.get('EDITOR', 'vi'), request_path ]

    subprocess.run(command)
