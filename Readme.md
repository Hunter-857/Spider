写了一个简单爬虫

使用notedown插件来读写github源文件

注意：这个只推荐给想上github提交改动的小伙伴。 我们源代码是用markdown格式来存储，而不是jupyter默认的ipynb格式。我们可以用notedown插件来读写markdown格式。下面命令下载源代码并且安装环境：

git clone https://github.com/mli/gluon-tutorials-zh
cd gluon-tutorials-zh
conda env create -f environment.yml
source activate gluon # Windows下不需要 source

然后安装notedown，运行Jupyter并加载notedown插件：

pip install https://github.com/mli/notedown/tarball/master
jupyter notebook --NotebookApp.contents_manager_class='notedown.NotedownContentsManager'

【可选项】默认开启notedown插件

首先生成jupyter配置文件（如果已经生成过可以跳过）

jupyter notebook --generate-config

将下面这一行加入到生成的配置文件的末尾（Linux/macOS一般在~/.jupyter/jupyter_notebook_config.py)

c.NotebookApp.contents_manager_class = 'notedown.NotedownContentsManager'

之后就只需要运行jupyter notebook即可。

需要在项目所在路径下激活环境来并且查看代码


