__author__ = 'ishai'

from piston.resource import Resource
from api.handlers import *

experiences_resource = Resource(ExperienceHandler)
