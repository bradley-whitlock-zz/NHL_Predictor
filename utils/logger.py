import logging
import sys

FORMAT = "%(levelname)s %(asctime)s - %(name)s: %(message)s"

logging.basicConfig( 
	format=FORMAT,
    stream=sys.stdout,
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S"
)

log = logging.getLogger('NHL_Predictor')
