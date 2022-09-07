/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

export interface IGetFindingEvidences {
  finding: {
    evidence: {
      animation: {
        date: string | null;
        description: string | null;
        url: string | null;
      };
      evidence1: {
        date: string | null;
        description: string | null;
        url: string | null;
      };
      evidence2: {
        date: string | null;
        description: string | null;
        url: string | null;
      };
      evidence3: {
        date: string | null;
        description: string | null;
        url: string | null;
      };
      evidence4: {
        date: string | null;
        description: string | null;
        url: string | null;
      };
      evidence5: {
        date: string | null;
        description: string | null;
        url: string | null;
      };
      exploitation: {
        date: string | null;
        description: string | null;
        url: string | null;
      };
    };
    id: string;
  };
}
