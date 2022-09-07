/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import React from "react";
import { Hits, Index } from "react-instantsearch-dom";

import { HitCount } from "./HitCount";
import { PageHit } from "./PageHit";

interface IProps {
  index: { name: string };
}

export const HitsInIndex = ({ index }: IProps): JSX.Element => (
  <Index indexName={index.name}>
    <HitCount />
    <Hits hitComponent={PageHit} />
  </Index>
);
