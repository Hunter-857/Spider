# coding=utf-8
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
# 二乘偏差均值
from sklearn.metrics import mean_absolute_error
# 绝对值偏差均值
from sklearn.datasets import load_digits
# 引入 digits 数据集
from sklearn.metrics import accuracy_score
# 测试结果的准确性
from sklearn import tree
import graphviz
import matplotlib.pyplot as plt  # doctest: +SKIP


def look_data():
    plt.gray()  # doctest: +SKIP
    plt.matshow(digits.images[0])  # doctest: +SKIP
    plt.show()  # doctest: +SKIP


# 准备数据集
digits = load_digits()
# look_data()
# 获取数据集的特征集和分类标识
features = digits.data
labels = digits.target
# 随机抽取 33% 的数据作为测试集，其余为训练集
train_features, test_features, train_labels, test_labels = train_test_split(features, labels, test_size=0.33, random_state=0)
# 创建 CART 分类树
clf = tree.DecisionTreeClassifier(criterion='gini')
# 拟合构造分类树
clf = clf.fit(train_features, train_labels)
# 用 CART 分类树做预测
test_predict = clf.predict(test_features)
# 预测结果与测试集作对比
score = accuracy_score(test_labels, test_predict)
# 输出准确率
print('准确率 %.4f'%score)
dot_data = tree.export_graphviz(clf, out_file=None)
graph = graphviz.Source(dot_data)
# 输出分类树图示
graph.view()
