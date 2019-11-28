# coding=utf-8
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.feature_extraction import DictVectorizer
# 1数据读入
train_data = pd.read_csv('./train.csv')
test_data = pd.read_csv('./test.csv')
train_data.head()
train_data.tail()
train_data.describe()


# 使用平均年龄填充缺失的值
train_data['Age'].fillna(train_data['Age'].mean, inplace=True)
test_data['Age'].fillna(test_data['Age'].mean, inplace=True)
# 使用平均机票填充缺失的值
train_data['Fare'].fillna(train_data['Fare'].mean, inplace=True)
test_data['Fare'].fillna(test_data['Fare'].mean, inplace=True)
train_data['Embarked'].value_counts()

train_data['Embarked'].fillna('S', inplace=True)
test_data['Embarked'].fillna('S', inplace=True)

features = ['Pclass', 'Sex', 'Age', 'SibSp', 'Parch', 'Fare', 'Embarked']
train_features = train_data[features]
test_features = train_data[features]
train_labels = train_data['Survived']

print (train_features.info())
dvec = DictVectorizer(sparse=False)
train_features = dvec.fit_transform(train_features.to_dict(orient='record'))

# 构造 ID3 决策树
clf = DecisionTreeClassifier(criterion='entropy')
# 决策树训练
clf.fit(train_features, train_labels)

test_features=dvec.transform(test_features.to_dict(orient='record'))
# 决策树预测
pred_labels = clf.predict(test_features)

# 得到决策树准确率
acc_decision_tree = round(clf.score(train_features, train_labels), 6)
print(u'score 准确率为 %.4lf' % acc_decision_tree)


