import json
import glob
import pandas as pd
import seaborn as sns
import matplotlib.colors as mcolors
import math
import itertools
import matplotlib.pyplot as plt
import numpy as np
import tqdm
import gc

import json


colors = list(mcolors.BASE_COLORS)
del colors[7]


def load_config(json_file="config.json"):
    return json.load(open(json_file))


def get_filenames(dir, file_type="csv"):
    return glob.glob(f"{dir}/*.{file_type}")


def del_list(lst):
    for i in lst:
        del i
    del lst


def get_dfs_from_filenames(filenames, type="csv", chunk_size=100):
    res = []
    temp = None
    for filename in tqdm.tqdm(filenames):
        if (type == "csv"):
            res.append(pd.read_csv(filename))
        if (type == "json"):
            d = json.load(open(filename))
            df = pd.DataFrame(d)
            df["http_filename"] = filename
            res.append(df)

        if (len(res) >= chunk_size):
            temp = pd.concat(res)
            del_list(res)
            gc.collect()
            res = [temp]

    return pd.concat(res)


def get_df(dir):
    csv_names = glob.glob(dir)
    res = []
    for i in csv_names:
        res.append(pd.read_csv(i))
        res[-1]["chunk_csv_name"] = i.split("/")[-1]
    return pd.concat(res)


def plot_cdf(data, label=None, lw=None, markevery=0.1, bw=1, color=None):
    sns.kdeplot(label=label, data=data, cumulative=True, bw_method=bw,
                linewidth=lw, markevery=markevery, color=color)


def plot_pdf(data, bw=1, discrete=True, bins="auto", color=None, kde=True):
    ax_1 = sns.histplot(data, color=color, stat="probability", kde=kde, kde_kws={
                        "bw_method": bw}, discrete=discrete, bins=bins)


def get_unique_values_from_key(df, keys):
    res_dict = {}
    res_list = []

    for key in keys:
        value = list(df[key].unique())
        res_dict[key] = value
        res_list.append(value)

    return res_dict, res_list


def build_query(params, keys, relationship="&"):
    res = ""
    for i in range(len(params)):
        param = params[i]
        key = keys[i]
        if (i == 0):
            if (type(param) is np.bool_):
                res += f" {key} == {param}"
            else:
                res += f" {key} == '{param}'"
        else:
            if (type(param) is np.bool_):
                res += f" & {key} == {param}"
            else:
                res += f" & {key} == '{param}'"
    return res


def plot_multiple_cdfs(df, keys, plot_key, is_cdf=True, is_discrete=False, bw=1, kde=True, group_num=None, group_legends=[[]], xlim=(0, 1), xlabel=None, pallete=None, bins="auto"):
    res_dict, res_list = get_unique_values_from_key(df, keys)
    combos = list(itertools.product(*res_list))
    legends = []
    group_count = 0
    for i in range(len(combos)):
        params = combos[i]
        query = build_query(params, keys)
        data = df.query(f"{query}")
        if (pallete != None):
            colors = pallete
        else:
            colors = list(mcolors.BASE_COLORS)

        if (len(data) == 0):
            continue

        color_index = i % len(colors)
        if (group_num != None):

            color_index = i % group_num

        if (is_cdf):
            plot_cdf(data[plot_key], bw=bw, color=colors[color_index])
        else:
            plot_pdf(data[plot_key], color=colors[color_index],
                     discrete=is_discrete, kde=kde, bins=bins)
        group_count = group_count + 1
        print("combo: {}, Mean: {}, Median: {}".format(
            params, data[plot_key].mean(), data[plot_key].median()))
        legends.append(params)

        if (group_num != None and group_count >= group_num):
            batch = math.floor(i/group_num)
            plt.legend(group_legends[batch])
            plt.xlim(xlim)
            plt.xlabel(xlabel)
            group_count = 0
            plt.show()

    if (group_legends == [[]]):
        plt.legend(legends)

    # print(len(combos))

    # print(bin_counter)

    # print(colors)
