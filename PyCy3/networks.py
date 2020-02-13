# -*- coding: utf-8 -*-

# ==============================================================================
# Functions for NETWORK management and retrieving information on networks, nodes
# and edges. Includes all functions that result in the creation of a new network
# in Cytoscape, in addition to funcitons that extract network models into
# other useful objects.
#
# I. General network functions
# II. General node functions
# III. General edge functions
# IV. Network creation
# V. Network extraction
# VI. Internal functions
#
# Note: Go to network_selection.py for all selection-related functions
#
# ==============================================================================
# I. General network functions
# ------------------------------------------------------------------------------

import sys
import re
import os
import warnings
import pandas as pd
import igraph as ig

from . import commands
from . import tables
from . import network_selection
from . import layouts
from .pycy3_utils import DEFAULT_BASE_URL, node_name_to_node_suid, node_suid_to_node_name, edge_name_to_edge_suid
from .exceptions import CyError
from .decorators import debug

def __init__(self):
    pass

def set_current_network(network=None, base_url=DEFAULT_BASE_URL):
    """Selects the given network as "current".

    Args:
        network (SUID, str, None): Network name or suid of the network that you want set as current
        base_url (str): Ignore unless you need to specify a custom domain,
            port or version to connect to the CyREST API. Default is http://localhost:1234
            and the latest version of the CyREST API supported by this version of PyCy3.

    Returns:
        (dict) containing server JSON response

    Raises:
        ValueError: if server response has no JSON
        requests.exceptions.RequestException: if can't connect to Cytoscape or Cytoscape returns an error

    Examples:
        >> set_current_network() # sets current network to current
        []

        >> set_current_network('MyNetwork') # sets network named 'MyNetwork' as current
        []

        >>set_current_network(1502) # sets network having SUID 1502 as current
        []

        returns {"data': {}, "errors": []}
    """
    suid = get_network_suid(network)
    cmd = 'network set current network=SUID:"' + str(suid) + '"'
    return commands.commands_post(cmd, base_url=base_url)

def rename_network(title, network=None, base_url=DEFAULT_BASE_URL):
    """Sets a new name for this network.

    Duplicate network names are not allowed

    Args:
        title (str): New name for the network
        network (SUID, str, None): name or suid of the network that you want to rename; default is "current" network
        base_url (str): Ignore unless you need to specify a custom domain,
            port or version to connect to the CyREST API. Default is http://localhost:1234
            and the latest version of the CyREST API supported by this version of PyCy3.

    Returns:
        (dict) containing server JSON response

    Raises:
        ValueError: if server response has no JSON
        requests.exceptions.RequestException: if can't connect to Cytoscape or Cytoscape returns an error

    Examples:
        rename_network('renamed network') - changes "current" network's name to "renamed network"
        rename_network('renamed network', 'MyNetwork') - changes network named 'MyNetwork' to be named "renamed network"
        rename_network('renamed network', 1502) - sets network having SUID 1502 to be named "renamed network"
        returns {"data': {}, "errors": []}
    """
    old_suid = get_network_suid(network, base_url=base_url)
    cmd = 'network rename name="' + title + '" sourceNetwork=SUID:"' + str(old_suid) + '"'
    return commands.commands_post(cmd, base_url)

def get_network_count(base_url=DEFAULT_BASE_URL):
    """Generators have a ``Yields`` section instead of a ``Returns`` section.

    Args:
        n (int): The upper limit of the range to generate, from 0 to `n` - 1.

    Yields:
        int: The next number in the range of 0 to `n` - 1.

    Examples:
        Examples should be written in doctest format, and should illustrate how
        to use the function.

        >>> print([i for i in example_generator(4)])
        [0, 1, 2, 3]

    """
    res = commands.cyrest_get('networks/count', base_url=base_url)
    return list(res.values())[0]

def get_network_name(suid=None, base_url=DEFAULT_BASE_URL):
    if isinstance(suid, str):
        # title provided
        if suid == 'current':
            network_suid = get_network_suid(base_url=DEFAULT_BASE_URL)
        else:
            net_names = get_network_list(base_url=base_url)
            if suid in net_names:
                return suid
            else:
                raise CyError('Network does not exist: ' + suid)
    elif isinstance(suid, int):
        # suid provided
        network_suid = suid
    else:
        network_suid = get_network_suid(base_url=DEFAULT_BASE_URL)

    res = commands.cyrest_get('networks.names', {'column': 'suid', 'query': network_suid}, base_url=DEFAULT_BASE_URL)
    return res[0]['name']

def get_network_suid(title=None, base_url=DEFAULT_BASE_URL):
    if isinstance(title, str):
        # Title was provided
        if title == 'current':
            network_title = title
        else:
            net_names = get_network_list(base_url=base_url)
            if title in net_names:
                network_title = title
            else:
                raise CyError('Network does not exist: ' + title)
    elif isinstance(title, int):
        # SUID was provided
        net_suids = commands.cyrest_get('networks', base_url=base_url)
        if title in net_suids:
            return title
        raise CyError('Network does not exist: ' + str(title))
    else:
        # Don't understand, so use current network
        network_title = 'current'

    # Make requested network current and return its SUID
    cmd = 'network get attribute network="' + network_title + '" namespace="default" columnList="SUID"'
    response = commands.commands_post(cmd, base_url=base_url)
    return int(response[0]['SUID'])

def get_network_list(base_url=DEFAULT_BASE_URL):
    cy_network_names = []
    if get_network_count(base_url=base_url):
        cy_networks_suids = commands.cyrest_get('networks', base_url=base_url)
        for suid in cy_networks_suids:
            res = commands.cyrest_get('networks/' + str(suid), base_url=base_url)
            cy_network_names.append(res['data']['name'])

    return cy_network_names

def export_network(filename=None, type='SIF', network=None, base_url=DEFAULT_BASE_URL):
    cmd = 'network export'  # a good start

    # filename must be suppled
    if filename is None: filename = get_network_name(network)

    # optional args
    if network is not None: cmd += ' network="SUID:' + str(get_network_suid(network, base_url=base_url)) + '"'

    type = type.upper()
    if type == 'CYS':
        sys.stderr.write('Saving session as a CYS file...')
        raise CyError("Implement this") # TODO: saveSession(filename=filename, base.url = base.url)
    else:
        # e.g., CX, CYJS, GraphML, NNF, SIF, XGMML
        if type == 'GRAPHML': type = 'GraphML'
    cmd += ' options="' + type + '"'

    ext = '.' + type.lower()
    if re.search(ext + '$', filename) is None: filename += ext
    filename = os.path.abspath(filename)
    if os.path.exists(filename): warnings.warn('This file already exists. A Cytoscape popup will be generated to confirm overwrite.')

    return commands.commands_post(cmd + ' OutputFile="' + filename + '"', base_url=base_url)

def delete_network(network=None, base_url=DEFAULT_BASE_URL):
    suid = get_network_suid(network)
    res = commands.cyrest_delete('networks/' + str(suid), base_url=base_url, require_json=False)
    return res

def delete_all_networks(base_url=DEFAULT_BASE_URL):
    res = commands.cyrest_delete('networks', base_url=base_url, require_json=False)
    return res

# ==============================================================================
# II. General node functions
# ------------------------------------------------------------------------------

def get_first_neighbors(node_names=None, as_nested_list=False, network=None, base_url=DEFAULT_BASE_URL):
    #TODO: This looks very inefficient because for each node, the entire node table is fetched from Cytoscape and the neighbor list is de-dupped ... verify this and maybe do better
    if node_names is None:
        node_names = network_selection.get_selected_nodes(network=network, base_url=base_url)
        if node_names is None: raise CyError('No nodes selected')

    if (len(node_names) == 0): return None

    net_suid = get_network_suid(network, base_url=base_url)
    neighbor_names = []

    for node_name in node_names:
        # get first neighbors for each node
        node_suid = node_name_to_node_suid([node_name], net_suid, base_url=base_url)[0]
        # TODO: Verify that this won't break if node_name_to_node_suid returns a list instead of a scalar

        first_neighbors_suids = commands.cyrest_get('networks/' + str(net_suid) + '/nodes/' + str(node_suid) + '/neighbors', base_url=base_url)
        first_neighbors_names = node_suid_to_node_name(first_neighbors_suids, net_suid, base_url=base_url)

        if as_nested_list:
            neighbor_names.append([node_name, first_neighbors_names])
        else:
            neighbor_names += first_neighbors_names
            neighbor_names = list(dict.fromkeys(neighbor_names)) # dedup list

    return neighbor_names


def add_cy_nodes(node_names, skip_duplicate_names=True, network=None, base_url=DEFAULT_BASE_URL):
    net_suid = get_network_suid(network, base_url=base_url)
    if skip_duplicate_names:
        all_nodes_list = get_all_nodes(net_suid, base_url=base_url)
        node_names = list(set(node_names) - set(all_nodes_list))

    res = commands.cyrest_post('networks/' + str(net_suid) + '/nodes', body=node_names, base_url=base_url)
    return res

def get_node_count(network=None, base_url=DEFAULT_BASE_URL):
    net_suid = get_network_suid(network, base_url=base_url)
    res = commands.cyrest_get('networks/' + str(net_suid) + '/nodes/count', base_url=base_url)
    return res['count']

def get_all_nodes(network=None, base_url=DEFAULT_BASE_URL):
    net_suid = get_network_suid(network, base_url=base_url)
    n_count = get_node_count(net_suid, base_url=base_url)
    if n_count == 0: return None

    res = commands.cyrest_get('networks/' + str(net_suid) + '/tables/defaultnode/columns/name', base_url=base_url)
    return res['values']

# ==============================================================================
# III. General edge functions
# ------------------------------------------------------------------------------

def add_cy_edges(source_target_list, edge_type='interacts with', directed=False, network=None, base_url=DEFAULT_BASE_URL):
    net_suid = get_network_suid(network, base_url=base_url)

    # Create list of all nodes in order presented
    if len(source_target_list) == 2 and isinstance(source_target_list, list) and isinstance(source_target_list[0], str) and isinstance(source_target_list[1], str):
        flat_source_target_list = source_target_list
    else:
        flat_source_target_list = [item    for sublist in source_target_list    for item in sublist]
    edge_suid_list = node_name_to_node_suid(flat_source_target_list, net_suid, base_url=base_url)

    # Verify that
    if True in [True if isinstance(x, list) else False    for x in edge_suid_list]:
        sys.stderr.write('add_cy_edges: more than one node found for a given source or target - no edges added')
        return None
        # TODO: Create consistent policy for logging to console and returning error values

    # Note: use str() for edge SUIDs in case the SUIDs exceed JSON's int encoding
    edge_data = [{'source':str(edge_suid_list[x]), 'target':str(edge_suid_list[x+1]), 'directed':directed, 'interaction':edge_type}    for x in range(0, len(edge_suid_list) - 1, 2)]

    res = commands.cyrest_post('networks/' + str(net_suid) + '/edges', body=edge_data, base_url=base_url)
    return res

def get_edge_count(network=None, base_url=DEFAULT_BASE_URL):
    net_suid = get_network_suid(network, base_url=base_url)
    res = commands.cyrest_get('networks/' + str(net_suid) + '/edges/count', base_url=base_url)
    return res['count']

def get_edge_info(edges, network=None, base_url=DEFAULT_BASE_URL):
    net_suid = get_network_suid(network, base_url=base_url)
    if isinstance(edges, str): edges = [edges]

    def convert_edge_name_to_edge_info(edge_name):
        edge_suid = edge_name_to_edge_suid(edge_name, network, base_url=base_url)
        res = commands.cyrest_get('networks/' + str(net_suid) + '/edges/' + str(edge_suid[0]), base_url=base_url)
        return res['data']

    edge_info = [convert_edge_name_to_edge_info(x)   for x in edges]
    # TODO: Verify that it's always OK to return a list instead of a single dict ... this happens in many places
    return edge_info

def get_all_edges(network=None, base_url=DEFAULT_BASE_URL):
    net_suid = get_network_suid(network, base_url=base_url)
    e_count = get_edge_count(network, base_url=base_url)
    if e_count == 0: return None

    res = commands.cyrest_get('networks/' + str(net_suid) + '/tables/defaultedge/columns/name', base_url=base_url)
    return res['values']

# ==============================================================================
# IV. Network creation
# ------------------------------------------------------------------------------

def clone_network(network=None, base_url=DEFAULT_BASE_URL):
    net_suid = get_network_suid(network, base_url=base_url)
    res = commands.commands_post('network clone network=SUID:"' + str(net_suid) + '"')
    return res['network']

def create_subnetwork(nodes=None, nodes_by_col='SUID', edges=None, edges_by_col='SUID', exclude_edges=False, subnetwork_name=None, network=None, base_url=DEFAULT_BASE_URL):
    # TODO: Verify that node and edge names can't contain blanks or commas
    title = get_network_suid(network, base_url=base_url)
    exclude_edges = 'true' if exclude_edges else 'false'
    if isinstance(nodes, str) and nodes in ['all', 'selected', 'unselected']: nodes_by_col = None
    if isinstance(edges, str) and edges in ['all', 'selected', 'unselected']: edges_by_col = None
    json_sub = {'source': 'SUID:' + str(title), 'excludeEdges': exclude_edges, 'nodeList': commands.prep_post_query_lists(nodes, nodes_by_col), 'edgeList': commands.prep_post_query_lists(edges, edges_by_col)}
    if not subnetwork_name is None: json_sub['networkName'] = subnetwork_name

    res = commands.cyrest_post('commands/network/create', body=json_sub, base_url=base_url)
    return res['data']['network']

def create_network_from_igraph(igraph, title='From igraph', collection='My Igraph Network Collection', base_url=DEFAULT_BASE_URL):
    raise CyError('Not implemented') # TODO: implement create_network_from_igraph

def create_network_from_graph(graph, title='From graph', collection='My GraphNEL Network Collection', base_url=DEFAULT_BASE_URL):
    raise CyError('Not implemented') # TODO: implement create_network_from_graph

def create_network_from_data_frames(nodes=None, edges=None, title='From dataframe', collection='My Dataframe Network Collection', base_url=DEFAULT_BASE_URL, *, node_id_list='id', source_id_list='source', target_id_list='target', interaction_type_list='interaction'):
    # it looks like nodes is a dataframe like this (from R):
    # #' nodes <- data.frame(id=c("node 0","node 1","node 2","node 3"),
    # #'            group=c("A","A","B","B"), # categorical strings
    # #'            score=as.integer(c(20,10,15,5))) # integers
    # if nodes is empty, we get a list of nodes out of the source/target values for edges

    # it looks like edges is a dataframe like this (from R):
    # ' edges <- data.frame(source=c("node 0","node 0","node 0","node 2"),
    # '            target=c("node 1","node 2","node 3","node 3"),
    # '            interaction=c("inhibits","interacts",
    # '                          "activates","interacts"),  # optional
    # '            weight=c(5.1,3.0,5.2,9.9)) # numeric
    def compute_edge_name(source, target, interaction):
        return source + ' (' + interaction + ') ' + target

    # Create a node list even if we have to use the edges lists to infer nodes
    if nodes is None:
        if not edges is None:
            id_list = []
            for source, target in zip(edges['source'].values, edges['target'].values):
                id_list.append(source)
                id_list.append(target)
            nodes = pd.DataFrame(data=id_list, columns=['id'])
        else:
            return 'Create Network Failed: Must provide either nodes or edges'

    # create the JSON for a node list ... in cytoscape.js format
    json_nodes = [{'data': {'id': node}}    for node in nodes[node_id_list]]

    # create the JSON for an edge list ... in cytoscape.js format
    json_edges = []
    if not edges is None:
        if not interaction_type_list in edges.columns: edges[interaction_type_list] = 'interacts with'
        edges_sub = edges[[source_id_list, target_id_list, interaction_type_list]]
        json_edges = [{'data': {'name': compute_edge_name(source, target, interaction), 'source': source, 'target': target, 'interaction': interaction}}   for source, target, interaction in zip(edges_sub[source_id_list], edges_sub[target_id_list], edges_sub[interaction_type_list])]

    # create the full JSON for a cytoscape.js-style network ... see http://manual.cytoscape.org/en/stable/Supported_Network_File_Formats.html#cytoscape-js-json
    # Note that no node or edge attributes are included in this version of the network
    json_network = {'data': [{'name': title}], 'elements': {'nodes': json_nodes, 'edges': json_edges}}

    # call Cytoscape to create this network and return the SUID
    network_suid = commands.cyrest_post('networks', parameters={'title': title, 'collection': collection}, body=json_network, base_url=base_url)

    # drop the SUID column if one is present
    nodes = nodes.drop(['SUID'], axis=1, errors='ignore')

    # load node attributes into Cytoscape network
    if not set(nodes.columns) - set('id') is None:
        tables.load_table_data(nodes, data_key_column=node_id_list, table_key_column=node_id_list, network=network_suid, base_url=base_url)

    if not edges is None:
        # get rid of SUID column if one is present
        edges = edges.drop(['SUID'], axis=1, errors='ignore')
        # create edge name out of source/interaction/target
        edge_names = [compute_edge_name(source, target, interaction) for source, interaction, target in zip(edges[source_id_list], edges[interaction_type_list], edges[target_id_list])]
        edges['name'] = edge_names
        # find out the SUID of each node so it can be used in a multigraph if needed
        edges['data.key.column'] = edge_name_to_edge_suid(edge_names, network_suid, base_url=base_url)

        # if the edge list looks real, add the edge attributes (if any)
        if not set(edges.columns) - set(['source', 'target', 'interaction', 'name', 'data.key.column']) is None:
            tables.load_table_data(edges, data_key_column='data.key.column', table='edge', table_key_column='SUID', network=network_suid, base_url=base_url)

    print('Applying default style...')
    commands.commands_post('vizmap apply styles="default"', base_url=base_url)

    print('Applying preferred layout')
    layouts.layoutNetwork(network=network_suid)

    return network_suid


def import_network_from_file(file=None, base_url=DEFAULT_BASE_URL):
    if file is None:
        file = 'extdata/galfiltered.sif'
    else:
        file = os.path.abspath(file)
    res = commands.commands_post('network load file file=' + file, base_url=base_url)
    return res

# ==============================================================================
# V. Network extraction
# ------------------------------------------------------------------------------

def create_igraph_from_network(network=None, base_url=DEFAULT_BASE_URL):
    suid = get_network_suid(network, base_url=base_url)

    # get dataframes
    cyedges = tables.get_table_columns('edge', network=suid, base_url=base_url)
    cynodes = tables.get_table_columns('node', network=suid, base_url=base_url)

    # check for source and target columns ... if they're not present, dig them out of the full name
    if not ['source', 'target'] in list(cyedges.columns):
        src_trg = [re.split("\ \\(.*\\)\ ", x) for x in cyedges['name']]
        cyedges['source'] = [x[0] for x in src_trg]
        cyedges['target'] = [x[1] for x in src_trg]

    # set up iGraph vertices ... first create vertex by naming it, then pile on attributes
    # Tutorial: https://igraph.org/python/doc/tutorial/tutorial.html
    # Source: https://github.com/igraph/python-igraph/blob/master/src/igraph/__init__.py
    g = ig.Graph(directed=True)

    # add all nodes and their attributes
    g.add_vertices(list(cynodes['name']))
    for col in cynodes.columns:
        if not col in ['name', 'SUID']: g.vs[col] = list(cynodes[col])

    # add all edges and their nodes
    g.add_edges([(src, trg) for src, trg in zip(cyedges['source'], cyedges['target'])])
    cyedges.rename({'source': 'from', 'target': 'to'})
    for col in cyedges.columns:
        if not col in ['SUID']: g.es[col] = list(cyedges[col])

    return g


def create_graph_from_network(network=None, base_url=DEFAULT_BASE_URL):
    raise CyError('Not implemented') # TODO: implement create_graph_from_network

# ==============================================================================
# VI. Internal functions
#
# Dev Notes: Prefix internal functions with a '_'. Skip doc_strings for these
# functions.
# ------------------------------------------------------------------------------

def first_func():
    """ This is my first function """
    print("Executing first_func()")

    res = commands.cyrest_get()
    print(res)

    return res