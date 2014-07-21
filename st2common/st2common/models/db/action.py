import datetime
import mongoengine as me

from st2common import log as logging
from st2common.models.db import MongoDBAccess
from st2common.models.db.stormbase import (StormFoundationDB, StormBaseDB)

__all__ = ['ActionDB',
           'ActionExecutionDB',
           ]


LOG = logging.getLogger(__name__)


class ActionDB(StormBaseDB):
    """The system entity that represents a Stack Action/Automation in
       the system.
    Attribute:
        enabled: flag indicating whether this action is enabled in the system.
        repo_path: relative path to the action artifact. Relative to the root
                   of the repo.
        run_type: string identifying which actionrunner is used to execute the action.
        parameter_names: flat list of strings required as key names when running
                   the action.
    """

    enabled = me.BooleanField(required=True, default=True,
                          help_text='Flag indicating whether the action is enabled.')
    artifact_paths = me.ListField(
                          help_text='Paths to action content relative to repository base.')
    entry_point = me.StringField(required=True,
                          help_text='Action entrypoint.')
    runner_type = me.StringField(required=True,
                          help_text='Execution environment to use when invoking the action.')
    parameters = me.DictField(default={},
                          help_text='Action parameters with optional default values.')

    def __str__(self):
        result = []
        result.append('ActionDB@')
        result.append(str(id(self)))
        result.append('(')
        result.append('id="%s", ' % self.id)
        result.append('enabled="%s", ' % self.enabled)
        result.append('artifact_paths="%s", ' % str(self.artifact_paths))
        result.append('entry_point="%s", ' % self.entry_point)
        result.append('runner_type="%s", ' % self.runner_type)
        result.append('parameters=%s, ' % str(self.parameters))
        result.append('uri="%s")' % self.uri)
        return ''.join(result)


class ActionExecutionDB(StormFoundationDB):
    """
        The databse entity that represents a Stack Action/Automation in
        the system.

        Attributes:
            status: the most recently observed status of the execution.
                    One of "starting", "running", "completed", "error".
            result: an embedded document structure that holds the
                    output and exit status code from the action.
    """

    # TODO: Can status be an enum at the Mongo layer?
    status = me.StringField(required=True,
                help_text='The current status of the ActionExecution.')
    start_timestamp = me.DateTimeField(default=datetime.datetime.now(),
                help_text='The timestamp when the ActionExecution was created.')
    action = me.DictField(required=True,
                help_text='The action executed by this instance.')
    runner_parameters = me.DictField(default={},
                help_text='The key-value pairs passed as parameters to the action runner.')
    action_parameters = me.DictField(default={},
                help_text='The key-value pairs passed as parameters to the execution.')
    result = me.StringField(default='', help_text='Action defined result.')

    # TODO: Write generic str function for API and DB model base classes
    def __str__(self):
        result = []
        result.append('ActionExecutionDB@')
        result.append(str(id(self)))
        result.append('(')
        result.append('id=%s, ' % self.id)
        result.append('action=%s, ' % str(self.action))
        result.append('status=%s, ' % str(self.status))
        result.append('start_timestamp=%s, ' % str(self.start_timestamp))
        result.append('runner_parameters=%s, ' % str(self.runner_parameters))
        result.append('action_parameters=%s, ' % str(self.action_parameters))
        result.append('result=%s, ' % self.result)
        result.append(')')
        return ''.join(result)


# specialized access objects
action_access = MongoDBAccess(ActionDB)
actionexec_access = MongoDBAccess(ActionExecutionDB)
