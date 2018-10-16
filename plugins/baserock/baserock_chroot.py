#!/usr/bin/python
import baserock
from baserock import Baserock
import definitions
import os
import sys


def main():
    try:
        new_ws = sys.argv[1]
        system = sys.argv[2]
        build_id = sys.argv[3]
        delivery_type = sys.argv[4]
    except IndexError:
        print("Not enough arguments!\nProgram expects:\n1.workspace\n2.cluster\n3.ID\n4.SDK or BSP\n5.NODE NAME")
        sys.exit(2)
            
   
    repo, branch, remote = definitions.get_repo_and_branch(system)

    cluster = definitions.get_cluster(delivery_type)
    if not cluster.endswith('.morph'):
        cluster += '.morph'

    os.environ['BUILD_ID_J'] = build_id
    baserock.create_new_ws(new_ws, repo, branch)
    b = Baserock(new_ws, branch, repo, remote)
    if delivery_type == 'SDK':
        #cluster = 'base-system-armv7lhf-jcihw-test-sdk.morph'
        repository = repo.replace(':', '/')
        path = os.path.join('/src', new_ws, branch, repository, cluster)
        with open(path, 'r+b') as fd:
            lines = fd.read()
            lines = lines.replace('/src/deploy', '/src/deploy/' + build_id + '/SDK')
            fd.seek(0)
            fd.truncate()
            fd.write(''.join(lines))
    elif delivery_type == 'BSP':
        cluster = 'base-system-armv7lhf-jcihw-test-fusion-deploy.morph'

    b.build_and_deploy(cluster)

    if delivery_type == 'SDK':
        #cluster = 'base-system-armv7lhf-jcihw-test-sdk.morph'
        repository = repo.replace(':', '/')
        path = os.path.join('/src', new_ws, branch, repository, cluster)
        with open(path, 'r+b') as fd:
            lines = fd.read()
            lines = lines.replace('/src/deploy/' + build_id + '/SDK', '/src/deploy')
            fd.seek(0)
            fd.truncate()
            fd.write(''.join(lines))
            
    # Stupid hack to change the ownership of the newly created BS files in chroot
    # TODO: BS files should be part from the baserock workspace
    os.system("chmod gou+w ./BSPOS_BS1.0/plugins/baserock/*.pyc")
    print( "\n\nRunning : chmod gou+w ./BSPOS_BS1.0/plugins/baserock/*.pyc\n\n")


if __name__ == '__main__':
    main()

