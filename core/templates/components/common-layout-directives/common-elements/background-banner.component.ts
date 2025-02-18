// Copyright 2015 The Oppia Authors. All Rights Reserved.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//      http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS-IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

/**
 * @fileoverview Component for the background banner.
 */

import {Component, OnInit} from '@angular/core';
import {UrlInterpolationService} from 'domain/utilities/url-interpolation.service';

@Component({
  selector: 'background-banner',
  templateUrl: './background-banner.component.html',
})
export class BackgroundBannerComponent implements OnInit {
  constructor(private urlInterpolationService: UrlInterpolationService) {}
  bannerImageFileUrl: string = '';
  ngOnInit(): void {
    const possibleBannerFilenames: string[] = [
      'bannerA.svg',
      'bannerB.svg',
      'bannerC.svg',
      'bannerD.svg',
    ];
    const bannerImageFilename: string =
      possibleBannerFilenames[
        Math.floor(Math.random() * possibleBannerFilenames.length)
      ];
    this.bannerImageFileUrl = this.urlInterpolationService.getStaticImageUrl(
      '/background/' + bannerImageFilename
    );
  }
}
