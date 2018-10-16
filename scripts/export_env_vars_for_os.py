#!/usr/bin/python

import os

environment_variables_keys = [
    "BUILD_NAME",
    "JOB_NAME",
    "Variant",
    "Version",
    "HAS_REALLY",
    "IS_DAILY_Integrity_BUILD",
    "IS_DAILY_Linux_BUILD",
    "IS_Nightly_Integrity_BUILD",
    "IS_Nightly_Linux_BUILD",
    "IS_DAILY_BUILD",
    "NODE_LABELS"
]

total_environment_variable_keys = len(environment_variables_keys)
counter = 0

with open("environment_vars_for_os.txt", "w") as file:
    for env_var_key in environment_variables_keys:
        counter += 1
        if os.getenv(env_var_key, None) == None:
            print("Missing necessary environment : " + env_var_key)
            continue
        if " " in os.environ[env_var_key]:
            os.environ[env_var_key] = "'" + os.environ[env_var_key] + "'"
        file.write(env_var_key + "=" + os.getenv(env_var_key) +
                       ("\n" if counter < total_environment_variable_keys else ""))