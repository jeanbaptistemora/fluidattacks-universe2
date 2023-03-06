import React from "react";
import { useTranslation } from "react-i18next";

import { RepoIcon } from "./styles";

import { Button } from "components/Button";
import { Dropdown } from "components/Dropdown";
import { Col, Row } from "components/Layout";
import { Text } from "components/Text";
import {
  azureIcon,
  bitBucketIcon,
  gitHubIcon,
  gitLabIcon,
  squarePlusIcon,
} from "resources";

interface IRepositoryProps {
  isVisible: boolean;
  onClick: () => void;
}

interface IRepositoriesDropdownProps {
  availableRepositories: {
    gitLab?: IRepositoryProps;
    gitHub?: IRepositoryProps;
    azure?: IRepositoryProps;
    bitbucket?: IRepositoryProps;
    other?: IRepositoryProps;
  };
  dropDownText: string;
}

const RepositoriesDropdown: React.FC<IRepositoriesDropdownProps> = ({
  availableRepositories,
  dropDownText,
}): JSX.Element => {
  const { t } = useTranslation();

  const { gitLab, gitHub, azure, bitbucket, other } = availableRepositories;

  const repositories = [
    {
      icon: gitLabIcon,
      id: t("components.repositoriesDropdown.gitLabButton.id"),
      isVisible: gitLab?.isVisible,
      onClick: gitLab?.onClick,
      text: t("components.repositoriesDropdown.gitLabButton.text"),
    },
    {
      icon: gitHubIcon,
      id: t("components.repositoriesDropdown.gitHubButton.id"),
      isVisible: gitHub?.isVisible,
      onClick: gitHub?.onClick,
      text: t("components.repositoriesDropdown.gitHubButton.text"),
    },
    {
      icon: azureIcon,
      id: t("components.repositoriesDropdown.azureButton.id"),
      isVisible: azure?.isVisible,
      onClick: azure?.onClick,
      text: t("components.repositoriesDropdown.azureButton.text"),
    },
    {
      icon: bitBucketIcon,
      id: t("components.repositoriesDropdown.bitbucketButton.id"),
      isVisible: bitbucket?.isVisible,
      onClick: bitbucket?.onClick,
      text: t("components.repositoriesDropdown.bitbucketButton.text"),
    },
    {
      icon: squarePlusIcon,
      id: t("components.repositoriesDropdown.otherButton.id"),
      isVisible: other?.isVisible,
      onClick: other?.onClick,
      text: t("components.repositoriesDropdown.otherButton.text"),
    },
  ];

  return (
    <Dropdown
      align={"left"}
      button={<Button variant={"primary"}>{dropDownText}</Button>}
      id={"repositories-dropdown"}
      minWidth={"420px"}
    >
      <Row align={"center"} justify={"center"}>
        {repositories.map((repo): JSX.Element | undefined => {
          const { icon, id, isVisible, onClick, text } = repo;

          if (isVisible === undefined ? false : isVisible) {
            return (
              <Col id={id} key={id}>
                <Button onClick={onClick} size={"xs"}>
                  <Row justify={"center"}>
                    <RepoIcon src={icon} />
                  </Row>
                  <Row>
                    <Text>{text}</Text>
                  </Row>
                </Button>
              </Col>
            );
          }

          return undefined;
        })}
      </Row>
    </Dropdown>
  );
};

export { RepositoriesDropdown };
