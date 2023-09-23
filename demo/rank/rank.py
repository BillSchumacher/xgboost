#!/usr/bin/python
from sklearn.datasets import load_svmlight_file

import xgboost as xgb
from xgboost import DMatrix

#  This script demonstrate how to do ranking with xgboost.train
x_train, y_train = load_svmlight_file("mq2008.train")
x_valid, y_valid = load_svmlight_file("mq2008.vali")
x_test, y_test = load_svmlight_file("mq2008.test")

group_train = []
with open("mq2008.train.group", "r") as f:
    data = f.readlines()
    group_train.extend(int(line.split("\n")[0]) for line in data)
group_valid = []
with open("mq2008.vali.group", "r") as f:
    data = f.readlines()
    group_valid.extend(int(line.split("\n")[0]) for line in data)
group_test = []
with open("mq2008.test.group", "r") as f:
    data = f.readlines()
    group_test.extend(int(line.split("\n")[0]) for line in data)
train_dmatrix = DMatrix(x_train, y_train)
valid_dmatrix = DMatrix(x_valid, y_valid)
test_dmatrix = DMatrix(x_test)

train_dmatrix.set_group(group_train)
valid_dmatrix.set_group(group_valid)

params = {'objective': 'rank:ndcg', 'eta': 0.1, 'gamma': 1.0,
          'min_child_weight': 0.1, 'max_depth': 6}
xgb_model = xgb.train(params, train_dmatrix, num_boost_round=4,
                      evals=[(valid_dmatrix, 'validation')])
pred = xgb_model.predict(test_dmatrix)
