#!/usr/bin/python

import os
import sys

variant = os.getenv("Variant", None)
workspace = os.getenv("WORKSPACE", None)

buns_with_additional_user_variant_for_integrity = {
    "AR.ArWrapperProcess" : ("%s.ArHudTester" % (variant))
}
buns_with_additional_user_variant_for_linux = {
}

def check_is_bun_existing_in_current_workspace(bun, variant):

    bun_tokens = bun.split('.')
    bun_domain = bun_tokens[0].strip()
    bun_name = bun_tokens[1].strip()
    bun_domain_and_name_joined = os.path.join(bun_domain, bun_name)
    path_to_bun_in_source_space = os.path.join(workspace,
                                               "SourceSpace/" + bun_domain_and_name_joined)
    deli_space_with_variant_joined = os.path.join("DeliSpace", variant)
    path_to_bun_in_deli_space = os.path.join(workspace,
                                             deli_space_with_variant_joined + "/" + bun_domain_and_name_joined)

    is_bun_existing_in_source_space = os.path.exists(path_to_bun_in_source_space)
    is_bun_existing_in_deli_space = os.path.exists(path_to_bun_in_deli_space)
    is_bun_existing_in_current_workspace = is_bun_existing_in_source_space or is_bun_existing_in_deli_space

    return is_bun_existing_in_current_workspace


def main(argv):
    os.chdir(workspace)
    if variant != None:
        buns_with_additional_user_variant = {}

        if "Integrity" in variant:
            buns_with_additional_user_variant = buns_with_additional_user_variant_for_integrity
        elif "Lin" in variant:
            buns_with_additional_user_variant = buns_with_additional_user_variant_for_linux

        for bun in buns_with_additional_user_variant:
            current_variant = buns_with_additional_user_variant[bun]
            if check_is_bun_existing_in_current_workspace(bun, current_variant) == True:
                os.system("./Tools/Bunny/Bunny/bin/BunnyBuild %s %s" % (bun, current_variant))


if __name__ == "__main__":
    main(sys.argv)