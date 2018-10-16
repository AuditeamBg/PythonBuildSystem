#!/usr/bin/python
import json
import os


def get_cluster_type(cluster):
    with open("BSPOS_BS1.0/plugins/conf/cluster_types.json", 'r') as fd:
        types = json.load(fd)
        return types[cluster]


def get_cluster(cluster_type):
    with open("BSPOS_BS1.0/plugins/conf/cluster_types.json", 'r') as fd:
        clusters = json.load(fd)
        return clusters[cluster_type]


def get_repo_and_branch(system):
    with open("BSPOS_BS1.0/plugins/conf/dependencies.json", 'r') as fd:
        content = json.load(fd)
        if system in content:
            repo = content[system]["repo"]
            branch = content[system]["branch"]
            remote = content[system]["remote"]
            return repo, branch, remote


def add_optionals(new_ws, branch, repo, optionals):
    opts = optionals.split(",")
    if "" in opts:
        opts.remove("")
    p = os.path.join("/src", new_ws, branch, repo, "base-system-armv7lhf-jcihw-test.morph")
    with open(p, 'a') as fd:
        for o in opts:
            fd.write("- morph: " + o + "\n")


def remove_optionals(new_ws, branch, repo, optionals):
    opts = optionals.split(",")
    if "" in opts:
        opts.remove("")
    p = os.path.join("/src", new_ws, branch, repo, "base-system-armv7lhf-jcihw-test.morph")
    with open(p, 'r') as fd:
        lines = fd.readlines()
    with open(p, 'w') as fd:
        for line in lines:
            for o in opts:
                if line != "- morph: " + o + "\n":
                    fd.write(line)
                    break