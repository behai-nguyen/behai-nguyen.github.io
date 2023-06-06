---
layout: post
title: "CI/CD #03. Jenkins: using Pipeline and proper Bash script to run Pytest."
description: We write a proper and generic Bash script file to ⓵ create a virtual environment, ⓶ run editable install, and ⓷ run Pytest for all tests. Then we write a generic Jenkins Pipeline which will ⓵ clone a Python project GitHub repository, ⓶ call the Bash script file to do all the works.

gallery-image-list:
    - "https://behainguyen.files.wordpress.com/2023/02/057-04.png"
    - "https://behainguyen.files.wordpress.com/2023/02/057-05.png"

tags:
- Jenkins
- Bash
- Pipeline
- Pytest
---

*We write a proper and generic Bash script file to ⓵ create a virtual environment, ⓶ run editable install, and ⓷ run Pytest for all tests. Then we write a generic Jenkins Pipeline which will ⓵ clone a Python project GitHub repository, ⓶ call the Bash script file to do all the works.*

| ![057-feature-image.png](https://behainguyen.files.wordpress.com/2023/02/057-feature-image.png) |
|:--:|
| *CI/CD #03. Jenkins: using Pipeline and proper Bash script to run Pytest.* |

To recap, I am running 
<a href="https://www.jenkins.io/" title="Jenkins" target="_blank">Jenkins</a>
2.388 LTS on my Ubuntu 22.10, the name of this machine is <code>HP-Pavilion-15</code>.
I am accessing Jenkins and <code>HP-Pavilion-15</code> from my Windows 10 machine 
using FireFox and <code>ssh</code>, respectively. And 
<a href="https://www.jenkins.io/doc/book/pipeline/" title="Pipeline" target="_blank">Pipeline</a>
is the Jenkins documentation page which I have been working through.

I'm discussing converting the <em>“Free style shell script”</em> 
in <a href="https://behainguyen.wordpress.com/2023/01/28/ci-cd-01-jenkins-manually-clone-a-python-github-repo-and-run-pytest/"
title="CI/CD #01. Jenkins: manually clone a Python GitHub repo and run Pytest." target="_blank">CI/CD #01. Jenkins: manually clone a Python GitHub repo and run Pytest</a> 
to a proper Bash script (file), and calling this Bash script 
file in a Jenkins Pipeline using the <code>sh</code> step.

Jenkins is running under user <code>jenkins</code>, and the group is 
also named <code>jenkins</code>. This is apparent if we list contents of
Jenkins' work directory, which is <code>/var/lib/jenkins/workspace/</code>.

To make managing permissions easier, I will create the Bash script 
file under user <code>jenkins</code>. To do that, we need 
to be able to log in, and <code>ssh</code> to <code>HP-Pavilion-15</code>
under user <code>jenkins</code>. We need to set its password:

```
$ sudo passwd jenkins
```

Once the password is set, we can use it to log in, via:

```
C:\>ssh jenkins@hp-pavilion-15
```

The original <em>“Free style shell script”</em> code we are converting 
to proper Bash script code is:

```shell
PYENV_HOME=$WORKSPACE/venv

# Delete previously built virtualenv
if [ -d $PYENV_HOME ]; then
    rm -rf $PYENV_HOME
fi

# Create virtualenv and install necessary packages
virtualenv $PYENV_HOME
. $PYENV_HOME/bin/activate
$PYENV_HOME/bin/pip install -e .
$PYENV_HOME/bin/pytest
```

<code>ssh</code> into the Ubuntu machine with:

```
C:\>ssh jenkins@hp-pavilion-15
```

The home directory of user <code>jenkins</code> is <code>/var/lib/jenkins</code>.
Create the new sub-directory <code>scripts/</code> under home directory, and
create the <code>pytest.sh</code> Bash script file under this 
<code>/var/lib/jenkins/scripts</code>.

```
Content of /var/lib/jenkins/scripts/pytest.sh:
```

{% highlight console linenos %}
#!/bin/bash

#
# 04/01/2023.
#
# A generic script which create a clean virtual environment and run pytest.
#
# Intended to be used in a Jenkins GitHub project Pipeline as:
#
#    sh("${JENKINS_HOME}/scripts/pytest.sh ${WORKSPACE}")
#
# The repo is cloned automatically by Jenkins. This script does the followings:
#
#   1. If virtual directory ${WORKSPACE}/venv exists, remove all of it.
#
#   2. Create virtual environment ${WORKSPACE}/venv, then activate it.
#
#   3. Run editable install for the project.
#
#   4. Finally run pytest.
#

if [ -z $1 ]; then
    echo "Usage: ${0##*/} <dir>"
    exit 1
fi

if [ ! -d $1 ]; then
    echo "$1 does not exist."
    exit 1
fi

virtual_dir=$1/venv

echo "Virtual directory $virtual_dir."

if [ -d $virtual_dir ]; then
    rm -rf $virtual_dir
    echo "$virtual_dir removed."
fi

virtualenv $virtual_dir

cd $1

. $virtual_dir/bin/activate
$virtual_dir/bin/pip install -e .
$virtual_dir/bin/pytest
{% endhighlight %}

Param <code>$1</code> to <code>pytest.sh</code> is basically the
project directory: Jenkins environment variable <code>${WORKSPACE}</code>.
Let's walk through the code:

<ul>
<li style="margin-top:10px;">Lines 23-26 -- there must be a 
directory parameter supplied, otherwise exit with error code 1.</li>

<li style="margin-top:10px;">Lines 28-31 -- the directory
passed in must exist, otherwise exit with error code 1.</li>

<li style="margin-top:10px;">Line 33 -- assemble the virtual 
directory absolute path under the passed in project directory. The 
name of the actual virtual directory is <code>venv</code>.
</li>

<li style="margin-top:10px;">Line 35 -- print out the absolute 
virtual directory path.</li>

<li style="margin-top:10px;">Lines 37-40 -- if the virtual 
directory exists already, remove it.</li>

<li style="margin-top:10px;">Line 42 -- create the virtual environment
using the absolute virtual directory.</li>

<li style="margin-top:10px;">Line 44 -- move to the passed in directory.
This directory is the parent of the actual virtual directory <code>venv</code>.
</li>

<li style="margin-top:10px;">Line 46 -- activate the virtual environment.</li>

<li style="margin-top:10px;">Line 47 -- run editable install.</li>

<li style="margin-top:10px;">Line 48 -- run Pytest.</li>
</ul>

We have to set the <strong>Execute</strong> permission for the owner:

```
$ chmod u+x pytest.sh
```

![057-01.png](https://behainguyen.files.wordpress.com/2023/02/057-01.png)

This script is generic enough to do Pytest for any Python project via 
a Jenkins Pipeline. The documentation also states that, an advantage 
of this approach is that we can test, such as this Bash script, in 
isolation. And also, reducing the Pipeline code, making it easier to
manage and follow.

Following is a generic Jenkins Pipeline code, which uses the above script:

{% highlight pipeline linenos %}
pipeline {
    agent any

    stages {
        stage('Pytest') {
            steps {
                sh("${JENKINS_HOME}/scripts/pytest.sh ${WORKSPACE}")
            }
        }
		
        stage('Email Notification') {
            steps {
                mail(body: "${JOB_NAME}, build ${BUILD_NUMBER} Pytest completed.", subject: 'Pytest completed.', to: 'behai_nguyen@hotmail.com')
            }
        }		
    }
}
{% endhighlight %}

<ul>
<li style="margin-top:10px;">Line 7 -- environment variable <code>${JENKINS_HOME}</code>
is user <code>jenkins</code> home directory, <code>${WORKSPACE}</code> is the project
directory.
</li>

<li style="margin-top:10px;">Lines 13 -- send out a simple email whose body has
the project name and the build number. This is just a simple email, and is discussed in 
<a href="https://behainguyen.wordpress.com/2023/02/03/ci-cd-02-jenkins-basic-email-using-your-gmail-account/"
title="CI/CD #02. Jenkins: basic email using your Gmail account." target="_blank">CI/CD #02. Jenkins: basic email using your Gmail account.</a>
</li>
</ul>

## Updated on 07/06/2023 -- Starts

The above Jenkins Pipeline code will work ONLY with <code>Pipeline script from SCM</code>, discussed later. It does NOT ALWAYS work with <code>GitHub project</code>, also discussed later.

<strong><code>GitHub project</code> will not clone the repo automatically! I made the mistake of thinking that it does: possibly because I already had the repo cloned on the local Jenkins workspace.</strong>

We need to include the stage to clone the repo <code>Clone Git repo</code>. The Jenkins Pipeline code for <code>GitHub project</code>, hence, is:

```
pipeline {
    agent any

    stages {
        stage('Clone Git repo') {
            steps {
                git(
                    url: "https://github.com/behai-nguyen/bh_apistatus.git",
                    branch: "main",
                    changelog: false,
                    poll: false
                )
            }
        }
        
        stage('Pytest') {
            steps {
                sh("${JENKINS_HOME}/scripts/pytest.sh ${WORKSPACE}")
            }
        }
		
        stage('Email Notification') {
            steps {
                mail(body: "${JOB_NAME}, build ${BUILD_NUMBER} Pytest completed.", subject: 'Pytest completed.', to: 'behai_nguyen@hotmail.com')
            }
        }		
    }
}
```

Also, in <code>/var/lib/jenkins/scripts/pytest.sh</code>, the comment:

```
...
# The repo is cloned automatically by Jenkins. This script does the followings:
...
```

is no longer true. It should be changed to:

```
...
# This script does the followings:
...
```

## Updated on 07/06/2023 -- Ends

<h3>On double quotes (<code>""</code>) and single quotes (<code>''</code>)</h3>

In the above Pipeline script, <strong>line 7</strong> uses double quotes (<code>""</code>).
The first part of <strong>line 13</strong> uses double quotes (<code>""</code>), while the rest
uses single quotes (<code>''</code>). In Jenkins, this is known as 
<a href="https://www.jenkins.io/doc/book/pipeline/jenkinsfile/#string-interpolation"
title="String interpolation" target="_blank">String interpolation</a>. There 
are security implications when it comes to credentials, 
the document recommends using single quotes. But if I used single quotes,
the value of the environment variables would not come out, instead everything
within the single quotes comes out as a literal string. I.e.:

<code>'${JOB_NAME}, build ${BUILD_NUMBER} Pytest completed.'</code>

The output is a literal string:

<code>${JOB_NAME}, build ${BUILD_NUMBER} Pytest completed.</code>

I don't quite understand this yet. I need to keep this in mind.

Let's do a Jenkins Pipeline to test this. The repo I am using is 
<a href="https://github.com/behai-nguyen/bh_apistatus.git/"
title="https://github.com/behai-nguyen/bh_apistatus.git/"
target="_blank">https://github.com/behai-nguyen/bh_apistatus.git/</a>.
The name of the new Pipeline project should be <code>bh_apistatus</code>,
on the <strong>Configure</strong> page, check <code>GitHub project</code>,
then fill in the address of the repo, as seen:

![057-02.png](https://behainguyen.files.wordpress.com/2023/02/057-02.png)

Scroll down to <strong>Pipeline</strong>, and select <code>Pipeline script</code>,
the content is the Pipeline script code above:

![057-03.png](https://behainguyen.files.wordpress.com/2023/02/057-03.png)

Please note that, if we save the above Pipeline script code 
to a file at the root level of the project, for example 
<code>Jenkinsfile</code>, then check in this file as part of the source code,
then we could select <code>Pipeline script from SCM</code>,
and fill in the rest of the fields as:

{% include image-gallery.html list=page.gallery-image-list %}

<strong>Script Path</strong> is a free type field, and is defaulted to
<code>Jenkinsfile</code>, if we use some other name, ensure to enter
it correctly.

I have tested both implementations on more than one repo. I did not 
have any problem.

It's clearly better to store the Pipeline script code in a file, so that
we can use our preference IDE to edit it, and also keeping a history of bug
fixings and etc.

This post is yet another smaller step to understand Jenkins better.
I did enjoy investigating this. I hope you find the information useful.
Thank you for reading and stay safe as always.
