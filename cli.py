from pathlib import Path
from argparse import ArgumentParser
from api import project_server
import uvicorn

cli = ArgumentParser()
cli.add_argument('root', help="The path for the root of a looker project")

args = cli.parse_args()

root = Path(args.root).resolve()

app = project_server(root)

uvicorn.run(app, host="localhost", port=8000)
