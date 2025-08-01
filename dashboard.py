import streamlit as st
from PIL import Image
import os
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

dataset_names = {
    "11cdff15": "Fujitsu PRIMERGY BX924 S4",
    "b8994569": "Lenovo ThinkSystem SD530",
    "a97fe24e": "Lenovo ThinkSystem SR630",
    "5f67cb23": "Lenovo ThinkSystem SR650",
    "f6fec747": "Dell PowerEdge C6420",
    "a6177608": "Lenovo ThinkSystem SR630 V2 "
}


available_nodes = {
'a97fe24e': {'0eb86326', '7f3747b5', 'ba36d475', 'd5a5fc09', 'fe2955c5'},
 'b8994569': {'0ad2c0c4','2dbc131e', '341872a6', '41721e4b', '5180b174','5333662e','5ede733f',
            '6fdf4d0d','8674a4f2', '8ccd7b3c','8d5a6c7e','a2ffa1e3', 'b9c737a2','bce59923','bd55f82d',
            'c658b44f','e5886d85','eb5d8f42','f006f6ea', 'f301a5e3'},
 'a6177608': {'00366801','0049db0c','0064a367','0065ef1b','05c5ef00','0861be67','111896c8','1125a01c',
            '13a6f4c8','1d247e53','1e64c783','22655375','22655375','25fe225b','28e8b849','2eea5215',
            '2fded806','366801','366801','391ea34d','3d7960e7','417242bc','43e593b3','46de937b',
            '4786760b','497660f4','49964896','49964896','51244a6f','5433c3e6','54c3811d','58512373',
            '58512373','5d7db037','5e87c22e','6a1acc69','6bb5c698','6d834fb8','764b2e98','788b0a71',
            '7c7d255d','7da5db71','7f4f3762','82415d68','85c6cd05','85ebbabd','8621bb59','88b02143',
            '8bab4dff','8d2843f5','98811351','98811351','a22bdd7c','a26788f6','a4ec376f','a57bfdd7',
            'b1b36b26','b6002837','b88cae4d','bb37a269','cbf4a974','ce52f982','d424b38d','d7ea95c2',
            'de50c1fe','e2b6ed0e','e41df102','e4362c19','e998d442','ea7f6999','fd5a1b56'},
 'f6fec747': {'3176c89e','4791e4fe','6ff55332','7e99a5c6','7f384201','a2ff297e','b022aa11','c2736b43'},
 '5f67cb23': {'06764465','184b905d','3a4828f5','46362b76','4985a7cf','4d8b845e','578d99bd','6342c79e',
              '668c569c','6764465','7c804642','972da8ab','a484c600','a639d055','a9e38583','bb1bcaff',
              'c9900ab9''d35334d1','d8d6d1e0','dda1bb77','fb77ceef'},
 '11cdff15': {'0d4840c3','21e01022','2d2d0311','3eb76848','4a4cffb4','54f5286d','5c5e400b','77d57e28',
              '79b5307d','a2f271b4','b654db47','cfc400f1'}}


st.header(f'Data-driven analyse')
overview = f'combined/Statistics/summary_architectures.csv'
if os.path.exists(overview):
    view = pd.read_csv(overview, index_col=0)
    st.subheader("Overview of the dataset")
    st.dataframe(view)
else:
    st.warning(f"Table not found")

# ---------- Power
selected_name = st.selectbox("Choose the machine type you want to analyse:", list(dataset_names.values()), key="machine_type_select")
selected_machine = [k for k, v in dataset_names.items() if v == selected_name][0]


st.subheader(f'ipmi_system_power_watts described (Watt)')
descriptive = pd.read_csv(f'combined/descriptive/descriptive_{selected_machine}.csv')
st.dataframe(descriptive)

# Boxplot


boxplot_stats = pd.read_csv(f'combined/boxplots/boxplot_stats_{selected_machine}.csv')
node_options = sorted(set(available_nodes[selected_machine]) & set(boxplot_stats['node']))
selected_node = st.selectbox("Choose node (boxplot):", node_options, key="boxplot_node_select")


subset = boxplot_stats[boxplot_stats['node'] == selected_node]

if not subset.empty:
    stats = subset.iloc[0]
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bxp([{
        'med': stats['median'],
        'q1': stats['q1'],
        'q3': stats['q3'],
        'whislo': stats['lower_whisker'],
        'whishi': stats['upper_whisker'],
        'fliers': []
    }], showfliers=False)
    ax.set_title(f"Boxplot IPMI Power for node {selected_node}")
    ax.set_ylabel('IPMI System Power (Watt)')
    st.pyplot(fig)
else:
    st.warning(f"No boxplot data available for node {selected_node}")

outliers_path = f"combined/outliers/outlier_{selected_machine}.csv"
if os.path.exists(outliers_path):
    outliers = pd.read_csv(outliers_path, index_col=0)
    st.subheader("Outliers bar chart")
    st.bar_chart(outliers)
else:
    st.warning(f"Outliers data niet gevonden voor {selected_machine}")


power_img_path = f"combined/Statistics/power_distribution_per_node_{selected_machine}.png"
if os.path.exists(power_img_path):
    power_img = Image.open(power_img_path)
    st.subheader("Power distribution per node")
    st.image(power_img, use_container_width=True)
else:
    st.warning(f"Power distribution plot niet gevonden voor {selected_machine}")

# ---------- PCA
pca_img_path = f"combined/pca/plot_hourly_nodes_{selected_machine}.png"
if os.path.exists(pca_img_path):
    pca_img = Image.open(pca_img_path)
    st.subheader("PCA plot of node behavior")
    st.image(pca_img, use_container_width=True)
else:
    st.warning(f"PCA plot niet gevonden voor {selected_name}")


# ---------- Clusters

st.subheader(f'Clusters')
node_options = sorted(available_nodes[selected_machine])
selected_node_cluster = st.selectbox("Choose node (cluster):", node_options, key="cluster_node_select")

img_path = f"combined/clusters/{selected_machine}/pca_cluster_{selected_node}.png"
clus_path = f"combined/Timeline/{selected_machine}/Timeline_clusters__{selected_node}.png"

col1, col2 = st.columns(2)
with col1:
    if os.path.exists(img_path):
        st.image(Image.open(img_path), caption=f'Clustering per node {selected_node}', use_container_width=True)
    else:
        st.warning(f"Image not found: {img_path}")

with col2:
    if os.path.exists(clus_path):
        st.image(Image.open(clus_path), caption=f'Timeline per node {selected_node}', use_container_width=True)
    else:
        st.warning(f"Image not gound: {clus_path}")
  

distribution_path = f'combined/clusters/outlier_{selected_machine}.csv'
if os.path.exists(distribution_path):
    distribution = pd.read_csv(distribution_path, index_col=0)
    distribution.index.name = "Node"  # Set index as 'Node'

    st.subheader("Distribution per Node")

    fig = px.line(
        distribution,
        title=f"Measurement distribution for {selected_name}",
        labels={
            "index": "Node",           
            "value": "Measurements",   
            "variable": "Cluster" 
        }
    )

    st.plotly_chart(fig)
else:
    st.warning(f"Distribution data not found for {selected_name}")


with open(f'combined/clusters/clusters_{selected_machine}', 'r') as file:
    inhoud = file.read()
st.text(inhoud)

st.header(f'Average statistics of clusters')
statistics = pd.read_csv(f'combined/Statistics/Statistics_{selected_machine}.csv')
st.dataframe(statistics)

st.header(f'Virtual machines')
vms = pd.read_csv(f'combined/vms/vms_{selected_machine}.csv')
st.dataframe(vms)



st.header(f'Energy efficientcy per cluster per hour')

for cluster_id in [0, 1, 2]:
    image_path = f'combined/efficiency/efficiency_cluster_{cluster_id}_{selected_machine}.png'
    if os.path.exists(image_path):
        st.subheader(f'Energy efficiency cluster {cluster_id}')
        energy_img = Image.open(image_path)
        st.image(energy_img, use_container_width=True)
    else:
        st.warning(f'Image not found for cluster {cluster_id} - {selected_name}')



st.subheader(f'Energy & CPU load per hour per node')
node_options = sorted(available_nodes[selected_machine])
selected_node_energy = st.selectbox("Choose node (energy/cpu):", node_options, key="energy_cpu_node_select")

energy_path = f"combined/results/plots/{selected_machine}/{selected_node}_energy_plot.png"
cpu_path = f"combined/results/plots/{selected_machine}/{selected_node}_cpu_plot.png"

col1, col2 = st.columns(2)
with col1:
    if os.path.exists(energy_path):
        st.image(Image.open(energy_path), caption=f'Energy use during the day from {selected_node}', use_container_width=True)
    else:
        st.warning(f"Image not found: {energy_path}")

with col2:
    if os.path.exists(cpu_path):
        st.image(Image.open(cpu_path), caption=f'Cpu Load during the day from {selected_node}', use_container_width=True)
    else:
        st.warning(f"Image not found: {cpu_path}")

st.header('Cluster Heatmap')

selected_cluster = st.selectbox('Choose a cluster (heatmap/table):', options=[0, 1, 2], key='heatmap_cluster_select')
heatmap_path = f'combined/efficiency/heatmap/{selected_machine}_{selected_cluster}_cluster_efficiency_summary.png'


if selected_machine == 'a6177608':
    st.markdown(
        f"**Note:** Because {selected_machine} contains many nodes, we show a _table_ instead of a _heatmap_ to avoid memory problems."
    )
    csv_path = f'combined/efficiency/table/{selected_machine}_cluster{selected_cluster}_efficiency.csv'

    if os.path.exists(csv_path):
        st.subheader(f'Table efficiency {selected_name} (Cluster {selected_cluster})')
        df_table = pd.read_csv(csv_path, index_col=0)
        
        df_table = df_table.fillna(0)
        num_cols = df_table.select_dtypes(include=['number']).columns
        format_dict = {col: "{:.1f}" for col in num_cols}
        
        st.dataframe(df_table.style.format(format_dict), use_container_width=True)
    else:
        st.warning(f'Table not found for cluster {selected_cluster} - {selected_machine}')

else:
    if os.path.exists(heatmap_path):
        st.subheader(f'Heatmap efficiency {selected_name} (Cluster {selected_cluster})')
        heat_img = Image.open(heatmap_path)
        st.image(heat_img, use_container_width=True)
    else:
        st.warning(f'Image not found for cluster {selected_cluster} - {selected_machine}')


score_path = f'combined/results/total_{selected_machine}.png'
if os.path.exists(score_path):
    st.subheader(f'Final results {selected_machine}')
    score_img = Image.open(score_path)
    st.image(score_img, use_container_width=True)
else:
    st.warning(f'Image not found for cluster {selected_machine}')