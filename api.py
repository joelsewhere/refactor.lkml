from fastapi import FastAPI
from starlette.responses import FileResponse 
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

def project_server(project_json):
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
    
    return app