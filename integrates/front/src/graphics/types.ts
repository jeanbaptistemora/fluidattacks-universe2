/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

export interface IGraphicProps {
  bsHeight: number;
  shouldDisplayAll?: boolean;
  documentName: string;
  documentType: string;
  entity: string;
  generatorName: string;
  generatorType: string;
  className: string;
  infoLink?: string;
  reportMode: boolean;
  subject: string;
  title: string;
}
