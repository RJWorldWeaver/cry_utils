class XForm(object):
    """
    Class used to add and subtract positional information
    from an XML.etree from a CRYTEK layer file
    """

    def __init__(self, obj=None, name=None):
        super(XForm, self).__init__()
        if obj is not None:
            self.name = obj.attrib['Name']
            self.pos_x = float(obj.attrib['Pos'].split(',')[0]) if "Pos" in obj.attrib else 0.000000
            self.pos_y = float(obj.attrib['Pos'].split(',')[1]) if "Pos" in obj.attrib else 0.000000
            self.pos_z = float(obj.attrib['Pos'].split(',')[2]) if "Pos" in obj.attrib else 0.000000
            self.rot_x = float(obj.attrib['Rotate'].split(',')[1]) if "Rotate" in obj.attrib else 0.000000
            self.rot_y = float(obj.attrib['Rotate'].split(',')[2]) if "Rotate" in obj.attrib else 0.000000
            self.rot_z = float(obj.attrib['Rotate'].split(',')[3]) if "Rotate" in obj.attrib else 0.000000
            self.scale_x = float(obj.attrib['Scale'].split(',')[0]) if "Scale" in obj.attrib else 0.000000
            self.scale_y = float(obj.attrib['Scale'].split(',')[1]) if "Scale" in obj.attrib else 0.000000
            self.scale_z = float(obj.attrib['Scale'].split(',')[2]) if "Scale" in obj.attrib else 0.000000
        else:
            self.name = name
            self.pos_x = 0.000000
            self.pos_y = 0.000000
            self.pos_z = 0.000000
            self.rot_x = 0.000000
            self.rot_y = 0.000000
            self.rot_z = 0.000000
            self.scale_x = 0.000000
            self.scale_y = 0.000000
            self.scale_z = 0.000000

    def __add__(self, other):
        x = XForm(name=self.name)
        x.pos_x = self.pos_x + other.pos_x
        x.pos_y = self.pos_y + other.pos_y
        x.pos_z = self.pos_z + other.pos_z
        x.rot_x = self.rot_x + other.rot_x
        x.rot_y = self.rot_y + other.rot_y
        x.rot_z = self.rot_z + other.rot_z
        x.scale_x = self.scale_x + other.scale_x
        x.scale_y = self.scale_y + other.scale_y
        x.scale_z = self.scale_z + other.scale_z
        return x

    def __sub__(self, other):
        x = XForm(name=self.name)
        x.pos_x = self.pos_x - other.pos_x
        x.pos_y = self.pos_y - other.pos_y
        x.pos_z = self.pos_z - other.pos_z
        x.rot_x = self.rot_x - other.rot_x
        x.rot_y = self.rot_y - other.rot_y
        x.rot_z = self.rot_z - other.rot_z
        x.scale_x = self.scale_x - other.scale_x
        x.scale_y = self.scale_y - other.scale_y
        x.scale_z = self.scale_z - other.scale_z
        return x

    @property
    def pos(self):
        """ returns a list of the positions [x, y, z]"""
        return [self.pos_x, self.pos_y, self.pos_z]

    @pos.setter
    def pos(self, pos_list):
        """sets positions with a list"""
        self.pos_x, self.pos_y, self.pos_z = pos_list

    @property
    def rot(self):
        """ returns a list of the rotations [1.0, x, y, z]"""
        return [1.0, self.rot_x, self.rot_y, self.rot_z]

    @rot.setter
    def rot(self, rot_list):
        """sets rotations with a list"""
        self.rot_x, self.rot_y, self.rot_z = rot_list

    @property
    def scale(self):
        """returns a list of the scales [x,y,z]"""
        return [self.rot_x, self.rot_y, self.rot_z]

    @scale.setter
    def scale(self, scale_list):
        """sets scales with a list"""
        self.scale_x, self.scale_y, self.scale_z = scale_list

    def __str__(self):
        """the nice string version of the xform"""
        return "Xform[%s] Position: [%f, %f, %f] Rotate: [%f, %f, %f] Scale: [%f, %f, %f] " % (
            self.name, self.pos_x, self.pos_y, self.pos_z,
            self.rot_x, self.rot_y, self.rot_z,
            self.scale_x, self.scale_y,
            self.scale_z)
