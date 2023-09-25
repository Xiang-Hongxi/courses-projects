import numpy as np
import pandas as pd
import sklearn.model_selection as ms
import sklearn.linear_model as lm
import sklearn.metrics as mt

df_train = pd.read_csv("C:/Users/Lenovo/Desktop/Task 1a/train.csv")
X = df_train[["x1","x2","x3","x4","x5","x6","x7","x8","x9","x10","x11","x12","x13"]]
y = df_train["y"]

lamda_set = np.array([0.1,1,10,100,200])

cv = ms.KFold(n_splits=10, shuffle=True,random_state=17)

RMSE = np.zeros(5)

i=0
for lamda in lamda_set:
    model = lm.Ridge(alpha=lamda, fit_intercept=False, copy_X=True)
    scores = ms.cross_val_score(model, X, y, cv=cv, scoring='neg_root_mean_squared_error')
    RMSE[i] = -scores.mean()
    i=i+1

output = pd.DataFrame(data = RMSE)
output.to_csv("C:/Users/Lenovo/Desktop/Task 1a/submit.csv",index = False, header = None)

