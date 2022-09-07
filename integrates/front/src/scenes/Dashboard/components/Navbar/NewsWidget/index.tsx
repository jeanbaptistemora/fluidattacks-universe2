/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import { faBullhorn } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import AnnounceKit from "announcekit-react";
import React, { useContext } from "react";

import { Button } from "components/Button";
import { Text } from "components/Text";
import type { IAuthContext } from "utils/auth";
import { authContext } from "utils/auth";

const NewsWidget: React.FC = (): JSX.Element => {
  const { userEmail }: IAuthContext = useContext(authContext);

  return (
    <Button size={"sm"}>
      <AnnounceKit
        user={{ email: userEmail, id: userEmail }}
        widget={"https://news.atfluid.com/widgets/v2/ZmEGk"}
        widgetStyle={{ position: "absolute", top: "25px" }}
      >
        <Text size={4}>
          <FontAwesomeIcon icon={faBullhorn} />
        </Text>
      </AnnounceKit>
    </Button>
  );
};

export { NewsWidget };
