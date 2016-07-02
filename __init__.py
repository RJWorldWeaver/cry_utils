#!/usr/bin/env python
# title           :cry_utils module
# description     :This module contains a bunch of helper function for use in CRYENGINE sandbox python scripting
# author          :Chris Sprance / Entrada Interactive
# date            :06/30/16
# usage           : contains helper functions for python programming in CRYENGINE sandbox
# notes           :
# python_version  :2.7
# ==============================================================================


def get_prefab_objects_by_prefab_name(name, prefab_dir="D:/perforce/dev/GameSDK/Prefabs"):
    """gets a prefabs xml <objects></objects>
    and all child <object></object> elements
    this is used in the layer parser when a layer contains
    a <object type='Prefab'>

     It returns all <object> children but not the top <objects>
     ready to be parsed with xml.etree.ElementTree"""
    import os
    import xml.etree.ElementTree as ET
    # split the name into it's parts
    prefab_parts = name.split('.')

    # prefab_master.prefab_group.prefab_name
    prefab_master = prefab_parts[0]
    prefab_name = '.'.join(prefab_parts[1:])

    # first build our path with the prefab_master and the prefab_dir
    xml_path = os.path.normpath(os.path.join(prefab_dir, prefab_master + '.xml'))

    # if no file exists return false
    if not os.path.exists(xml_path):
        return False

    # get the xml root from the file
    with open(xml_path, 'r') as xml_file:
        tree = ET.parse(xml_file).getroot()
        return tree.findall("./Prefab[@Name='%s']/Objects/Object" % prefab_name)


def norm_path_for_ce(path, maintain_casing=True):
    """Normalize a path for use within cryengine
    This means stripping off any of the non relevant file path
    and only using what's past GameSDK
    """
    import os
    split_path = os.path.normpath(path).split(os.path.sep)
    for idx, part in enumerate(split_path):
        if part == 'GameSDK':
            return '/'.join(split_path[idx + 1:]) if maintain_casing else '/'.join(split_path[idx + 1:]).lower()


