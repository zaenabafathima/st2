# Copyright 2019 Extreme Networks, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import

from oslo_config import cfg

from st2common import config as common_config
from st2common.constants.system import VERSION_STRING
from st2common.constants.system import DEFAULT_CONFIG_FILE_PATH

common_config.register_opts()

CONF = cfg.CONF


def parse_args(args=None):
    cfg.CONF(args=args, version=VERSION_STRING,
             default_config_files=[DEFAULT_CONFIG_FILE_PATH])


def register_opts():
    _register_common_opts()
    _register_results_tracker_opts()


def get_logging_config_path():
    return cfg.CONF.resultstracker.logging


def _register_common_opts():
    common_config.register_opts()


def _register_results_tracker_opts():
    resultstracker_opts = [
        cfg.StrOpt(
            'logging', default='/etc/st2/logging.resultstracker.conf',
            help='Location of the logging configuration file.')
    ]

    CONF.register_opts(resultstracker_opts, group='resultstracker')


register_opts()
