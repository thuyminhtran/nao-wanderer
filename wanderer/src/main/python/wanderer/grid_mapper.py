'''
Created on 19 Apr 2013

@author: davesnowdon
'''

from naoutil.jsonobj import to_json_string
from wanderer import AbstractMapper, MEM_MAP
from grid import OccupancyGrid, Location, GRID_SIZE, CELL_SIZE
from robotstate import nao_sonar_model

class OccupancyGridMapper(AbstractMapper):
    def __init__(self, env):
        super(OccupancyGridMapper, self).__init__(env)
        self.env = env
        self.grid = OccupancyGrid(GRID_SIZE, CELL_SIZE, None)
        self.sonar_model = nao_sonar_model()
    
    # update map based on new sensor data
    def update(self, position, sensors):
        loc = Location(sensors.get_sensor('LeftSonar'),
                       sensors.get_sensor('RightSonar'),
                       position)
        if self.grid.origin is None:
            self.grid.origin = loc.get_point()
        self.grid.update_grid_cells(loc, self.sonar_model)
        self.save_map()
    
    # return the current map
    def get_map(self):
        return self.grid
    
    # store the current map in ALMemory
    def save_map(self):
        self.env.memory.insertData(MEM_MAP, to_json_string(self.grid))