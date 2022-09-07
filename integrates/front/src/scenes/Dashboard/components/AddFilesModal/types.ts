/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

export interface IAddFilesModalProps {
  isOpen: boolean;
  isUploading: boolean;
  onClose: () => void;
  onSubmit: (values: { description: string; file: FileList }) => void;
}
