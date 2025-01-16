// Copyright 2024 The Oppia Authors. All Rights Reserved.
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
 * @fileoverview Component for a URL fragment.
 */

import {Component, Input, Output, EventEmitter} from '@angular/core';
import {AppConstants} from 'app.constants';

@Component({
  selector: 'UrlFragmentEditorComponent',
  templateUrl: './url-fragment-editor.component.html',
})
export class UrlFragmentEditorComponent {
  // Here label is the heading of the input box.
  @Input() label: string;
  // Here placeholder specifies the text to display in the input box.
  @Input() placeholder: string;
  // Here maxLength specifies the maximum number of acceptable characters.
  @Input() maxLength: number;
  // Here fragmentType indicates the type of fragment, such as "story" or "topic".
  @Input() fragmentType: string;
  // Here generatedUrlPrefix is the URL prefix format, and the URL fragment is appended to generate the URL for accessing the page.
  @Input() generatedUrlPrefix: string;
  // Here fragmentIsDuplicate indicates whether the URL fragment already exists.
  @Input() fragmentIsDuplicate: boolean;
  // Here accessingPage specifies the type of page being accessed using the generated URL.
  @Input() accessingPage: string;
  // Here disabled flag indicates whether the input field is editable or not.
  @Input() disabled: boolean = false;
  @Input() urlFragment: string = '';
  @Output() urlFragmentChange: EventEmitter<string> =
    new EventEmitter<string>();
  @Output() blur: EventEmitter<void> = new EventEmitter<void>();

  validUrlFragmentRegex = new RegExp(AppConstants.VALID_URL_FRAGMENT_REGEX);

  formatUrlFragment(): void {
    this.urlFragment = this.urlFragment
      .trim()
      .toLowerCase()
      .replace(/\s+/g, '-');
  }

  onBlur(): void {
    this.blur.emit();
  }

  onChange(): void {
    if (!this.urlFragment) {
      this.urlFragment = '';
    }
    this.formatUrlFragment();
    this.urlFragmentChange.emit(this.urlFragment);
  }
}
