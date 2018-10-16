#!/usr/bin/python

import os
from local_incremental_build import get_variant
from local_incremental_build import get_os

valueOfLineForBeginningOfTheScopeOfTheMethod = 'def get_correct_workspace_for_current_variant(os_name, variant_name):'
valueOfLineForFinishingOfTheScopeOfTheMethod = '    return correct_path_to_workspace'
build_name = os.getenv('BUILD_NAME')
currentVariant=get_variant(build_name)
currentOs = get_os(build_name)
currentOsBlockValue = 'if os_name == "%s":' % currentOs
currentVariantBlockValue = 'if variant_name == "%s"' % currentVariant
isReplaceNecessary = False
pathToCurrentScript = "local_incremental_build.py"
current_workspace_for_current_variant = ""

with open(pathToCurrentScript) as f:
    lines = f.readlines()
    startingIndexOfMethod = -1
    endingIndexOfMethod = -1
    currentIndex = -1

    for line in lines:
        currentIndex += 1

        if valueOfLineForBeginningOfTheScopeOfTheMethod in line:
            startingIndexOfMethod = currentIndex
        elif valueOfLineForFinishingOfTheScopeOfTheMethod in line:
            endingIndexOfMethod = currentIndex
            break

    if startingIndexOfMethod > -1 \
        and endingIndexOfMethod > -1 \
        and startingIndexOfMethod < endingIndexOfMethod:
        indexesOfAllLinesOfTheMethod = range(startingIndexOfMethod, endingIndexOfMethod + 1, 1)
        isInCurrentOsBlock = False
        isInCurrentVariantBlock = False
        indexOfLineWithTheCorrectWorkspace = -1

        for index in indexesOfAllLinesOfTheMethod:

            if isInCurrentOsBlock == True:
                if isInCurrentVariantBlock == True:
                    indexOfLineWithTheCorrectWorkspace = index
                    break
                else:
                    if currentVariantBlockValue in lines[index]:
                        isInCurrentVariantBlock = True
            else:
                if currentOsBlockValue in lines[index]:
                    isInCurrentOsBlock = True

        if indexOfLineWithTheCorrectWorkspace > -1:
            startingIndexOfCorrectPathValue = lines[indexOfLineWithTheCorrectWorkspace].index('"')
            subStringWithTheValue = lines[indexOfLineWithTheCorrectWorkspace][startingIndexOfCorrectPathValue:]

            current_workspace_for_current_variant = os.environ["WORKSPACE"].replace('/home/visteon/workspace/', '/workspace/JenkinsWorkspace/')
            current_workspace_for_current_variant_in_script = subStringWithTheValue.replace('"', "").strip('\n')

            if current_workspace_for_current_variant != current_workspace_for_current_variant_in_script:

                isReplaceNecessary = True
                lines[indexOfLineWithTheCorrectWorkspace] = lines[indexOfLineWithTheCorrectWorkspace].replace(subStringWithTheValue, '"%s"\n' % current_workspace_for_current_variant)
        f.close()

# If there is different workspace path. Rewrite the script with the new one.
if isReplaceNecessary == True:
    print("--Workspace is changed to : %s" % current_workspace_for_current_variant)
    pathToNewScript = "new.py"

    with open(pathToNewScript, "w+") as f:
        f.truncate()
        f.writelines(lines)
        f.close()

    os.remove(pathToCurrentScript)
    os.rename(pathToNewScript, pathToCurrentScript)