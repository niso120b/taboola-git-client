import os
import stat
from jinja2 import Environment, FileSystemLoader
from Classes.GitClasses import GitRepo, GitCommit, GitDir

"""
    ------------------------------------
            Function copyHookFile
    ------------------------------------
    Description - put the git hook file for the post-commit in the repository with execute premissions
                    copy the file from the templates folder and render it with jinja2 template
    Input       - 
          work_path : the git working path
          hook_path : the path of the hooks folder
    Output      - None
"""
def copyHookFile(work_path, hook_path):
    j2_env = Environment(loader=FileSystemLoader('/opt/Templates'), trim_blocks=True)
    template = j2_env.get_template('post-commit.j2')
    rendered_template = template.render(script_path='/opt/taboola/client.py', git_path=work_path)
    new_file_path = hook_path+"/post-commit"

    ''' Delete hook file if exist '''
    try:
        os.remove(new_file_path)
    except OSError:
        pass

    ''' Write rendered template to hook file'''
    file = open(new_file_path, 'w+')
    file.write(rendered_template)
    file.close()

    ''' Add execute premissions to all users'''
    st = os.stat(new_file_path)
    os.chmod(new_file_path, st.st_mode | stat.S_IEXEC | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

"""
    ------------------------------------
            Function copyHookFile
    ------------------------------------
    Description - Scan for all the local git repositories and 
                    put the git hook file for the post-commit in the each reposiroty in hooks folder
    Input       - 
          path  : the path from where to start scaning
    Output      - None
"""
def installScript(path="/opt/"):
    repos = GitRepo.getRepos(path=path,recursive=True)
    for repo in repos:
        copyHookFile(work_path=repo.working_tree_dir, hook_path=repo.working_tree_dir+"/.git/hooks")
