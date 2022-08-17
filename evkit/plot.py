import pandas as pd
import matplotlib.pyplot as plt


def plot_beta_wacc(beta, wacc):
    plt.style.use('ggplot')
    plt.figure(figsize=(10, 5))
    n = len(wacc)
    plt.scatter(x=beta_asset,
                y=wacc,
                edgecolor='black',
                linewidth=1,
                alpha=0.75)
    plt.title('Asset beta - WACC \nN = ' + str(n))
    plt.xlabel('Asset beta')
    plt.ylabel('WACC')
    plt.tight_layout()
    plt.show()


def plot_dcf_mkt_price(dcf_price, mkt_price):
    plt.style.use('seaborn')
    plt.figure(figsize=(10, 5))
    n = len(dcf_price)
    # plt.plot(
    #     dcf_price,
    #     linewidth=1,
    # )
    # plt.plot(
    #     mkt_price,
    #     linewidth=1,
    #     alpha=0.75
    # )
    plt.scatter(x=mkt_price, y=dcf_price / mkt_price, linewidth=1, alpha=0.75)
    plt.xscale('log')
    # plt.yscale('log')
    plt.title('DCF-WACC stock price to market quote \nN = ' + str(n))
    plt.xlabel('DCF-WACC / Market quote')
    plt.ylabel('Market quote')
    plt.tight_layout()
    plt.show()


file_name = 'healthcare-20190616.csv'
path_csv = '../reports/' + file_name

data = pd.read_csv(path_csv)
beta_asset = data['beta_asset']
wacc = data['wacc']
mkt_price = data.mkt_stock_price
dcf_price = data.stock_price
ratio = dcf_price / mkt_price

plot_beta_wacc(beta=beta_asset, wacc=wacc)
plot_dcf_mkt_price(dcf_price, mkt_price)
