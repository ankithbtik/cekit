import logging
import os
import shutil
import yaml

from concreate.errors import ConcreateError

try:
    import ConfigParser as configparser
except:
    import configparser

logger = logging.getLogger('concreate')

cfg = {}


def parse_cfg():
    cp = configparser.ConfigParser()
    cp.read(os.path.expanduser('~/.concreate'))
    return cp._sections


def cleanup(target):
    """ Prepates target/image directory to be regenerated."""
    dirs_to_clean = [os.path.join(target, 'image', 'modules'),
                     os.path.join(target, 'image', 'repos'),
                     os.path.join(target, 'repo')]
    for d in dirs_to_clean:
        if os.path.exists(d):
            logger.debug("Removing dirty directory: '%s'" % d)
            shutil.rmtree(d)


def load_descriptor(descriptor):
    """ parses descriptor and validate it against requested schema type

    Args:
      descriptor - yaml descriptor or path to a descriptor to be loaded

    Returns descriptor as a dictionary
    """
    if not os.path.exists(descriptor):
        logger.info("Descriptor path '%s' doesn't exists, trying to parse it directly."
                    % descriptor)
        try:
            return yaml.safe_load(descriptor)
        except Exception:
            raise ConcreateError('Cannot load descriptor.')

    logger.debug("Loading descriptor from path '%s'." % descriptor)

    with open(descriptor, 'r') as fh:
        return yaml.safe_load(fh)
