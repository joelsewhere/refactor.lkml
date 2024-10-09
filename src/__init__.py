OTHER_EXPLORES = [
    'secureset_salesforce', 
    'student_services_cases', 
    'online_roster_cross_reference', 
    'milestone_canvas_submissions', 
    'milestone_student_progress', 
    'canvas_curriculum_tracking', 
    'yale_tech_sub', 'student_roster', 
    'registrar_pipeline_prototype', 
    'registrar_out_of_bound_payments', 
    'compliance_online_roster', 
    'compliance_in_person_roster', 
    'marketing_email', 
    'learn_co_users', 
    'leaves_of_absence', 
    'registrar_enrollments', 
    'scheduled_invoices', 
    'salesforce_rosters', 
    'registrar_roster', 
    'nps_formstack_duplicates', 
    'post_grad_canvas_deactivation', 
    'student_curriculum_long', 
    'zoom_imports', 
    'canvas_course_grades', 
    'marketo_return_to_campus', 
    'marketo_leads',
    ]

import lkml, re, os, shutil, json
from glob import glob
from itertools import chain
from requests import get
from typing import Tuple, List
from pathlib import Path


IGNORE = [
    '__pycache__',
    '__init__',
    '.git',
]


def get_files(path):
    paths = []
    for p in path.rglob("*"):
        found_ignore = False
        for ignore in IGNORE:
            if ignore in p.as_posix():
                found_ignore = True
        if not found_ignore:
            root_idx = p.parts.index(path.stem)
            project_p = Path(*p.parts[root_idx:])
            paths.append((p, project_p))
    return paths


def project_json(files):
    output = []
    tree = {"text": files[0][1].parts[0], "state": {
        "opened": True,
    },
    "children": output
    }
    helper = {}
    for abspath, rel in files:
        current = tree
        subpath = ""
        for idx, segment in enumerate(rel.parts[1:]):
            if "children" not in current:
                current["children"] = []
            subpath += "/" + segment
            if subpath not in helper:
                relpath = Path(segment)
                if not relpath.suffixes:
                    filetype = 'default'
                else:
                    filetype = relpath.suffixes[0].replace('.', '')
                    
                helper[subpath] = { "text": segment, "type": filetype, "abspath": Path(*rel.parts[:idx]).as_posix()}
                current["children"].append(helper[subpath])
            current = helper[subpath]
    
    return tree


                
            



    
# def get_filepaths() -> Tuple[dict, dict]:
#     # Collect the paths for local .explore and .view files
#     explore_files = glob('./*/*.explore.lkml') + glob('./*/*.explore')
#     # Collect the explore filenames and map them to the file path
#     pattern = r'/([a-zA-Z]+(?:_[a-zA-Z]+)*)\.explore'
#     explores_path_map = dict(zip([(re.findall(pattern, file)[0]) for file in explore_files], 
#                             explore_files))

#     unorganized = ['google_analytics', 'huntr', 'slack']
#     unorganized_views = [glob(f'./{directory}/*.view.lkml') for directory in unorganized]
#     # All view paths
#     view_files = (glob('./*/*.view.lkml') 
#                 + glob('./views/*/*.view.lkml')
#                 + glob('./*/*.view.lkml')
#                 + glob('./*.view.lkml')
#                 + list(chain.from_iterable(unorganized_views))) # Unpack list
#     # Collect the view filenames and map them to the file path
#     pattern = r'/([a-zA-Z0-9]+(?:_[a-zA-Z0-9]+)*)\.view'
#     views_path_map = {}
#     for file in view_files:
#         match = re.findall(pattern, file)
#         if match:
#             views_path_map[match[0]] = file

#     return explores_path_map, views_path_map

# def generate_explore_files(explores:List[dict], 
#                          views_path_map:dict, 
#                          OTHER_EXPLORES:list) -> None:

#     other_lkml = {
#             "includes": [],
#             "explores": [],
#             }
#     group_paths = set()
#     # Loop over each explore dictionary
#     for explore in explores:
#         # Collect the path for the explore
#         if explore.get('name') in OTHER_EXPLORES:
#             group_path, explore_path = './other', './other/other.model.lkml'
#         else: group_path, explore_path = get_explore_filepath(explore)
#         group_paths.add(group_path)
#         # documentation: https:/lkml.readthedocs.io/en/latest/simple.html#simple-lookml-generation
#         lookml = {
#             "includes": [],
#             "explores": [],
#             }
        
#         # Add the explore data to the lookml
#         if explore.get('name') in OTHER_EXPLORES:
#             other_lkml['explores'].append(explore)
#         else: lookml['explores'].append(explore)

#         # Collect the joins from the explore
#         # in order to generate the import paths for each
#         # view file in the explore
#         joins = explore.get('joins', [{}]) 
#         # Find the base view for the explore
#         view_name = explore.get('view_name')
#         from_ = explore.get('from')
#         if view_name:
#             base_view = view_name
#         elif from_:
#             base_view = from_
#         else:
#             base_view = explore.get('name')

#         # Loop over all of the view dependencies
#         # Generate the relative path from the explore to the view file
#         # Add the relative path to the `includes` lookml key
#         for dependency in [{'name': base_view}] + joins:
#             name = dependency.get('name')
#             view_path = views_path_map.get(name)
#             if explore_path and view_path:
#                 abspath = os.path.abspath
#                 dirname = os.path.dirname
#                 include_path = os.path.relpath(abspath(view_path), dirname(abspath(explore_path)))
#                 if explore.get('name') in OTHER_EXPLORES:
#                     other_lkml['includes'].append(include_path)
#                 else:
#                     lookml['includes'].append(include_path)

#         if not explore.get('name') in OTHER_EXPLORES:
#             # Write the production explore to the .explore file
#             with open(explore_path, 'w+') as file:
#                 lkml.dump(lookml, file)
#     if not os.path.isdir('./other'):
#         os.mkdir('other')
#     with open('./other/other.model.lkml', 'w+') as file:
#         file.write(lkml.dump(other_lkml))
    
#     return list(group_paths)

# def get_explore_filepath(explore):

#     group_label = explore.get('group_label', 'Flatiron')
#     group_label = (group_label.lower()
#                                 .replace('.', '')
#                                 .replace(' ', '_')
#                                 .replace('(', '')
#                                 .replace(')', '')
#                     )
#     explore_name = explore.get('name')
#     group_path = os.path.join('.', group_label)
#     explore_path = os.path.join(group_path, explore_name + '.explore.lkml')
#     if not os.path.isdir(group_path):
#         os.mkdir(group_path)
#     return group_path, explore_path
 
# def generate_explores(other_explores):
#     print('Generating explores...')
#     model = get_flatiron_model()
#     explores = model.get('explores')
#     explores_path_map, views_path_map = get_filepaths()
#     return generate_explore_files(explores,
#                                   views_path_map,
#                                   other_explores)

# def organize_views():
#     print('Organizing views...')
#     if not os.path.isdir('./views'):
#         os.mkdir('views')
#     views = get_filepaths()[1]
#     for view_name, old_path in views.items():
#         with open(old_path, 'r') as file:
#             view = lkml.load(file.read())['views'][0]
#         table_name = view.get('sql_table_name')
#         if table_name:
#             schema = table_name.split('.')[0]
#         elif view.get('derived_table'):
#             schema = 'derived'
#         schema_path = os.path.join('views', schema)
#         new_view_path = os.path.join(schema_path, view_name + '.view.lkml')
#         if not os.path.exists(schema_path):
#             os.mkdir(schema_path)
#         shutil.move(old_path, new_view_path)
#         with open(new_view_path, 'r+') as file:
#             file_text = file.read()
#             if 'datagroup_trigger' in file_text or 'morning_pdts' in file_text:
#                 file_text = 'include: "../../config.model.lkml"\n\n' + file_text
#                 file.seek(0)
#                 file.truncate()
#                 file.write(file_text)


# def delete_old_directories(group_paths):
#     print('Deleting old directories...')
#     group_paths_ = [x.replace('./', '') for x in group_paths] + ['views']
#     for path in os.listdir():
#         if os.path.isdir(path) and path not in group_paths_ and 'git' not in path:
#             shutil.rmtree(path)

# def generate_explore_models(group_paths):
#     print('Generating explore models...')
#     lookml = {
#         "includes": ["../config.model.lkml", "*/*.explore.lkml"],
#     }
#     for path in group_paths:
#         explores = glob(os.path.join(path, '*.explore.lkml'))
#         model = os.path.join(path, path[2:] + '.model.lkml')
#         with open(model, 'w+') as file:
#             file.write(lkml.dump(lookml))

# # def include_config():
# #     explores = glob('**/*.explore.lkml')
# #     views = glob('views/*/*.view.lkml')
# #     files = explores + views
# #     for file in files:
# #         with open(file, 'w+') as f:
# #             text = f.read()
# #             if 


# def update_flatiron_model():
#     old_model = get_flatiron_model()
#     lookml = {
#         "includes": ["./config.model.lkml", "*/*.explore.lkml", "./other/other.model.lkml"],
#         "map_layers": old_model["map_layers"],
#     }
#     with open('flatiron.model.lkml', 'w+') as file:
#         file.write(lkml.dump(lookml))

# def main():
#     organize_views()
#     group_paths = generate_explores(OTHER_EXPLORES)
#     group_paths_ = [x.replace('./', '') for x in group_paths]
#     delete_old_directories(group_paths)
    
#     #### Eventually, the goal is probably to move to models for
#     #### each explore group.
#     #### This change will require writing code to update each
#     #### lookml reference to the flatiron model via the 
#     #### looker api. 
#     # generate_explore_models(group_paths)
#     # print('Deleting flatiron.model.lkml')
#     # os.remove('./flatiron.model.lkml')
    
#     #### For now, we will import every explore
#     #### into the flatiron model
#     print('Updating flatiron.model.lkml...')
#     update_flatiron_model()
