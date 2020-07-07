# ~/*
#  * Copyright 2018 Databricks, Inc.  All rights reserved.
#  *
#  * Licensed under the Apache License, Version 2.0 (the "License");
#  * you may not use this file except in compliance with the License.
#  * You may obtain a copy of the License at
#  *
#  * http://www.apache.org/licenses/LICENSE-2.0
#  *
#  * Unless required by applicable law or agreed to in writing, software
#  * distributed under the License is distributed on an "AS IS" BASIS,
#  * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  * See the License for the specific language governing permissions and
#  * limitations under the License.
#  *
#  * Modifitations - David Aronchick <david.aronchick@microsoft.com>
#  *
#  */
from octostore.entities._octostore_object import _OctostoreObject
from octostore.mlflow.protos.service_pb2 import Experiment as ProtoExperiment,\
    ExperimentTag as ProtoExperimentTag


class ExperimentTag(_OctostoreObject):
    """Tag object associated with an experiment."""
    def __init__(self, key, value):
        self._key = key
        self._value = value

    def __eq__(self, other):
        if type(other) is type(self):
            return self.__dict__ == other.__dict__
        return False

    @property
    def key(self):
        """String name of the tag."""
        return self._key

    @property
    def value(self):
        """String value of the tag."""
        return self._value

    def to_proto(self):
        param = ProtoExperimentTag()
        param.key = self.key
        param.value = self.value
        return param

    @classmethod
    def from_proto(cls, proto):
        return cls(proto.key, proto.value)
