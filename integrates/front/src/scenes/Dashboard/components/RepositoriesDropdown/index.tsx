import React from "react";

import { RepoIcon } from "./styles";

import { Button } from "components/Button";
import { Dropdown } from "components/Dropdown";
import { Col, Row } from "components/Layout";
import { Text } from "components/Text";

interface IRepositoryProps {
  icon: string;
  id?: string;
  isVisible: boolean;
  onClick: () => void;
  text: string;
}

interface IRepositoriesDropdownProps {
  availableRepositories: IRepositoryProps[];
  dropDownText: string;
}

const RepositoriesDropdown: React.FC<IRepositoriesDropdownProps> = ({
  availableRepositories,
  dropDownText,
}): JSX.Element => {
  return (
    <Dropdown
      align={"left"}
      button={<Button variant={"primary"}>{dropDownText}</Button>}
      minWidth={"420px"}
    >
      <Row align={"center"} justify={"center"}>
        {availableRepositories.map(
          (repo: IRepositoryProps): JSX.Element | undefined => {
            const { icon, id, isVisible, onClick, text } = repo;

            if (isVisible) {
              return (
                <Col
                  id={id === undefined ? text : id}
                  key={id === undefined ? text : id}
                >
                  <Button onClick={onClick} size={"xs"}>
                    <Row justify={"center"}>
                      <RepoIcon src={icon} />
                    </Row>
                    <Row>
                      <Text mt={1}>{text}</Text>
                    </Row>
                  </Button>
                </Col>
              );
            }

            return undefined;
          }
        )}
      </Row>
    </Dropdown>
  );
};

export { RepositoriesDropdown };
