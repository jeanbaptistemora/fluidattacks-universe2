/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import _ from "lodash";
import React from "react";
import { useLocation, useParams } from "react-router-dom";

import { ChartsView } from "scenes/Dashboard/containers/ChartsGenericView";

const ChartsForGroupView: React.FC = (): JSX.Element => {
  const params: { groupName: string } = useParams();
  const searchParams: URLSearchParams = new URLSearchParams(
    useLocation().search
  );

  const subjectFromSearchParams: string | null = searchParams.get("group");

  const subject: string = _.isNull(subjectFromSearchParams)
    ? params.groupName
    : subjectFromSearchParams;

  return (
    <React.StrictMode>
      <ChartsView
        bgChange={searchParams.get("bgChange") === "true"}
        entity={"group"}
        reportMode={searchParams.get("reportMode") === "true"}
        subject={subject}
      />
    </React.StrictMode>
  );
};

export { ChartsForGroupView };
