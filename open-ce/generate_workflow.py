from build_tree import BuildTree
from jinja2 import Template,Environment, FileSystemLoader
import sys

def main():

    dependency_map = {}
    env_file_list = []
    python_variants = {'3.6', '3.7'}
    build_types = {'cuda', 'cpu'}

    # process cmd line arguments
    if len(sys.argv) < 4:
        print("Missing required number of parameters\n"
             "Format:- <pkg env file>, <python_version>, <build_type>\n"
             "Example:- 'envs/spacy-env.yaml', '3.6', 'cuda' ")
        sys.exit(1)

    # For env files
    if str(sys.argv[1]).__contains__(','):
        env_file_list.append(str(sys.argv[1]).split(','))
    else:
        env_file_list.append(str(sys.argv[1]))

    # For py variants
    if python_variants.__contains__(str(sys.argv[2])):
        py_verion = sys.argv[2]

    # For build variants
    if build_types.__contains__(str(sys.argv[3])):
        build_type = sys.argv[3]


    # Create the BuilTree object
    buildTree = BuildTree(env_file_list , py_verion, build_type)
    if not buildTree:
          sys.exit(1)

    # Itrerate over the object to prepare a 
    # dictionary of recipe as key and recipe dependency list as its value
    for buildCmd in buildTree:
        dependency_list = []
        if len(buildCmd.build_command_dependencies):
            for dependency in buildCmd.build_command_dependencies:
              dependency_list.append(str(buildTree[dependency].name()))
        else:
            dependency_map.update({buildCmd.recipe: []})
        dependency_map.update({buildCmd.recipe: dependency_list})


    # Load the workflow-template 
    file_loader = FileSystemLoader('open-ce/templates')
    env = Environment(loader=file_loader)
    template = env.get_template('workflow-template.yaml')
    print(template.render(buildTree=buildTree,dependency_map=dependency_map))

    # Write the generated workflow to a file
    filename = 'workflows/workflow.yaml'
    with open(filename, 'w') as fh:
        fh.write(template.render(buildTree=buildTree,dependency_map=dependency_map))

if __name__ == "__main__":
      main()

