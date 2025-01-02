from fastapi import FastAPI
from starlette.responses import FileResponse 
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from typing import Dict, Any
from fastapi import Request
from pathlib import Path

def project_server(project_json, flattened):
    app = FastAPI()


    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.mount('/static', StaticFiles(directory='static', html=True), name='static')

    @app.get("/")
    async def main():
        return FileResponse('index.html')

    @app.get("/data")
    async def data():
        return [project_json]
    
    @app.post("/move")
    async def move(request: Request):
        data = await request.json()
        
        id = data['id']
        new_parent = data['new_parent']
        node_name = Path(id).parts[-1]
        new_path = Path(new_parent) / node_name
        flattened[id] = new_path.as_posix()

        print(flattened)

    @app.post('/rename')
    async def rename(request: Request):
        data = await request.json()

        id = data['id']
        new = data['new']
        old = data['old']
        if id in flattened:
            val = flattened[id]
            flattened[id] = val.replace(old, new)
        
        print(flattened)
        # if id is not found return indicator to javascript 
        # so the id can be set for the new node

    
    return app



    # [
    #     {
    #         'text' : 'Project Root',
    #         'state' : {
    #         'opened' : True,
    #         },
    #         'children' : [
    #         { 'text' : 'README.md', 'type': 'md'},
    #         { 'text' : 'config.lkml', 'type': 'lkml'},
    #         { 'text' : 'meta.txt', 'type': 'other'},
    #         {'text': 'Model Name', "type": "default", "children": [
    #             { 'text' : 'file.explore.lkml', 'type': 'explore'},
    #             { 'text' : 'file.view.lkml', 'type': 'view'},
    #             { 'text' : 'file.model.lkml', 'type': 'model'},
    #         ], "state": {"opened": True}},
    #         {'text': 'dashboards', "type": "default", "children": [
    #             {'text': 'file.dashboard.lookml', "type": "dashboard"}
    #         ]}
    #         ]
    #     }
    #     ]