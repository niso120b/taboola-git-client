from sys import argv
from git import GitCmdObjectDB
from Classes.InstallHooks import installScript
from Classes.GitClasses import GitRepo, GitCommit, GitDir
from Classes.SendPost import sendCommitData, setDataInDict

"""
    ------------------
            Main
    ------------------
    Description - Main
    Inputs with args -
            action - argv[1] - install or post 
                    install : for installing the git client hooks on the clients
                    post    : for sent the last commit trigger data to the flask server
            path   - argv[2] - the path 
                    in install case : the path from where to start scan git repositories
                    in post case    : the path of the git repo
"""
if __name__ == '__main__':
    print("Taboola Git Client")

    if len(argv) != 3:
        print("ERROR: you should pass two parameters action and path")
        print(" Install: python /opt/taboola/client.py install /opt/")
        print(" Post: python /opt/taboola/client.py post /opt/project/path/")
        exit(1)
    
    action = str(argv[1])
    path = str(argv[2])

    if action == "install":
        installScript(path=path)
    else:
        if action == "post":
            repo = GitRepo(path=path, odbt=GitCmdObjectDB)
            commit_id = str(repo.head.commit.hexsha)
            commit = GitCommit(repo=repo, commit_id=commit_id)
            data = setDataInDict(commit=commit)
            sendCommitData(data=data)
        else:
            print("ERROR: you pass a wrong action parameter its should be install or post")
            print(" Install: python /opt/taboola/client.py install /opt/")
            print(" Post: python /opt/taboola/client.py post /opt/project/path/")
            exit(1)
