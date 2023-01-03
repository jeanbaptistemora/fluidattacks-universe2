import {
  faBullhorn,
  faCheck,
  faMagnifyingGlass,
  faQuestion,
} from "@fortawesome/free-solid-svg-icons";
import AnnounceKit from "announcekit-react";
import { Form, Formik } from "formik";
// https://github.com/mixpanel/mixpanel-js/issues/321
// eslint-disable-next-line import/no-named-default
import { default as mixpanel } from "mixpanel-browser";
import React, { useCallback, useContext } from "react";
import type { FC } from "react";
import { useTranslation } from "react-i18next";
import { useHistory } from "react-router-dom";

import { HelpModal } from "./HelpModal";
import { UserProfile } from "./UserProfile";

import { Navbar } from "../components/Navbar";
import { Button } from "components/Button";
import { Input } from "components/Input";
import { useShow } from "components/Modal";
import { NavBar } from "components/NavBar";
import { authContext } from "utils/auth";
import type { IAuthContext } from "utils/auth";
import { Can } from "utils/authz/Can";
import { featurePreviewContext } from "utils/featurePreview";
import { alphaNumeric, composeValidators } from "utils/validations";

interface IDashboardNavBarProps {
  userRole?: string;
}

const DashboardNavBar: FC<IDashboardNavBarProps> = ({
  userRole,
}: Readonly<IDashboardNavBarProps>): JSX.Element => {
  const { userEmail }: IAuthContext = useContext(authContext);
  const { featurePreview } = useContext(featurePreviewContext);
  const { push } = useHistory();
  const [showHelp, openHelp, closeHelp] = useShow();
  const { t } = useTranslation();

  const handleClickToDo = useCallback((): void => {
    push("/todos");
  }, [push]);

  const handleSearch = useCallback(
    (values: { groupName: string }): void => {
      const groupName = values.groupName.toLowerCase();
      if (groupName.trim() !== "") {
        mixpanel.track("SearchGroup", { group: groupName });
        push(`/groups/${groupName}/vulns`);
      }
    },
    [push]
  );

  return featurePreview ? (
    <NavBar>
      <Can do={"front_can_use_groups_searchbar"}>
        <Formik
          initialValues={{ groupName: "" }}
          name={"searchBar"}
          onSubmit={handleSearch}
        >
          <Form>
            <Input
              childLeft={
                <Button icon={faMagnifyingGlass} size={"xs"} type={"submit"} />
              }
              name={"groupName"}
              placeholder={t("navbar.searchPlaceholder")}
              validate={composeValidators([alphaNumeric])}
            />
          </Form>
        </Formik>
      </Can>
      <div className={"mr2"} />
      <Button icon={faBullhorn} size={"md"}>
        <AnnounceKit
          user={{ email: userEmail, id: userEmail }}
          widget={"https://news.fluidattacks.tech/widgets/v2/ZmEGk"}
          widgetStyle={{ left: "-14px", position: "absolute", top: "20px" }}
        >
          {t("components.navBar.news")}
        </AnnounceKit>
      </Button>
      <Button icon={faCheck} onClick={handleClickToDo} size={"md"}>
        {t("components.navBar.toDo")}
      </Button>
      <Button icon={faQuestion} onClick={openHelp} size={"md"}>
        {t("components.navBar.help")}
      </Button>
      <UserProfile userRole={userRole} />
      <HelpModal onClose={closeHelp} open={showHelp} />
    </NavBar>
  ) : (
    <Navbar userRole={userRole} />
  );
};

export type { IDashboardNavBarProps };
export { DashboardNavBar };
