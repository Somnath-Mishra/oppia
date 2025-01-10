# coding: utf-8
#
# Copyright 2025 The Oppia Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS-IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Change user null bios to empty string"""

from __future__ import annotations

from core.jobs import base_jobs
from core.jobs.io import ndb_io
from core.jobs.transforms import job_result_transforms
from core.jobs.types import job_run_result
from core.platform import models

import apache_beam as beam

MYPY = False
if MYPY: # pragma: no cover
    from mypy_imports import user_models

(user_models,) = models.Registry.import_models([models.Names.USER])


class ChangeUserNullBiosToEmptyStringJob(base_jobs.JobBase):
    """Change user null bios to empty string and save to Datastore."""

    def run(self) -> beam.PCollection[job_run_result.JobRunResult]:
        user_settings_query = user_models.UserSettingsModel.get_all()
        
        user_settings_models = (
            self.pipeline
            | 'Get all UserSettingsModels' >> ndb_io.GetModels(user_settings_query)
        )

        users_with_invalid_bios = (
            user_settings_models
            | 'Filter users with invalid bios' >> beam.Filter(
                lambda user: not isinstance(user.user_bio, str) or len(user.user_bio) > 2000
            )
        )

        updated_users = (
            users_with_invalid_bios
            | 'Set invalid bios to empty string' >> beam.Map(
                lambda user: (setattr(user, 'user_bio', ""), user)[1]
            )
        )

        deleted_users = (
            users_with_invalid_bios
            | 'Extract NDB keys from UserSettingsModel' >> beam.Map(lambda model: model.key)
            | 'Delete invalid users' >> ndb_io.DeleteModels()
        )


        saved_users = (
            updated_users
            | 'Save updated user models to Datastore' >> ndb_io.PutModels()
        )

        test_output = (
            updated_users
            | 'Generate test output' >> beam.Map(
                lambda user: job_run_result.JobRunResult.as_stdout(
                    f"Test Output - Username: {user.username}, New Bio: {user.user_bio}"
                )
            )
        )
        success_message = (
            saved_users
            | 'Log success message' >> beam.Map(
                lambda _: job_run_result.JobRunResult.as_stdout(
                    "Successfully updated user bios to empty string for all invalid entries."
                )
            )
        )

        return (
            (test_output,
            success_message)
            | 'Combine reported results' >> beam.Flatten()
        )
