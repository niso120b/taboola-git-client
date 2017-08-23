# Taboola Git Client

Taboola DevOps developer, programing task.

Solution By Nissim Bitan, Mamram almuni with 5 years experience in multi Cloud Developing and DevOps and FullStack Developing
**this solution contains 2 actions:**

## Installation
Scan recursive a given path and search for local git repositories and on each repository
the installation script inject the hook script to the git repository hooks folder.

**Usage:**

``pyhton CLIENT_SCRIPT install PATH``

**Example:**

``pyhton /opt/taboola/client install /opt/``

and its scan the /opt/ folder recursive and run the installation

## Post

when users at systems that the client are allready install and the hook script inside the git repository make a commit
so the client send the data about the commit in **POST** request and the server print it.

**Usage:**

``pyhton CLIENT_SCRIPT post PATH``

**Example:**

``pyhton /opt/taboola/client post /opt/git_repo_dir``

### Server Output Example

```
* Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
----------------Commit Details------------------
Author: niso120b
Email: niso120b@gmail.com
Repository Name: taboola-java-jenkins
Branch: master
Commit Message: Update README.md file

Files:
directory : bin
file : bin/calc
directory : src
directory : src/main
directory : src/main/antlr
file : src/main/antlr/Expr.g4
directory : src/main/java
file : src/main/java/Calc.java
file : src/main/java/CalcEvalVisitor.java
directory : src/test
directory : src/test/java
file : src/test/java/CalcTest.java
file : README.md
file : jenkinsfile
file : pom.xml
Diffs:
File: README.md
Diff:
b'@@ -7,7 +7,7 @@ and create all the ci process in jenkins.

### Additional changes and extra files

-**the solution contain:**
+**the solution contains:**
* Jenkinsfile - which run all the process in the jenkins (in Groovy)
* pom.xml - add rpm-maven-plugin and create the process to create the rpm
* bin folder - the bin folder contain the calc file, its the **calc** command at the final result
'
------------------------------------------------
127.0.0.1 - - [23/Aug/2017 01:16:37] "POST /post_commit/ HTTP/1.1" 200 -
```

## Contact

Nissim Bitan - niso120b@gmail.com
