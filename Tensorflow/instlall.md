#Tensor flow Install
 ## CPU 和 GPU 的 不同版本 
    
    pip install tensorflow  --cpu
    pip install tensorflow-gpu   --gpu 
    
    pip uninstall tensorflow 
  
  ## Conda 要支持虚拟环境 需要安装插件
    jupyter notebook 安装 jupyter
    conda install nb_conda
    python -m ipykernel install --user --name DL --display-name "deeplearningproject"
    注：上述两个 deeplearningproject，前者是自身环境名称，不能变化；后者是在jupyter notebook的显示名称，可修改。
    
首先使用jupyter kernelspec list查看安装的内核和位置
进入安装内核目录打开kernel.jason文件，查看Python编译器的路径是否正确
如果不正确修改为正确的安装路径，我修改后的路径为： 
"D:\\Program Files\\Anaconda3\\envs\\tensorflow\\python.exe"
重启jupyter
