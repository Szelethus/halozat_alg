import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import glob


def concat_csvs():
    path = '.' # use your path
    all_files = glob.glob(path + "/*.csv")

    li = []

    for filename in all_files:
        df = pd.read_csv(filename, index_col=None, header=0)
        li.append(df)

        df = pd.concat(li, axis=0, ignore_index=True)
    return df

def groom_data(df):
    df = df.drop(['node visit sequence', 'node exploration sequence', 'port encoding', 'port sequence'], axis=1)
    df["was route successful"] = df["was route successful"].astype(int)
    df["upper boundary for runtime"] = np.power((df["number of nodes"]),2)
    return df

def plot_succ_density_backtrack(df):
    df_density_var = df[['number of nodes','graph density', 'was route successful']].groupby(['number of nodes']).mean()
    ax = plt.gca()

    df_density_var.plot(kind='line',y='was route successful', label='success rate',ax=ax)
    plt.title('Success rate - with constant node number and varying density')
    plt.savefig('success_constnode_vardenst.png')
    


def plot_succ_density_node(df):
    df_node_var = df[['number of nodes','graph density', 'was route successful']].groupby(['graph density']).mean()
    ax = plt.gca()

    df_node_var.plot(kind='line',y='was route successful', label='success rate',ax=ax)
    plt.title('Success rate - with constant density and varying node number')
    plt.savefig('success_constdenst_varnode.png')
    

def plot_time_node_edge(df):
    df_edges_var = df[['number of nodes','number of edges', 'time']].groupby(['number of nodes']).mean()
    ax = plt.gca()

    df_edges_var.plot(kind='line',y='time', label='time(sec)',ax=ax)
    plt.title('Running time - with constant node number and varying edge number')
    plt.savefig('time_constnode_vardenst.png')
    

def plot_backtrack_nodes_edges(df):
    df_backtrack_var = df[['number of nodes','number of edges', 'backtrack length']].groupby(['number of nodes']).mean()
    ax = plt.gca()

    df_backtrack_var.plot(kind='line',y='backtrack length', label='avg backtrack length in round',ax=ax)
    plt.title('Avg backtrack length - with constant node number and varying edge number')
    plt.savefig('avgbacktrack_constnode_varedge.png')
    

def plot_lefacount_denst_nodes(df):
    df_backtrack_var = df[['number of nodes','graph density', 'tree leaf count']].groupby(['number of nodes']).mean()
    ax = plt.gca()

    df_backtrack_var.plot(kind='line',y='tree leaf count', label='avg backtrack length in round',ax=ax)
    plt.title('Avg number of tree leaf - with constant node number and varying density')
    plt.savefig('avgtreeleaf_constnode_vardenst.png')
    

def plot_exploration_length(df):
    ax = plt.gca()
    df_round= df.groupby(['exploration length']).mean()
    df_round.plot(kind='line',y='reverse edges taken',ax=ax)
    df_round.plot(kind='line',y='forward edges taken', color='red',ax=ax)
    df_round.plot(kind='line',y='reverse edges taken', color='yellow',ax=ax)
    df_round.plot(kind='line',y='backtrack length', color='gray',ax=ax)
    plt.savefig('exp_length.png')

    
    plt.savefig('round.png')

def bar_plot(df):
    fig, ax = plt.subplots(figsize=(8,8))

    X = ['Unsuccessful routes', 'Successful routes']
    X_axis = np.arange(len(X))
    ratio = 0.1

    df_success = df.groupby(['was route successful']).mean()

    plt.bar(X_axis - 0.4, df_success['number of edges'], ratio, label = 'Avg number of edges')
    plt.bar(X_axis - 0.3, df_success['number of nodes'], ratio, label = 'Avg number of nodes')
    plt.bar(X_axis - 0.2, df_success['graph density'], ratio, label = 'Avg graph density')
    plt.bar(X_axis - 0.1, df_success['exploration length'],ratio, label = 'Avg exploration length')
    plt.bar(X_axis + 0.0, df_success['backtrack length'], ratio, label = 'Avg backtrack length')
    plt.xticks(X_axis, X)

    plt.legend()
    plt.savefig('bar_plot.png')

def plot_upper_bound(df):
    ax = plt.gca()
    df_gr = df.groupby(['number of nodes']).mean()
    df_gr['avg successful route'] = df_gr['was route successful']
    df_gr.plot(kind='line',y='exploration length',ax=ax)
    df_gr.plot(kind='line',y='upper boundary for runtime', color='red',ax=ax)

    
    plt.savefig('upper_bound.png')

def create_plots():
    df = concat_csvs()
    df = groom_data(df)
    plot_succ_density_backtrack(df)
    plot_succ_density_node(df)
    plot_time_node_edge(df)
    plot_backtrack_nodes_edges(df)
    plot_lefacount_denst_nodes(df)
    plot_exploration_length(df)
    bar_plot(df)
    plot_upper_bound(df)

create_plots()
