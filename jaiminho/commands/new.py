from jaiminho.commands.commons import request_file
import os
import shutil
import subprocess


def run(args):
    request_path = request_file(args, args.name)

    request_dir = os.path.dirname(request_path)

    os.makedirs(request_dir, exist_ok=True)

    if os.path.exists(request_path):
        print(f'Existing request: {args.name}')
        return 1

    if args.model:
        model_path = request_file(args, args.model)

        shutil.copy(model_path, request_path)
    else:
        open(request_path, 'w').close()

    if not args.no_edit:
        command = [ os.environ.get('EDITOR', 'vi'), request_path ]

        subprocess.run(command)

