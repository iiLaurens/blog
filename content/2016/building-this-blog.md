Title: Building this blog
Slug: building-this-blog
Date: 2016-05-01 15:17
Tags: Python, Pelican, Github pages
Author: Laurens

With the creation of this site I immediately have a topic to write about. In this
post I hope to document how to copy this static blog that is created using *Pelican*
and hosted on *Github Pages*. In doing so I hope that anyone (mostly future me) can
replicate my blog with minimal effort. The only requirements are a Python distribution with virtual environments ([Anaconda](https://www.continuum.io/downloads) is assumed here), git and Windows. I assume that everybody is already familiar with the concept of a static blog.

# Obtaining the blog's requirements
The source for this blog can be found in my [Github repository](https://github.com/iiLaurens/blog). Simply clone the contents to a local
folder and build the minimum Python (v2.7 in this case) environment in a suitable folder, such as `venv`.

After that activate the python environment with the command `activate ./venv` and install
the required packages. This static blog is created using *Pelican*.

```bash
git clone https://github.com/iiLaurens/blog.git
cd blog
conda create -p venv python=2.7
activate ./venv
pip install -r requirements.txt
```

Now we should be all set to build the actual static website!

# Building the blog using Pelican
The way this blog works is that it takes a folder with notes (in this case Markdown files) and build a nice static blog from it. In this case, all the content is in the appropiately named `content` folder. Make sure that the virtual python environment is still active and start building with Pelican. The first argument should be the folder that holds the content and additionally we have to supply the settings config so that the blog actually works the way I wanted it. The blog in it's entirety is build in the `output` folder.
```bash
pelican content -s pelicanconf.py
```
Ideally, we check whether the blog displays correctly before sending it to the world. This is simply possible by starting a simple local HTTP Server in the `output` folder. Make sure that the site url is updated accordingly in the blog's settings in `pelicanconf.py` to, for example, `http://localhost:8000`.
```bash
cd output
python -m SimpleHTTPServer
```
If everything looks nice and peachy then revert the site url in the settings file and get ready to upload the blog!

# Uploading to Github Pages
Before uploading, be sure that you have a Git repository on Github that is named `<username>.github.io`. If so, simply push the output folder to this repository but start by (re)initialising a git repo in the `output` folder.
```bash
git init
git add .
git commit -m "add static blog"
git push https://<username>:<password>@github.com/<username>/<username>.github.io.git master --force
```
The reason that I apply a forcefull push here is to circumvent any problems that might arise when the repository already exists on github and is not empty.

And just like that, we have obtained a copy of the source of this blog, recreated it and uploaded it to your own Github User pages. It is recommended to keep a seperate repository with the source of the blog and update it whenever it is changed.
