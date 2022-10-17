from .models import * # Ensures that all the modules have been loaded in their new locations *first*.
from . import models  # imports WrapperPackage/packageA
from .utils import * # Ensures that all the modules have been loaded in their new locations *first*.
from . import utils  # imports WrapperPackage/packageA
import sys
sys.modules['models'] = models
sys.modules['utils'] = utils