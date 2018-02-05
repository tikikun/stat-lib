import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
from statsmodels.formula.api import ols


def gen_dum(data, dummy_name, condition_name, condition):
    result = pd.DataFrame()
    for col in data.columns:
        result[col] = data[col]
    result[dummy_name] = (result[condition_name] > condition).astype(int)
    return result


class drop():
    def __init__(self, data, var_name):
        self.Data = data
        self.Var_name = var_name

    def more(self, condition):
        roller = self.Data[self.Var_name] > condition
        condition_index = self.Data[roller].index
        return self.Data.drop(condition_index)

    def less(self, condition):
        roller = self.Data[self.Var_name] < condition
        condition_index = self.Data[roller].index
        return self.Data.drop(condition_index)

    def equal(self, condition):
        roller = self.Data[self.Var_name] = condition
        condition_index = self.Data[roller].index
        return self.Data.drop(condition_index)


class lin_reg():
    def __init__(self, data):
        self.Data = data

    def stat_table(self, model_des):
        model = ols(model_des, self.Data).fit()
        return model

    def graph(self, x_name, y_name, set_size=5, set_aspect=1, dot_size=10):
        g = sns.regplot(x=x_name, y=y_name,
                        scatter_kws={"s": dot_size},
                        data=self.Data)
        if set_aspect > 1:
            xlen = set_size*set_aspect
            ylen = set_size
        elif set_aspect <= 1:
            xlen = set_size
            ylen = set_size*set_aspect
        g.figure.set_size_inches(xlen, ylen)

    def graph_int(self, x_name, y_name, dummy_target, condition,
                  set_size=8, set_aspect=2, dot_size=10):
        dummy_var = 'dum_' + dummy_target
        data_dum = gen_dum(self.Data, dummy_var, dummy_target, condition)
        sns.lmplot(x=x_name, y=y_name, hue=dummy_var, ci=False, data=data_dum,
                   size=set_size, aspect=set_aspect, palette="Set1",
                   scatter_kws={"s": dot_size}, line_kws={"lw": 1})

    def grid_4(self, x_name, y_name, dummy_target, condition,
               extra_dum=None, set_size=3, set_aspect=1,dot_size=1):
        dummy_var = 'dum_' + dummy_target
        data_dum = gen_dum(self.Data, dummy_var, dummy_target, condition)
        g = sns.FacetGrid(data_dum, row=extra_dum, col=dummy_var,
                          margin_titles=True, size=set_size, aspect=set_aspect)
        g.map(sns.regplot, x_name, y_name, color="black",
              fit_reg=True, x_jitter=.1, scatter_kws={"s": dot_size})
