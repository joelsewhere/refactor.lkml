from pathlib import Path
from argparse import ArgumentParser
from api import project_server
import uvicorn
from src import get_files, project_json

cli = ArgumentParser()
cli.add_argument('root', help="The path for the root of a looker project")

args = cli.parse_args()

root = Path(args.root).resolve()

files = get_files(root)
print(files)
json = project_json(files)
print(json)

app = project_server(json)


uvicorn.run(app, host="localhost", port=8000)
