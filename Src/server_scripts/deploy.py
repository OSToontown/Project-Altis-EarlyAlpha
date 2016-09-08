"""
ToDo List:

- Start Servers ex. deploy.py --startserver astron/uber etc. (DONE)
- Update Server ex. deploy.py --update-server (NOT DONE)
- Deploy Client Code ex. deploy.py --deployment (DONE)

"""

#Config, only change server_directory & deployment_directory if needed.
#=================
server_directory = '/root/src'
astron_directory = server_directory + '/astron'
astroncfg_directoy = astron_directory + '/config'
server_scripts_directory = server_directory + '/astron/linux'
deployment_directory = '/root/compiler'
manifest_directory = deployment_directory + '/config'
manifest_file = 'manifest-info.json'
rpc_server_directory = server_directory + '/tools'
#=================

import argparse
import os
import sys
import subprocess
import json

parser = argparse.ArgumentParser()
parser.add_argument('--start-server',
                    help='This starts the server specificed, ex. deploy.py --start astron')
parser.add_argument('--update-server',
                    help='This updates our server.')
parser.add_argument('--deploy-client',
                    help='This pushes our client code.')
parser.add_argument('--start-rpc-server',
                    help='This starts rpc server.')

args = parser.parse_args()

if args.start_server:
    os.chdir(server_scripts_directory)
    print 'Executing', args.start_server, 'server'
    subprocess.call('./start-' + args.start_server + '.sh')

if args.deploy_client:
    print 'Deploying client code'
    os.chdir(manifest_directory)
    with open(manifest_file, 'r') as i:
        json_data = json.load(i)
        json_data['server_version'] = args.deploy_client
    with open(manifest_file, 'w') as i:
        i.write(json.dumps(json_data, indent=4))
    print 'Successfully replaced', args.deploy_client, 'in', manifest_file
    os.chdir(deployment_directory)
    subprocess.call('./GameUpdate.sh', shell=True)
    print 'Successfully deployed client code version:', args.deploy_client

if args.update_server:
    os.chdir(deployment_directory)
    subprocess.call('./ServerUpdate.sh', shell=True)
    print 'Successfully updated the server version:', args.update_server

if args.start_rpc_server:
    print 'Starting RPC Invasions'
    os.chdir(rpc_server_directory)
    subprocess.call('./start-invasions.sh', shell=True)
    print 'Successfully started invasions!'


print 'Finished.'
