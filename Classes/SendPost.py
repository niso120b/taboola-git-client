import json
import requests
from Classes.GitClasses import GitRepo, GitCommit, GitDir

"""
    ------------------------------------
            Function sendCommitData
    ------------------------------------
    Description - Send the data of the commit to the flask server in POST request
    Input       - 
          data  : dict object that contain the commit data 
    Output      - None
"""
def sendCommitData(data):
    data_json = json.dumps(data)
    print(data_json)
    post_result = requests.post(url="http://127.0.0.1:5000/post_commit/",json=data_json).json()
    if post_result['result'] == True:
        print("success")

"""
    ------------------------------------
            Function setDataInDict
    ------------------------------------
    Description - set dict with the data from the commit
    Input       - 
          commit  : the git commit
    Output      - A dict object
"""
def setDataInDict(commit):
    result = {}
    result["author"] = commit.commit.author.name
    result["email"] = commit.commit.author.email
    try:
        result["name"] = commit.repo["name"]
    except:
        result["name"] = commit.repo.working_dir.split("/")[-1]
    result["branch"] = commit.commit.repo.active_branch.name
    result["message"] = commit.commit.message
    result["files"] = []

    files = commit.getTree().getAll()
    for item in files:
        if type(item) is GitDir:
            result["files"].append({"type":"directory", "path": item.tree.path})
        else:
            result["files"].append({"type": "file", "path": item.blob.path})

    result["diff"] = []
    diffs = commit.getChanges()
    for diff in diffs:
        result["diff"].append({"file": diff.a_path , "content": str(diff.diff)})

    return result