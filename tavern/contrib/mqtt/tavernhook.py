import logging
import yaml
from os.path import join, abspath, dirname

import requests

from tavern.util.dict_util import format_keys

from .request import MQTTRequest
from .response import MQTTResponse


logger = logging.getLogger(__name__)


session_type = requests.Session

request_type = MQTTRequest
request_block_name = "mqtt_publish"

def get_expected_from_request(session, stage, test_block_config):
    # mqtt response is not required
    m_expected = stage.get("mqtt_response")
    if m_expected:
        # format so we can subscribe to the right topic
        f_expected = format_keys(m_expected, test_block_config["variables"])
        mqtt_client = session
        mqtt_client.subscribe(f_expected["topic"])
        expected = f_expected
    else:
        expected = m_expected

    return expected

verifier_type = MQTTResponse
response_block_name = "mqtt_response"

schema_path = join(abspath(dirname(__file__)), "schema.yaml")
with open(schema_path, "r") as schema_file:
    schema = yaml.load(schema_file)