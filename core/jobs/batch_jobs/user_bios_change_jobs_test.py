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

"""Unit tests for jobs.batch_jobs.user_bios_change_jobs."""

from __future__ import annotations

from core.jobs import job_test_utils
from core.jobs.batch_jobs import user_bios_change_jobs
from core.jobs.types import job_run_result
from core.platform import models
import re
from core.jobs import job_utils

from typing import Final, Type

MYPY = False
if MYPY:
    from mypy_imports import user_models
    from mypy_imports import datastore_services

(user_models,) = models.Registry.import_models([models.Names.USER])

datastore_services = models.Registry.import_datastore_services()


class ChangeUserNullBiosToEmptyStringJobTests(job_test_utils.JobTestBase):

    JOB_CLASS: Type[
        user_bios_change_jobs.ChangeUserNullBiosToEmptyStringJob
    ] = user_bios_change_jobs.ChangeUserNullBiosToEmptyStringJob

    USER_USERNAME_1: Final = 'user_1'
    USER_USERNAME_2: Final = 'user_2'

    def test_empty_storage(self) -> None:
        self.assert_job_output_is_empty()

    def test_user_with_null_bio(self) -> None:
        user = self.create_model(
            user_models.UserSettingsModel,
            id='user_id_1',
            username=self.USER_USERNAME_1,
            email='a@a.com',
        )
        user.update_timestamps()
        self.put_multi([user])

        self.assert_job_output_is([
            job_run_result.JobRunResult(
                stdout=f"Test Output - Username: {self.USER_USERNAME_1}, New Bio: "),
        ])

        # updated_user = datastore_services.get_multi([
        #     datastore_services.Key(
        #         user_models.UserSettingsModel,
        #         'user_id_1'
        #     )])[0].__dict__

        # user_settings = f"{updated_user}"
        # user_bio_match = re.search(r"user_bio='(.*?)'", user_settings)
        # user_bio = user_bio_match.group(1)
        # updated_user = job_utils.get_ndb_model_from_beam_entity()
        # user_bio = job_utils.get_model_property(user, 'user_bio')
        # self.assertIsInstance(user_bio, str)

    def test_user_with_valid_bio(self) -> None:
        user = self.create_model(
            user_models.UserSettingsModel,
            id='user_id_2',
            username=self.USER_USERNAME_2,
            email='b@b.com',
            user_bio='Test Bio'
        )
        user.update_timestamps()
        self.put_multi([user])

        self.assert_job_output_is_empty()
        # updated_user = datastore_services.get_multi([
        #     datastore_services.Key(
        #         user_models.UserSettingsModel,
        #         'user_id_2'
        #     )])[0]
        # user_settings = f"{updated_user}"
        # user_bio_match = re.search(r"user_bio='(.*?)'", user_settings)
        # user_bio = user_bio_match.group(1)
        # user_bio = job_utils.get_model_property(user, 'user_bio')
        # self.assertEqual(user_bio, 'Test Bio')
