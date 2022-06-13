import pandas as pd
import numpy as np

emp_df = pd.read_csv('/Users/user/dataknows/emp_funds_compare/boolio.csv', encoding='utf-8-sig')
rg_df = pd.read_excel('/Users/user/dataknows/richgo_tax_0510.xlsx')

emp_df = emp_df.drop(columns='ticker')
rg_df = rg_df.rename(columns={'Unnamed: 0': 'base_dt'})
rg_df = rg_df.set_index('base_dt')

emp_df = pd.pivot(emp_df, index='base_dt', columns='product_name', values='adj_pr')

rg_df.index = pd.to_datetime(rg_df.index)
emp_df.index = pd.to_datetime(emp_df.index)

df = emp_df.join(rg_df, how='outer')


def calc_pct_change(df):
    chg_df = df.pct_change() + 1
    chg_df.iloc[0] = 100
    chg_df = chg_df.cumprod()
    return chg_df


def calc_ann_return(df):
    p = (df.index[-1] - df.index[0]).days / 365
    ann_return = ((df.iloc[-1] / df.iloc[0]) ** (1 / p) - 1).rename('ann_return')
    return ann_return


def calc_ann_vol(df):
    ann_vol = (df.pct_change().std(ddof=0) * np.sqrt(365)).rename('ann_vol')
    return ann_vol


def calc_sharpe_ratio(df, riskfree=None):
    if riskfree is None:
        riskfree = 0
    else:
        riskfree = riskfree
    ann_return = calc_ann_return(df)
    ann_vol = calc_ann_vol(df)
    sharpe_ratio = np.where((ann_return - riskfree) >= 0,
                            (ann_return - riskfree) / ann_vol,
                            (ann_return - riskfree) * ann_vol)
    sharpe_ratio = pd.Series(index=ann_return.index, data=sharpe_ratio)
    return sharpe_ratio


def calc_mdd(df):
    mdd = (df.div(df.cummax()).sub(1).min().abs()).rename('mdd')
    return mdd


def to_csv(df, sharpe, mdd):
    df.to_csv('/Users/user/dataknows/boolio_richgo.csv', encoding='utf-8-sig')
    sharpe.to_csv('/Users/user/dataknows/boolio_sharpe.csv', encoding='utf-8-sig')
    mdd.to_csv('/Users/user/dataknows/boolio_mdd.csv', encoding='utf-8-sig')


if __name__ == '__main__':
    df = calc_pct_change(df)
    sharpe = calc_sharpe_ratio(df)
    mdd = calc_mdd(df)
    to_csv(df, sharpe, mdd)

das = 000
