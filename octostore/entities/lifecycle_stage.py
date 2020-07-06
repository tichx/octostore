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

from octostore.entities.view_type import ViewType
from octostore.exceptions import OctostoreException


class LifecycleStage(object):
    ACTIVE = "active"
    DELETED = "deleted"
    _VALID_STAGES = set([ACTIVE, DELETED])

    @classmethod
    def view_type_to_stages(cls, view_type=ViewType.ALL):
        stages = []
        if view_type == ViewType.ACTIVE_ONLY or view_type == ViewType.ALL:
            stages.append(cls.ACTIVE)
        if view_type == ViewType.DELETED_ONLY or view_type == ViewType.ALL:
            stages.append(cls.DELETED)
        return stages

    @classmethod
    def is_valid(cls, lifecycle_stage):
        return lifecycle_stage in cls._VALID_STAGES

    @classmethod
    def matches_view_type(cls, view_type, lifecycle_stage):
        if not cls.is_valid(lifecycle_stage):
            raise OctostoreException("Invalid lifecycle stage '%s'" % str(lifecycle_stage))

        if view_type == ViewType.ALL:
            return True
        elif view_type == ViewType.ACTIVE_ONLY:
            return lifecycle_stage == LifecycleStage.ACTIVE
        elif view_type == ViewType.DELETED_ONLY:
            return lifecycle_stage == LifecycleStage.DELETED
        else:
            raise OctostoreException("Invalid view type '%s'" % str(view_type))
