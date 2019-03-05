#!/usr/bin/env python
# title           :cry_utils module
# description     :This module contains a bunch of helper function for use in CRYENGINE sandbox python scripting
# author          :Chris Sprance / Entrada Interactive
# date            :06/30/16
# usage           : contains helper functions for python programming in CRYENGINE sandbox
# notes           :
# python_version  :2.7
# ==============================================================================
import os
import xml.etree.ElementTree as ET
from BeautifulSoup import BeautifulSoup as BS
from etree_xforms import *
import io

from cry_utils.get_files_by_type import get_all_files


def make_soup(xml_path):
    with open(xml_path, "r") as xml_file:
        soup = BS("\n".join(xml_file.readlines()))
        return soup


def get_base_item_xml_path(skin_xml_path):
    soup = make_soup(skin_xml_path)
    item = soup.find("item")
    item_name = item["name"]
    item_file = find_xml_file_by_item_name(item_name)
    return item_file[0]


def get_item_material_from_skin_xml(skin_xml_path):
    soup = make_soup(skin_xml_path)
    params = soup.find("params")
    return params.find("param", {"name": "material"})["value"]


def is_skin(xml_path):
    with open(xml_path, "r") as xml_file:
        soup = BS(xml_file.readline())
        return soup.find("skin")


def is_vehicle_skin(xml_path):
    try:
        soup = make_soup(xml_path)
        vehicle = soup.find("item")["name"]
        return vehicle in map(lambda x: str(x[0]), get_all_vehicle_names_and_paths())
    except Exception as e:
        return False


def get_base_vehicle_xml_path(xml_filepath):
    soup = make_soup(xml_filepath)
    item = soup.find("item")
    item_name = item["name"]


def get_vehicle_name_from_skin(xml_filepath):
    soup = make_soup(xml_filepath)
    return soup.find("item")["name"]


def get_skin_name(xml_filepath):
    soup = make_soup(xml_filepath)
    return soup.find("skin")["name"]


def get_prefab_objects_by_prefab_name(
    name, prefab_dir="D:/perforce/dev/GameSDK/Prefabs"
):
    """gets a prefabs xml <objects></objects>
	and all child <object></object> elements
	this is used in the layer parser when a layer contains
	a <object type='Prefab'>
	 It returns all <object> children but not the top <objects>
	 ready to be parsed with xml.etree.ElementTree"""

    # split the name into it's parts
    prefab_parts = name.split(".")

    # prefab_master.prefab_group.prefab_name
    prefab_master = prefab_parts[0]
    prefab_name = ".".join(prefab_parts[1:])

    # first build our path with the prefab_master and the prefab_dir
    xml_path = os.path.normpath(os.path.join(prefab_dir, prefab_master + ".xml"))

    # if no file exists return false
    try:
        os.path.exists(xml_path)
        # get the xml root from the file
        with open(xml_path, "r") as xml_file:
            tree = ET.parse(xml_file).getroot()
            return tree.findall("./Prefab[@Name='%s']/Objects/Object" % prefab_name)
    except Exception as e:
        # silently report this error for debugging purposes
        print(e)


def norm_path_for_ce(path, maintain_casing=True):
    """Normalize a path for use within cryengine
	This means stripping off any of the non relevant file path
	and only using what's past GameSDK
	"""
    split_path = os.path.normpath(path).split(os.path.sep)
    for idx, part in enumerate(split_path):
        if part == "GameSDK":
            return (
                "/".join(split_path[idx + 1 :])
                if maintain_casing
                else "/".join(split_path[idx + 1 :]).lower()
            )


def get_excluded_files_list():
    with open(
        os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "excluded_entities.txt"
        ),
        "r",
    ) as f:
        return f.read().splitlines()


def get_item_name_from_xml(xml):
    soup = make_soup(xml)
    # is it a skin?
    try:
        skin_name = soup.find("skin")["name"]
        return skin_name
    except Exception as e:
        pass
    # is it a vehicle
    try:
        vehicle_name = soup.find("animated")["name"]
        return vehicle_name
    except Exception as e:
        pass
    # is it an item?    
    try:
        item_name = soup.find("item")["name"]
        if item_name not in get_excluded_files_list():
            return item_name
    except Exception as e:
        pass


def get_tent_geometry(placeable):
    tent = placeable.find("param", {"name": "placed_class"})
    if tent:
        items_dir = get_items_dir()
        print(items_dir, tent)
        unpacked_xml_path = "%s/%s.xml" % (items_dir, tent)
        with io.open(unpacked_xml_path) as xml_file:
            soup = BS(xml_file.read())
            thirdperson = soup.find("thirdperson")
            return thirdperson["name"]


def get_tent_material(placeable):
    tent = placeable.find("param", {"name": "placed_class"})
    if tent:
        items_dir = get_items_dir()
        unpacked_xml_path = "%s/%s.xml" % (items_dir, tent)
        print(items_dir, tent)
        with io.open(unpacked_xml_path) as xml_file:
            soup = BS(xml_file.read())
            thirdperson = soup.find("thirdperson")
            return thirdperson["material"]


def get_item_geometry_from_xml(xml, use_onground=False):
    with io.open(xml, "r") as xml_file:
        soup = BS(xml_file.read())
        # query for some common fields
        static = soup.find("static")
        thirdperson = soup.find("thirdperson")
        onground = soup.find("onground")
        powered = soup.find("powered")
        wearable = soup.find("param", {"name": "skin"})
        placeable = soup.find("item", {"class": "Placeable"})
        # check
        # if placeable:
        #     tent_geo = get_tent_geometry(placeable)
        #     if tent_geo:
        #         return tent_geo
        if not use_onground:
            if wearable:
                return wearable["value"]
            if powered:
                return powered["filename"]
            if static:
                return static["filename"]
            if thirdperson:
                return thirdperson["name"]
            if onground:
                return onground["name"]
        if onground:
            return onground["name"]


def get_item_material_from_xml(xml):
    with io.open(xml, "r") as xml_file:
        soup = BS(xml_file.read())
        # query for some common fields
        static = soup.find("static")
        thirdperson = soup.find("thirdperson")
        onground = soup.find("onground")
        wearable = soup.find("param", {"name": "mtl"})
        placeable = soup.find("item", {"class": "Placeable"})
        # check
        # if placeable:
        #     tent_mtl = get_tent_material(placeable)
        #     if tent_mtl:
        #         return tent_mtl
        # try and except are because sometimes mtl values can be listed in different ways.
        if wearable:
            try:
                if wearable["value"] is not None:
                    return wearable["value"].replace(".mtl", "")
            except KeyError:
                pass
        if static:
            try:
                if static["mtl"] is not None:
                    return static["mtl"].replace(".mtl", "")
            except KeyError:
                pass
        if thirdperson:
            try:
                if thirdperson["material"] is not None:
                    return thirdperson["material"].replace(".mtl", "")
            except KeyError:
                pass
        if onground:
            try:
                if onground["material"] is not None:
                    return onground["material"].replace(".mtl", "")
            except KeyError:
                pass


def get_items_dir():
    return os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            "..",
            "..",
            "GameSDK",
            "Scripts",
            "Entities",
            "Items",
            "XML",
        )
    )


def get_vehicles_dir():
    return os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            "..",
            "..",
            "GameSDK",
            "Scripts",
            "Entities",
            "Vehicles",
            "Implementations",
            "Xml",
        )
    )


def get_screenshots_dir():
    return os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..", "..", "user", "screenshots")
    )


def get_all_vehicle_names_and_paths():
    vehicle_paths = get_all_vehicle_paths()
    vehicle_soups = [make_soup(xml_path) for xml_path in vehicle_paths]
    return zip(map(lambda x: x.find("vehicle")["name"], vehicle_soups), vehicle_paths)


def get_all_item_names(exclude=True):
    """
    :param exclude: Should we Exclude certain items True By Default
    :return:
    """
    excluded_items = get_excluded_files_list()
    items_dir = get_items_dir()
    items = get_all_files(".xml", items_dir)
    ret_list = []
    for xml in items:
        with io.open(os.path.normpath(xml), "r") as f:
            soup = BS(f.readline())
            item = soup.find("item")
            if item is not None:
                if exclude:
                    if item["name"] not in excluded_items:
                        ret_list.append(item["name"])
    return ret_list


def get_all_item_paths():
    items_dir = get_items_dir()
    return get_all_files(".xml", items_dir)


def get_all_vehicle_paths():
    vehicles_dir = get_vehicles_dir()
    return filter(
        lambda x: x.find("_inventory.xml") == -1, get_all_files(".xml", vehicles_dir)
    )


def find_xml_file_by_item_name(item_name):
    item_paths = get_all_item_paths()
    item_paths_and_names = [
        (xml_path, get_item_name_from_xml(xml_path)) for xml_path in item_paths
    ]
    return filter(lambda item: item[1] == item_name, item_paths_and_names)[0]
