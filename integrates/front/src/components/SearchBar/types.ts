/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

interface IAvailableParameter {
  name: string;
  title: string;
  unique: boolean;
  options: string[];
}

interface IParameter extends IAvailableParameter {
  value: string;
}

interface ISearchBarProps {
  onSubmit: (search: string) => void;
  placeholder?: string;
}

interface IFormValues {
  search: string;
}

export type { IAvailableParameter, IFormValues, IParameter, ISearchBarProps };
