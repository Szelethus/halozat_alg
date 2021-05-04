import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import glob
import time



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
    df['number of edges'] = pd.to_numeric(df['number of edges'],errors='coerce')
    df['number of nodes'] = pd.to_numeric(df['number of nodes'],errors='coerce')
    df['oracle type'] = pd.to_numeric(df['oracle type'],errors='coerce')
    df['tree forward edges'] = pd.to_numeric(df['tree forward edges'],errors='coerce')
    df['tree reverse edges'] = pd.to_numeric(df['tree reverse edges'],errors='coerce')
    df['tree leaf count'] = pd.to_numeric(df['tree leaf count'],errors='coerce')
    df['tree root id'] = pd.to_numeric(df['tree root id'],errors='coerce')
    df['route root'] = pd.to_numeric(df['route root'],errors='coerce')
    df['robot starting node'] = pd.to_numeric(df['robot starting node'],errors='coerce')
    df['exploration length'] = pd.to_numeric(df['exploration length'],errors='coerce')
    df['forward edges taken'] = pd.to_numeric(df['forward edges taken'],errors='coerce')
    df['reverse edges taken'] = pd.to_numeric(df['reverse edges taken'],errors='coerce')
    df['backtrack length'] = pd.to_numeric(df['backtrack length'],errors='coerce')
    df["upper boundary for runtime"] = np.power((df["number of nodes"]),2)
    return df

def plot_succ_density_backtrack(df):
    df_density_var = df[['number of nodes','graph density', 'was route successful']].groupby(['number of nodes']).mean()
    ax = plt.gca()

    df_density_var.plot(kind='line',y='was route successful', label='success rate',ax=ax)
    plt.title('Success rate - with constant node number and varying density')
    plt.ylabel("success rate")
    plt.savefig('success_constnode_vardenst.png', bbox_inches='tight')
    


def plot_succ_density_node(df):
    df_node_var = df[['number of nodes','graph density', 'was route successful']].groupby(['graph density']).mean()
    ax = plt.gca()
    plt.ylabel("success rate")
    df_node_var.plot(kind='line',y='was route successful', label='success rate',ax=ax)
    plt.title('Success rate - with constant density and varying node number')
    plt.savefig('success_constdenst_varnode.png', bbox_inches='tight')
    time.sleep(60)
    

def plot_time_node_edge(df):
    df_edges_var = df[['number of nodes','number of edges', 'time']].groupby(['number of nodes']).mean()
    ax = plt.gca()
    plt.ylabel("time(sec)")
    df_edges_var.plot(kind='line',y='time', label='time(sec)',ax=ax)
    plt.title('Running time - with constant node number and varying edge number')
    plt.savefig('time_constnode_vardenst.png', bbox_inches='tight')
    time.sleep(60)

def plot_backtrack_nodes_edges(df):
    df_backtrack_var = df[['number of nodes','number of edges', 'backtrack length']].groupby(['number of nodes']).mean()
    ax = plt.gca()
    plt.ylabel("avg backtrack length(round)")
    df_backtrack_var.plot(kind='line',y='backtrack length', label='avg backtrack length in round',ax=ax)
    plt.title('Avg backtrack length - with constant node number and varying edge number')
    plt.savefig('avgbacktrack_constnode_varedge.png', bbox_inches='tight')
    time.sleep(60)

def plot_lefacount_denst_nodes(df):
    df_backtrack_var = df[['number of nodes','graph density', 'tree leaf count']].groupby(['number of nodes']).mean()
    ax = plt.gca()
    plt.ylabel("avg leaf tree count")
    df_backtrack_var.plot(kind='line',y='tree leaf count', label='avg backtrack length in round',ax=ax)
    plt.title('Avg number of tree leaf - with constant node number and varying density')
    plt.savefig('avgtreeleaf_constnode_vardenst.png', bbox_inches='tight')
    time.sleep(60)

def plot_exploration_length(df):
    ax = plt.gca()
    
    df_round= df.groupby(['exploration length']).mean()
    df_round.plot(kind='line',y='reverse edges taken',ax=ax)
    df_round.plot(kind='line',y='forward edges taken', color='red',ax=ax)
    df_round.plot(kind='line',y='reverse edges taken', color='yellow',ax=ax)
    df_round.plot(kind='line',y='backtrack length', color='gray',ax=ax)
    plt.ylabel('avg')
    plt.savefig('exp_length.png', bbox_inches='tight')
    time.sleep(60)
    
    # plt.savefig('round.png')

def bar_plot(df):
    df_success = df.groupby(['was route successful']).mean()
    fig, ax = plt.subplots(figsize=(8,8))

    X = ['Unsuccessful routes', 'Successful routes']
    X_axis = np.arange(len(X))
    ratio = 0.1

    plt.bar(X_axis - 0.3, df_success['number of nodes'], ratio, label = 'Avg number of nodes')
    plt.bar(X_axis - 0.2, df_success['graph density'], ratio, label = 'Avg graph density')
    plt.bar(X_axis - 0.1, df_success['exploration length'],ratio, label = 'Avg exploration length')
    plt.bar(X_axis + 0.0, df_success['backtrack length'], ratio, label = 'Avg backtrack length')
    plt.bar(X_axis + 0.1, df_success['forward edges taken'], ratio, label = 'Avg forward edge taken')
    plt.bar(X_axis + 0.2, df_success['reverse edges taken'], ratio, label = 'Avg reverse edge taken')
    plt.xticks(X_axis, X)
    plt.ylabel('avg')
    plt.legend()
    plt.savefig('bar_plot.png', bbox_inches='tight')
    time.sleep(60)

def plot_upper_bound(df):
    ax = plt.gca()
    df_gr = df.groupby(['number of nodes']).mean()
    df_gr['avg successful route'] = df_gr['was route successful']
    df_gr.plot(kind='line',y='exploration length',ax=ax)
    df_gr.plot(kind='line',y='upper boundary for runtime', color='red',ax=ax)
    plt.ylabel('number of steps')
    
    plt.savefig('upper_bound.png', bbox_inches='tight')
    time.sleep(60)
    
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
