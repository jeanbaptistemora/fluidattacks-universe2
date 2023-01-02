import type { ApolloError } from "@apollo/client";
import { useMutation, useQuery } from "@apollo/client";
import {
  faChevronRight,
  faCircleExclamation,
} from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { Field, Form, Formik } from "formik";
import type { GraphQLError } from "graphql";
// https://github.com/mixpanel/mixpanel-js/issues/321
// eslint-disable-next-line import/no-named-default
import { default as mixpanel } from "mixpanel-browser";
import React, { useCallback, useState } from "react";
import { useTranslation } from "react-i18next";

import { SidePanel } from "./components/SidePanel";
import { PhoneField } from "./PhoneField";
import { GET_STAKEHOLDER, SEND_SALES_EMAIL_TO_GET_SQUAD_PLAN } from "./queries";
import type {
  IAdditionFormValues,
  IGetStakeholderResult,
  ISendSalesMailToGetSquadPlan,
} from "./types";
import {
  machineLanguages,
  squadCICD,
  squadInfra,
  squadLanguages,
} from "./utils";

import { Button } from "components/Button";
import { Container } from "components/Container";
import { ExternalLink } from "components/ExternalLink";
import { Input } from "components/Input";
import { List } from "components/List";
import { Text } from "components/Text";
import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";
import { validAlphanumericSpace, validEmail } from "utils/validations";

export const LanguagesButton: React.FC = (): JSX.Element => {
  const { t } = useTranslation();
  const [machinePanel, setMachinePanel] = useState(false);
  const openMachinePanel = useCallback((): void => {
    mixpanel.track("SupportedLanguagesOnboarding");
    setMachinePanel(true);
  }, []);
  const closeMachinePanel = useCallback((): void => {
    setMachinePanel(false);
  }, []);
  const [squadPanel, setSquadPanel] = useState(false);
  const openSquadPanel = useCallback((): void => {
    setSquadPanel(true);
  }, []);
  const closeSquadPanel = useCallback((): void => {
    setSquadPanel(false);
    setMachinePanel(false);
  }, []);
  const [contactSalesPanel, setContactSalesPanel] = useState(false);
  const openContactSalesPanel = useCallback((): void => {
    setContactSalesPanel(true);
    setSquadPanel(false);
  }, []);
  const closeContactSalesPanel = useCallback((): void => {
    setContactSalesPanel(false);
    setSquadPanel(false);
    setMachinePanel(false);
  }, []);
  const [contactSalesConfirm, setContactSalesConfirm] = useState(false);
  const openContactSalesConfirm = useCallback((): void => {
    setContactSalesConfirm(true);
    closeContactSalesPanel();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);
  const closeContactSalesConfirm = useCallback((): void => {
    setContactSalesConfirm(false);
  }, []);
  const [sendSalesEmailToGetSquadPlan] =
    useMutation<ISendSalesMailToGetSquadPlan>(
      SEND_SALES_EMAIL_TO_GET_SQUAD_PLAN,
      {
        onCompleted: (result: ISendSalesMailToGetSquadPlan): void => {
          if (result.sendSalesMailToGetSquadPlan.success) {
            mixpanel.track("SendSquadFormOnboarding");
            openContactSalesConfirm();
          }
        },
        onError: (updateError: ApolloError): void => {
          updateError.graphQLErrors.forEach((error: GraphQLError): void => {
            msgError("error");
            Logger.warning("An error occurred sending the notification", error);
          });
        },
      }
    );

  const renderMachineUtil = useCallback((language: string): JSX.Element => {
    return (
      <Container align={"start"} pb={"7px"} pt={"7px"}>
        <Text bright={3} fontSize={"16px"} ta={"start"} tone={"dark"}>
          {language}
        </Text>
      </Container>
    );
  }, []);

  const handleSubmitClick = useCallback(
    async (values: IAdditionFormValues): Promise<void> => {
      await sendSalesEmailToGetSquadPlan({
        variables: {
          email: values.email,
          name: values.name,
          phone: {
            callingCountryCode: values.phone.callingCountryCode,
            nationalNumber: values.phone.nationalNumber,
          },
        },
      });
    },
    [sendSalesEmailToGetSquadPlan]
  );

  const renderSquadUtil = useCallback((language: string): JSX.Element => {
    return (
      <Container align={"start"} pb={"3px"} pt={"3px"}>
        <Text bright={3} fontSize={"16px"} ta={"start"} tone={"dark"}>
          {language}
        </Text>
      </Container>
    );
  }, []);
  const { data } = useQuery<IGetStakeholderResult>(GET_STAKEHOLDER, {
    onError: (error): void => {
      error.graphQLErrors.forEach(({ message }): void => {
        Logger.error("An error occurred loading stakeholder", message);
      });
    },
  });
  const stakeholderEmail: string = data ? data.me.userEmail : "";
  const stakeholderName: string = data ? data.me.userName : "";

  return (
    <Container
      align={"center"}
      display={"flex"}
      justify={"center"}
      minHeight={"137px"}
      pb={"38px"}
      pt={"25px"}
    >
      <Container
        align={"center"}
        bgColor={"#2e2e38"}
        borderBL={"5px"}
        borderBR={"5px"}
        borderTR={"5px"}
        borderTl={"5px"}
        display={"flex"}
        height={"100%"}
        maxHeight={"69px"}
        maxWidth={"445px"}
        width={"97.5%"}
        wrap={"wrap"}
      >
        <Container
          bgColor={"#bf0b1a"}
          height={"100%"}
          maxWidth={"12px"}
          width={"2.5%"}
        />
        <Container pl={"13px"}>
          <FontAwesomeIcon icon={faCircleExclamation} inverse={true} />
        </Container>
        <Text
          bright={2}
          disp={"inline"}
          fontSize={"15px"}
          ml={2}
          tone={"light"}
        >
          {t("autoenrollment.languages.checkLanguages")}
        </Text>
        <Container pl={"5px"}>
          <Button onClick={openMachinePanel} size={"text"} variant={"text"}>
            <Container borderBottom={"1.5px solid #dddde3"}>
              {t("autoenrollment.languages.sidepanelButton")}
            </Container>
          </Button>
          <SidePanel
            onClose={closeMachinePanel}
            open={machinePanel}
            width={"520px"}
          >
            <Container scrollInvisible={true}>
              <Container borderBottom={"2px solid #dddde3"} pb={"10px"}>
                <Text bright={3} fw={9} size={"big"} tone={"dark"}>
                  {t("autoenrollment.languages.machineLanguages.title")}
                </Text>
              </Container>
              <Container
                align={"center"}
                display={"flex"}
                pt={"32px"}
                ptMd={"12px"}
                wrap={"wrap"}
              >
                <Container pr={"8px"}>
                  <Text bright={3} fw={9} size={"big"} tone={"dark"}>
                    {t("autoenrollment.languages.machineLanguages.machinePlan")}
                  </Text>
                </Container>
                <Container
                  align={"center"}
                  border={"solid 1px #2e2e38"}
                  borderBL={"12px"}
                  borderBR={"12px"}
                  borderTR={"12px"}
                  borderTl={"12px"}
                  display={"flex"}
                  height={"26px"}
                  justify={"center"}
                  width={"75px"}
                >
                  <Text
                    bright={3}
                    fontSize={"12px"}
                    ta={"center"}
                    tone={"dark"}
                  >
                    {t("autoenrollment.languages.machineLanguages.tag")}
                  </Text>
                </Container>
                <Container
                  lineHeight={"1.5"}
                  pb={"70px"}
                  pbMd={"10px"}
                  pt={"14px"}
                  ptMd={"5px"}
                >
                  <Text bright={3} fontSize={"16px"} tone={"dark"}>
                    {t("autoenrollment.languages.machineLanguages.description")}
                  </Text>
                </Container>
                <Container
                  bgColor={"#ffffff"}
                  borderBL={"5px"}
                  borderBR={"5px"}
                  borderTR={"5px"}
                  borderTl={"5px"}
                  height={"370px"}
                  width={"470px"}
                >
                  <Container pb={"20px"} pl={"20px"} pr={"20px"} pt={"20px"}>
                    <List
                      columns={2}
                      items={machineLanguages}
                      justify={"start"}
                      render={renderMachineUtil}
                    />
                  </Container>
                </Container>
                <Container pt={"70px"} ptMd={"10px"}>
                  <Button onClick={closeMachinePanel} variant={"primary"}>
                    {t("autoenrollment.languages.machineLanguages.button")}
                  </Button>
                </Container>
                <Container pt={"10px"}>
                  <Button onClick={openSquadPanel} variant={"carousel"}>
                    <Text disp={"inline"}>
                      {t(
                        "autoenrollment.languages.machineLanguages.buttonSquadLanguages"
                      )}
                      <Text bright={3} disp={"inline"} fw={9} tone={"dark"}>
                        <ExternalLink>
                          {t(
                            "autoenrollment.languages.machineLanguages.checkSquadLanguages"
                          )}
                        </ExternalLink>
                      </Text>
                      <FontAwesomeIcon icon={faChevronRight} />
                    </Text>
                  </Button>
                </Container>
              </Container>
            </Container>
          </SidePanel>
          <SidePanel
            onClose={closeSquadPanel}
            open={squadPanel}
            width={"1040px"}
          >
            <Container display={"flex"} scrollInvisible={true} wrap={"wrap"}>
              <Container
                borderBottom={"2px solid #dddde3"}
                pb={"10px"}
                width={"100%"}
              >
                <Text bright={3} fw={9} size={"big"} tone={"dark"}>
                  {t("autoenrollment.languages.machineLanguages.title")}
                </Text>
              </Container>
              <Container width={"50%"}>
                <Container
                  align={"center"}
                  display={"flex"}
                  pt={"32px"}
                  wrap={"wrap"}
                >
                  <Container pr={"8px"}>
                    <Text bright={3} fw={9} size={"big"} tone={"dark"}>
                      {t(
                        "autoenrollment.languages.machineLanguages.machinePlan"
                      )}
                    </Text>
                  </Container>
                  <Container
                    align={"center"}
                    border={"solid 1px #2e2e38"}
                    borderBL={"12px"}
                    borderBR={"12px"}
                    borderTR={"12px"}
                    borderTl={"12px"}
                    display={"flex"}
                    height={"26px"}
                    justify={"center"}
                    width={"75px"}
                  >
                    <Text
                      bright={3}
                      fontSize={"12px"}
                      ta={"center"}
                      tone={"dark"}
                    >
                      {t("autoenrollment.languages.machineLanguages.tag")}
                    </Text>
                  </Container>
                  <Container lineHeight={"1.5"} pb={"85px"} pt={"14px"}>
                    <Text bright={3} fontSize={"16px"} tone={"dark"}>
                      {t(
                        "autoenrollment.languages.machineLanguages.description"
                      )}
                    </Text>
                  </Container>
                  <Container
                    bgColor={"#ffffff"}
                    borderBL={"5px"}
                    borderBR={"5px"}
                    borderTR={"5px"}
                    borderTl={"5px"}
                    height={"370px"}
                    scroll={"none"}
                    width={"470px"}
                  >
                    <Container pb={"20px"} pl={"20px"} pr={"20px"} pt={"20px"}>
                      <List
                        columns={2}
                        items={machineLanguages}
                        justify={"start"}
                        render={renderMachineUtil}
                      />
                    </Container>
                  </Container>
                  <Container pt={"110px"}>
                    <Button onClick={closeSquadPanel} variant={"primary"}>
                      {t("autoenrollment.languages.machineLanguages.button")}
                    </Button>
                  </Container>
                </Container>
              </Container>
              <Container width={"50%"}>
                <Container
                  align={"center"}
                  display={"flex"}
                  pt={"32px"}
                  wrap={"wrap"}
                >
                  <Container pr={"8px"}>
                    <Text bright={3} fw={9} size={"big"} tone={"dark"}>
                      {t("autoenrollment.languages.squadLanguages.squadPlan")}
                    </Text>
                  </Container>
                  <Container lineHeight={"1.5"} pb={"25px"} pt={"14px"}>
                    <Text bright={3} fontSize={"16px"} tone={"dark"}>
                      {t("autoenrollment.languages.squadLanguages.description")}
                    </Text>
                  </Container>
                  <Container lineHeight={"1.5"} pb={"12px"} pt={"0px"}>
                    <Text bright={3} fontSize={"16px"} fw={9} tone={"dark"}>
                      {t(
                        "autoenrollment.languages.squadLanguages.description2"
                      )}
                    </Text>
                  </Container>
                  <Container
                    bgColor={"#ffffff"}
                    borderBL={"5px"}
                    borderBR={"5px"}
                    borderTR={"5px"}
                    borderTl={"5px"}
                    height={"435px"}
                    width={"470px"}
                  >
                    <Container pb={"20px"} pl={"20px"} pr={"20px"} pt={"20px"}>
                      <List
                        columns={3}
                        items={squadLanguages}
                        justify={"start"}
                        render={renderSquadUtil}
                      />
                      <Container pb={"10px"} pt={"10px"}>
                        <Text bright={3} fontSize={"20px"} fw={9} tone={"dark"}>
                          {t(
                            "autoenrollment.languages.squadLanguages.squadSupportedCICD"
                          )}
                        </Text>
                      </Container>
                      <List
                        columns={2}
                        items={squadCICD}
                        justify={"start"}
                        render={renderSquadUtil}
                      />
                      <Container pb={"10px"} pt={"10px"}>
                        <Text bright={3} fontSize={"20px"} fw={9} tone={"dark"}>
                          {t(
                            "autoenrollment.languages.squadLanguages.squadSupportedInfra"
                          )}
                        </Text>
                      </Container>
                      <List
                        columns={2}
                        items={squadInfra}
                        justify={"start"}
                        render={renderSquadUtil}
                      />
                    </Container>
                  </Container>
                  <Container pt={"40px"}>
                    <Button
                      onClick={openContactSalesPanel}
                      variant={"tertiary"}
                    >
                      {t("autoenrollment.languages.squadLanguages.button")}
                    </Button>
                  </Container>
                </Container>
              </Container>
            </Container>
          </SidePanel>
          <SidePanel
            onClose={closeContactSalesPanel}
            open={contactSalesPanel}
            width={"520px"}
          >
            <Container scrollInvisible={true}>
              <Container borderBottom={"2px solid #dddde3"} pb={"10px"}>
                <Text bright={3} fw={9} size={"big"} tone={"dark"}>
                  {t("autoenrollment.languages.contactSales.title")}
                </Text>
              </Container>
              <Container lineHeight={"1.5"} pb={"25px"} pt={"20px"}>
                <Text bright={3} fontSize={"16px"} tone={"dark"}>
                  {t("autoenrollment.languages.contactSales.description")}
                </Text>
              </Container>
              <Container>
                <Formik
                  initialValues={{
                    email: stakeholderEmail,
                    name: stakeholderName,
                    phone: {
                      callingCountryCode: "57",
                      countryCode: "co",
                      nationalNumber: "",
                    },
                    toggle: false,
                  }}
                  name={"contactSalesOnboarding"}
                  onSubmit={handleSubmitClick}
                >
                  {({ isSubmitting, values }): JSX.Element => {
                    return (
                      <Form>
                        <Container pb={"7px"} pl={"7px"} pr={"7px"} pt={"7px"}>
                          <Input
                            label={
                              <Text fontSize={"16px"} fw={9}>
                                {"Full Name*"}
                              </Text>
                            }
                            name={"name"}
                            validate={validAlphanumericSpace}
                          />
                        </Container>
                        <Container pb={"7px"} pl={"7px"} pr={"7px"} pt={"16px"}>
                          <Input
                            label={
                              <Text fontSize={"16px"} fw={9}>
                                {"Email*"}
                              </Text>
                            }
                            name={"email"}
                            validate={validEmail}
                          />
                        </Container>
                        <Container pb={"7px"} pl={"7px"} pr={"7px"} pt={"16px"}>
                          <PhoneField
                            label={
                              <Text fontSize={"16px"} fw={9}>
                                {"Phone*"}
                              </Text>
                            }
                          />
                        </Container>
                        <Container
                          align={"center"}
                          display={"flex"}
                          justify={"start"}
                          pl={"12px"}
                          pt={"10px"}
                          wrap={"wrap"}
                        >
                          <Field name={"toggle"} type={"checkbox"} />
                          <Text
                            bright={9}
                            disp={"inline"}
                            fontSize={"14px"}
                            ml={2}
                            ta={"center"}
                            tone={"light"}
                          >
                            {t("autoenrollment.languages.contactSales.accept")}
                            <ExternalLink
                              href={"https://fluidattacks.com/terms-use/"}
                            >
                              {t(
                                "autoenrollment.languages.contactSales.termsOfUse"
                              )}
                            </ExternalLink>
                            {t("autoenrollment.languages.contactSales.and")}
                            <ExternalLink
                              href={"https://fluidattacks.com/privacy/"}
                            >
                              {t(
                                "autoenrollment.languages.contactSales.privacyPolicy"
                              )}
                            </ExternalLink>
                          </Text>
                        </Container>
                        <Container pl={"10px"} pt={"25px"}>
                          <Button
                            disabled={!values.toggle || isSubmitting}
                            type={"submit"}
                            variant={"primary"}
                          >
                            {"Submit Form"}
                          </Button>
                        </Container>
                      </Form>
                    );
                  }}
                </Formik>
              </Container>
            </Container>
          </SidePanel>
          <SidePanel
            onClose={closeContactSalesConfirm}
            open={contactSalesConfirm}
            width={"520px"}
          >
            <Container>
              <Container borderBottom={"2px solid #dddde3"} pb={"10px"}>
                <Text bright={3} fw={9} size={"big"} tone={"dark"}>
                  {t("autoenrollment.languages.contactSales.title")}
                </Text>
              </Container>
              <Container pt={"25px"}>
                <Text bright={3} fontSize={"24px"} fw={9} tone={"dark"}>
                  {t("autoenrollment.languages.contactSales.confirmSubtitle")}
                </Text>
              </Container>
              <Container lineHeight={"1.5"} pb={"25px"} pt={"35px"}>
                <Text
                  bright={3}
                  disp={"inline"}
                  fontSize={"16px"}
                  tone={"dark"}
                >
                  {t(
                    "autoenrollment.languages.contactSales.confirmDescription"
                  )}
                </Text>
                <Text
                  bright={3}
                  disp={"inline"}
                  fontSize={"16px"}
                  fw={9}
                  tone={"dark"}
                >
                  {t("autoenrollment.languages.squadLanguages.squadPlan")}
                </Text>
              </Container>
              <Container pt={"30px"}>
                <Button onClick={closeContactSalesConfirm} variant={"primary"}>
                  {t("autoenrollment.languages.machineLanguages.button")}
                </Button>
              </Container>
            </Container>
          </SidePanel>
        </Container>
      </Container>
    </Container>
  );
};
