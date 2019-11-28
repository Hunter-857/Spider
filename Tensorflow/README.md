# 安装 Jupyter
    #激活自己的python 环境 
    activate envname 
    pip install jupter
    #指定 Jupyter 使用的内核
    python -m ipykernel intall --user --name = env
    #查看 Jupyter的 kernel 
    jupyter kernelspec list
    # 启动 Jupyter
    jupyter notebook 
# TensorFlow 数据流图是一种声明式的编程范式
  建立数学模型表达式的变换偏向于数理逻辑
  ## 张量
  在数学中，张量是一种几何实体，广义上表述任意形式的数据
  
  TensorFlow 中则表示某种相同数据类型的多维数据，用来表现多维数据
  
  常用的几类张量:
  
    tf.constant //常量
    tf.placeholder //占位符
    tf.Variable // 变量
        
   