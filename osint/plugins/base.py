import abc

import six


@six.add_metaclass(abc.ABCMeta)
class SourceBase(object):
    """Base class for source of information plugin.
    """

    @abc.abstractmethod
    def get_result(self):
        """Get gathered result from the source
        """
