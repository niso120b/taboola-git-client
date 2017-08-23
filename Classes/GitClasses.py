import re
import os
from os import listdir, makedirs
from os.path import isdir, sep
from git import Repo, Blob, Diff
from git.exc import InvalidGitRepositoryError

"""
    ----------------------------------------
                Class GitRepo
               ---------------
    ----------------------------------------
    
    Represent a Git Repository
"""
class GitRepo(Repo):
    def __init__(self, *args, **kwargs):
        super(GitRepo, self).__init__(*args, **kwargs)

    """
        ------------------------------------
                Function getCommit
        ------------------------------------
        Description - Retrieve a GitCommit object represent single commit from reporistory
        Input       - 
              commitId : commit id 
        Output      - GitCommit object
    """
    def getCommit(self, commitId):
        return GitCommit(repo=self, commit_id=commitId)

    """
        ------------------------------------
                Function getTree
        ------------------------------------
        Description - Retrieve a GitTree object represent the tree in repo
        Input       - None
        Output      - GitTree object
    """
    def getTree(self):
        return GitTree(self, self.tree())

    """
        ------------------------------------
                Function getTreeFile
        ------------------------------------
        Description - Retrieve the content of file in path
        Input       - 
              path   : path of file
        Output      - content of file
    """
    def getTreeFile(self, path):
        return self.getTree().getFile(path)

    """
        ------------------------------------
                Function getRepos
        ------------------------------------
        Description - Retrieve a list of git repositories from a partent path
        Input       - 
              path      : parent path of git repositories
              recursive : scan the parent path recursively
        Output      - A list of GitRepo
    """
    @staticmethod
    def getRepos(path, recursive=False, excludePath=[]):
        contents = listdir(path)
        repos = []
        for content in contents:
            fullPath = path + sep + content
            fullPath = fullPath.replace('//', '/')
            if isdir(fullPath):
                try:
                    toAdd = True
                    for excl in excludePath:
                        if re.match(excl, content):
                            toAdd = False
                    if toAdd:
                        repos.append(GitRepo(fullPath))
                except InvalidGitRepositoryError:
                    if recursive:
                        repos.extend(GitRepo.getRepos(fullPath, True))
        return repos


"""
    ----------------------------------------
                Class GitCommit
               -----------------
    ----------------------------------------

    Represent a Single Commit
"""
class GitCommit():
    def __init__(self, commit=None, repo=None, commit_id=None):
        if commit == None:
            self.repo = repo
            self.commit = repo.commit(commit_id)
        else:
            self.commit = commit

    """
        ------------------------------------
                Function getChanges
        ------------------------------------
        Description - Retrieve a list of the diff changes in the commit
        Input       - None
        Output      - A list of Diff
    """
    def getChanges(self):
        parents = self.commit.parents
        if len(parents) > 0:
            for p in parents:
                pc = self.commit.repo.commit(p)
                return pc.diff(self.commit, create_patch=True)
        else:
            files = self.getTree().getAllFiles()
            diffs = []
            for fl in files:
                diffs.append(
                    Diff(self.commit.repo, None, fl.blob.path, None, fl.blob.hexsha, None, str(fl.blob.mode), True,
                         False, None, None, ''))
            return diffs

    """
        ------------------------------------
                Function getTree
        ------------------------------------
        Description - Retrieve a GitTree object represent the tree in thr commit
        Input       - None
        Output      - A list of Diff
    """
    def getTree(self):
        return GitTree(self.commit.repo, self.commit.tree)

"""
    ----------------------------------------
                Class GitTree
               -----------------
    ----------------------------------------

    Represent a Tree in repository
"""
class GitTree():
    def __init__(self, repo, tree):
        self.repo = repo
        self.tree = tree

    """
        ------------------------------------
                Function getFile
        ------------------------------------
        Description - Retrieve a GitFile object represent the file in the git repo
        Input       - 
            path    : the path of the file
        Output      - A GitFile object
     """
    def getFile(self, path):
        try:
            blob = self.tree[path]
            return GitFile(blob)
        except KeyError:
            raise GitPathNotFound('Path:' + path + ' not found')

    """
        ------------------------------------
                Function getRoot
        ------------------------------------
        Description - Retrieve a list with GitFile and GitDir object
                        represent the git root folder
        Input       - None
        Output      - list of GitFile and GitDir object
    """
    def getRoot(self):
        root = []
        for subTree in self.tree.trees:
            root.append(GitDir(subTree))
        for blob in self.tree.blobs:
            root.append(GitFile(blob))
        return root

    """
        ------------------------------------
                Function __getTreeFiles
        ------------------------------------
        Description - Retrieve a list with GitFile objects represent all files from path
        Input       - 
            tree    : the tree
            path    : path from where to start
        Output      - list of GitFile objects
    """
    def __getTreeFiles(self, tree, path=""):
        files = []
        for subTree in tree.trees:
            files.extend(self.__getTreeFiles(subTree, path))
        for blob in tree.blobs:
            files.append(GitFile(blob))
        return files

    """
        ------------------------------------
                Function getAllFiles
        ------------------------------------
        Description - Retrieve a list with GitFile objects represent all files in tree
        Input       - None
        Output      - list of GitFile objects
    """
    def getAllFiles(self):
        return self.__getTreeFiles(self.tree)

    """
        --------------------------------------------
                Function __getAllFilesAndFolders
        --------------------------------------------
        Description - Retrieve a list with GitFile and GitDir objects represent all files and directories from path
        Input       - 
            tree    : the tree
            path    : path from where to start
        Output      - list of GitFile and GitDir objects
    """
    def __getAllFilesAndFolders(self, tree, path=""):
        all = []
        for subTree in tree.trees:
            all.append(GitDir(subTree))
            all.extend(self.__getAllFilesAndFolders(subTree, path))
        for blob in tree.blobs:
            all.append(GitFile(blob))
        return all

    """
        ------------------------------------
                Function getAll
        ------------------------------------
        Description - Retrieve a list with GitFile and GitDir objects represent all files and directories in tree
        Input       - None
        Output      - list of GitFile and GitDir objects
    """
    def getAll(self):
        return self.__getAllFilesAndFolders(self.tree)

"""
    ----------------------------------------
                Class GitDir
               --------------
    ----------------------------------------

    Represent a directory in repository tree
"""
class GitDir(object):
    def __init__(self, tree, parent=None):
        self.tree = tree
        self.parent = parent

    """
        ------------------------------------
                Function getFiles
        ------------------------------------
        Description - Retrieve a list with GitFile objects represent all files in the directory
        Input       - None
        Output      - list of GitFile objects
    """
    def getFiles(self):
        files = []
        for blob in self.tree.blobs:
            files.append(GitFile(blob))
        return files

    """
        ------------------------------------
                Function getSubDirs
        ------------------------------------
        Description - Retrieve a list with GitDir objects represent all sub directories in the directory
        Input       - None
        Output      - list of GitDir objects
    """
    def getSubDirs(self):
        dirs = []
        for subTree in self.tree.trees:
            dirs.append(GitDir(subTree))
        return dirs

"""
    ----------------------------------------
                Class GitFile
               ---------------
    ----------------------------------------

    Represent a file in repository tree
"""
class GitFile(object):
    def __init__(self, blob):
        self.blob = blob

    """
        ------------------------------------
                Function getContent
        ------------------------------------
        Description - Retrieve the content of the file
        Input       - None
        Output      - file content string
    """
    def getContent(self):
        return self.blob.data_stream.read()

"""
    ----------------------------------------
                Class GitPathNotFound
               -----------------------
    ----------------------------------------

    Represent an Exception in case the git path is not found
"""
class GitPathNotFound(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)