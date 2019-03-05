import general
from cry_utils import norm_path_for_ce


def set_increment_amount():
    x1, y1, z1, x2, y2, z2 = general.get_selection_aabb()
    # width of x + 1/2 width of x because it measures from center point
    increment_amount = (x2 - x1) + ((x2 - x1) * 0.5)
    general.clear_selection()
    return increment_amount


def add_cgfs(items):
    """spawn in each of the cgfs from the array passed in and then return the names of the items"""
    added_names = []
    num_cols = 25
    x = 0
    increment_amount = 0
    for idx, item in enumerate(items):
        if idx % num_cols == 0:
            # increment by some amount set by the last objects x width
            x += increment_amount
        new_object = general.new_object(
            "Brush", norm_path_for_ce(item), "", x, (idx % num_cols) * 55, 32
        )
        general.select_object(new_object)
        increment_amount = set_increment_amount()
        added_names.append(new_object)
    general.clear_selection()
    general.select_objects(added_names)
    return added_names
