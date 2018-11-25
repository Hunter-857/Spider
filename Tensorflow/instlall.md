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