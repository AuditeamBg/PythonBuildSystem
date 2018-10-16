#!/usr/bin/python
import glob
import os
import sys
from subprocess import call


DOMAIN = "BSP"
HW_PLATFORM = "MosxH2"
DELIVERY_FOLDER = "Delivery"
BIN_FOLDER = "bin"
DOC_FOLDER = "doc"

HYPERVISOR = "HypervisorFusion"
KERNEL = "KernelLinux"
ROOTFS = "RootfsLinux"


'''
    cluster_system_depend - This dict maps all the clusters to the systems they depend from
    systems - list, that stores all the systems
    x86_systems - list, that stores all systems with x86 arch
    not_x86_systems - list, that stores all other systems (arm, ppc...)
    clusters - list, that stores all the clusters
    commands - list, that stores all available commands

'''


def get_artifact(path):
    if os.path.exists(path):
        with open(path, 'r') as fd:
            artifact = fd.readline()
            return artifact
    else:
        return None


def create_new_ws(new_ws, repo, branch):
    os.chdir('/src/')
    if os.path.exists(new_ws):
        return
    call(['mkdir', '-p', new_ws])
    os.chdir(new_ws)
    call(['morph', 'init'])
    call(['morph', 'checkout', repo, branch])


def deliver_bsp(build_id, version="v1.5.1"):
    items = [ROOTFS, KERNEL, HYPERVISOR]
    for item in items:
        item_root = os.path.join(DOMAIN, item, DELIVERY_FOLDER, HW_PLATFORM, version)

        temp_clone_dir = "tmp_for_clone"
        main_dir = '/src'

        os.chdir(main_dir)
        call(["mkdir", '-p', temp_clone_dir])
        temp_clone_path_dir = os.path.join(main_dir, temp_clone_dir)
        os.chdir(temp_clone_path_dir)
        repo = "igitt@10.142.144.96:/shared/" + item_root
        item_root = os.path.join(build_id, DOMAIN + '-' + version, item, DELIVERY_FOLDER, HW_PLATFORM, version)
        print(repo)
        print('/src/deploy/' + item_root)

        #call(["git", "clone", repo])
        #os.chdir("..")
        #call(["rm", "-rf", temp_clone_dir])

        #os.chdir(item_root)
        #call(["git", "init"])
        #call(["git", "remote", "add", "origin", repo])
        #call(['git', 'commit', '-m', "'Delivery " + version + "'"])
        #call(['git', 'push', 'origin', 'master'])

    print("Ready to push")


def deliver_sdk(build_id, version):
    item = "H2SDK"

    item_root = os.path.join(DOMAIN, item, DELIVERY_FOLDER, version)

    temp_clone_dir = "tmp_for_clone"
    main_dir = '/src'

    os.chdir(main_dir)
    call(["mkdir", '-p', temp_clone_dir])
    temp_clone_path_dir = os.path.join(main_dir, temp_clone_dir)
    os.chdir(temp_clone_path_dir)
    repo = "igitt@10.142.144.96:/shared/" + item_root
    item_root = os.path.join(build_id, DOMAIN + '-' + version, item, DELIVERY_FOLDER, version)
    print(repo)
    print('/src/deploy/' + build_id + '/SDK')

    #call(["git", "clone", repo])
    #os.chdir("..")
    #call(["rm", "-rf", temp_clone_dir])

    #os.chdir(item_root)
    #call(["git", "init"])
    #call(["git", "remote", "add", "origin", repo])
    #call(['git', 'commit', '-m', "'Delivery " + version + "'"])
    #call(['git', 'push', 'origin', 'master'])

    print("Ready to push")


class Baserock:

    def __init__(self, ws='ws-fusion', branch='/a2378-trove-1/achausd/jenkins', \
                 repo='/a2378-trove-1/fusion/definitions', remote="remotes/origin/a2378-trove-1/rcar-h2-jcihw/stable"):
        self.cluster_system_depend = {}
        self.systems = []
        self.not_x86_systems = []
        self.x86_systems = []
        self.clusters = []
        self.commands = ['build', 'distbuild', 'deploy', 'build-and-deploy']
        self.ws = ws
        self.branch = '/' + branch
        self.repo = '/' + repo.replace(':', '/')
        self.remote = remote
        self.version = None
        self.categorize_morphs()

    '''
        categorize_morphs:

        This function goes through all *.morph files in the definitions directory of the given project
        and categorizes them into clusters, systems and the relevant types of systems.

        It also extract the VERSION of the current delivery from the cluster file.
    '''

    def categorize_morphs(self):
        try:
            os.chdir('/src/' + self.ws + self.branch + self.repo)
        except IOError as e:
            print "I/O error({0}): {1}".format(e.errno, e.strerror)
        call(['git', 'fetch'])
        call(['git', 'merge', self.remote])
        files = glob.glob('*.morph')
        for f in files:
            if os.path.isfile(f):
                with open(f) as fd:
                    kind_pass = False
                    type_pass = False
                    content = fd.readlines()
                    if f == 'base-system-armv7lhf-jcihw-test-fusion-deploy.morph':
                        for line in content:
                            if 'DELIVERY_VERSION:' in line:
                                self.version = line.split('"')[1]
                                if "DELIVERY_VERSION" not in os.environ:
                                    os.environ["DELIVERY_VERSION"] = self.version
                                break
                    for line in content:
                        if 'kind: system' in line:
                            self.systems.append(f)
                            kind_pass = True
                        elif 'kind: stratum' in line:
                            break
                        elif 'kind: cluster' in line:
                            self.clusters.append(f)
                            break
                        if 'arch: x86' in line and not (f in self.x86_systems):
                            self.x86_systems.append(f)
                            type_pass = True
                        elif ('arch: arm' in line or 'arch: ppc' in line) and not (f in self.not_x86_systems):
                            self.not_x86_systems.append(f)
                            type_pass = True
                        if kind_pass and type_pass:
                            break
        for c in self.clusters:
            with open(c) as fd:
                sub_flag = False
                content = fd.readlines()
                for line in content:
                    if 'subsystems' in line:
                        sub_flag = True
                    if '- morph' in line:
                        line = line.rstrip('\n')
                        if not sub_flag:
                            self.cluster_system_depend[c] = {'System': line[9:]}
                        else:
                            self.cluster_system_depend[c]['Subsystems'] = line[11:]

    def build(self, system, command):
        if system in self.clusters:
            print("ERROR: {0} is a cluster".format(system))
            sys.exit(2)
        if system in self.x86_systems and command == 'build':
            print("morph build {0}".format(system))
        elif system in self.not_x86_systems and command == 'distbuild':
            print("morph distbuild {0}".format(system))
        else:
            print("ERROR: Invalid system.")
            sys.exit(2)
        is_failed = call(['morph', command, system])
        return is_failed

    def smart_build(self, system):
        is_failed = False
        if not system.endswith('.morph'):
            system += '.morph'
        if system not in self.systems:
            print('ERROR:{0} is not a system'.format(system))
            sys.exit(0)
        if system in self.x86_systems:
            is_failed = self.build(system, 'build')
        elif system in self.not_x86_systems:
            is_failed = self.build(system, 'distbuild')
        return is_failed

    '''
        need_to_deploy:

        Before execute the deploy command, this function checks if there is need to deploy.
        First, it checks if there are no already deployed files => yes, there is need to deploy.
        Second, if the path does not exist => need to deploy.
        After that it compares the build artifact's url with the last deployed such url. If they match,
        the system we are trying to deploy is the same as the last deployed => no need to deploy.
    '''

    def need_to_deploy(self, system):
        if 'sdk' in system:
            return 1
        if 'BUILD_ID_J' in os.environ:
            return 1
        morphology = self.cluster_system_depend[system]['System']
        os.environ['JENKINS_MORPH'] = morphology
        rootfs = '/src/deploy/BSP-' + self.version + '/RootfsLinux/Delivery/MosxH2/' + self.version + '/bin/rootfs.tar.gz'
        kernel = '/src/deploy/BSP-' + self.version + '/KernelLinux/Delivery/MosxH2/' + self.version + '/bin/boot.tar.gz'
        hypervisor = '/src/deploy/BSP-' + self.version + '/HypervisorFusion/Delivery/MosxH2/' + self.version + '/bin/boot.tar.gz'
        if not os.path.exists(rootfs) or not os.path.exists(kernel) or not os.path.exists(hypervisor):
            return 1
        f = '/src/deploy/BSP-' + self.version + '/artifact'
        last_artifact = get_artifact(f)
        if not last_artifact:
            return 1
        f = '/src/build/' + morphology + '-' + self.version + '/artifact'
        artifact = get_artifact(f)
        if not artifact:
            print("System not yet built")
            sys.exit(2)
        if last_artifact == artifact:
            return 0
        return 1

    def deploy(self, system):
        if system not in self.clusters:
            print("ERROR: {0} is not a cluster".format(system))
            sys.exit(2)
        print(system)
        if self.need_to_deploy(system):
            print("morph deploy {0}".format(system))
            call(['morph', 'deploy', system])
        else:
            print("No need to deploy!")
        if len(sys.argv) == 4:
            build_id = sys.argv[3]
            os.system("cd /src/deploy/ && ln -s BSP-" + self.version + " BSP-" + build_id)

    '''
        build_and_deploy:

        To use this command, you have to pass cluster as an argument.
        It will get the needed systems and build them before deploying the cluster.
        It some of the builds fail, the deploy wont take place.
    '''

    def build_and_deploy(self, system):
        if system not in self.clusters:
            print('ERROR: {0} not a cluster'.format(system))
            sys.exit(2)
        systems_to_build = self.cluster_system_depend[system]
        for x in systems_to_build:
            is_failed = self.smart_build(systems_to_build[x])
            if is_failed:
                return
        self.deploy(system)

    def execute_command(self, command, system):
        print(self.version)
        if command == 'build' or command == 'distbuild':
            self.build(system, command)
        elif command == 'deploy':
            self.deploy(system)
        elif command == 'build-and-deploy':
            self.build_and_deploy(system)

