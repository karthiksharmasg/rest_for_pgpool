from flask import Flask, jsonify, request, abort, make_response
import subprocess
import json

app = Flask(__name__)


@app.route('/urest/v1/pgpool/get_node_count', methods=['GET'])  ##/urest/v1/pgpool/get_node_count
def get_node_count():
    cmd = 'pcp_node_count 10 localhost 9898 pcp_user pcp_pass'
    output = subprocess.check_output(cmd, shell=True)
    return str(output).rstrip().lstrip()


def get_node_details(nodeid):
    cmd = 'pcp_node_info 10 localhost 9898 pcp_user pcp_pass ' + str(nodeid)
    try:
        output = subprocess.check_output(cmd, shell=True)
    except:
        return 'ERROR'
    return str(output)

@app.route('/urest/v1/pgpool/get_node_status', methods=['POST'])  ##/urest/v1/pgpool/get_node_status?nodeid=
def get_node_status():
    nodeid = request.args.get('nodeid')
    print nodeid

    cmd = 'pcp_node_info 10 localhost 9898 pcp_user pcp_pass '+nodeid
    try:
        output = subprocess.check_output(cmd, shell=True)
    except:
        return 'ERROR'
    return str(output).split(' ')[2]


@app.route('/urest/v1/pgpool/attach', methods=['POST'])  ##/urest/v1/pgpool/attach?nodeid=
def attach():
    nodeid = request.args.get('nodeid')
    cmd = 'pcp_attach_node 10 localhost 9898 pcp_user pcp_pass ' + nodeid
    print cmd
    try:
        ret = subprocess.call(cmd, shell=True)
        print ret
    except:
        return 'ERROR'
    return 'OK'


@app.route('/urest/v1/pgpool/detach', methods=['POST']) ##/urest/v1/pgpool/detach?nodeid=
def detach():
    nodeid = request.args.get('nodeid')
    cmd='pcp_detach_node 10 localhost 9898 pcp_user pcp_pass '+nodeid
    print cmd
    try:
        ret = subprocess.call(cmd, shell=True)
        print ret
    except:
        return 'ERROR'
    return 'OK'

@app.route('/urest/v1/pgpool/get_nodes', methods=['GET'])
def get_nodes():
    nodes = get_node_count()

    node_data= []
    node = {}
    for i in range (0,int(nodes)):
        data = get_node_details(i)
        if data != 'ERROR':
            node['nodeid'] = str(i).rstrip().lstrip()
            node['nodename'] = str(data.split(' ')[0]).rstrip().lstrip()
            node['nodeport'] = str(data.split(' ')[1]).rstrip().lstrip()
            node['nodestatus'] = str(data.split(' ')[2]).rstrip().lstrip()
            node['nodewight'] = str(data.split(' ')[3]).rstrip().lstrip()
            node_data.append(node)
            node = {}
    return json.dumps(node_data)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5050)
