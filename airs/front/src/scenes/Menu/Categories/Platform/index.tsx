import React, { useCallback } from "react";

import { AirsLink } from "../../../../components/AirsLink";
import { Container } from "../../../../components/Container";
import type { TDisplay } from "../../../../components/Container/types";
import { Grid } from "../../../../components/Grid";
import { Text } from "../../../../components/Typography";
import { useWindowSize } from "../../../../utils/hooks/useWindowSize";
import { translate } from "../../../../utils/translations/translate";

interface IPlatformProps {
  display: TDisplay;
}

const PlatformMenu: React.FC<IPlatformProps> = ({
  display,
}: IPlatformProps): JSX.Element => {
  const { width } = useWindowSize();
  const handleClick = useCallback((): void => {
    document.body.setAttribute("style", "overflow-y: auto;");
  }, []);

  return (
    <Container
      bgColor={"#ffffff"}
      display={display}
      scroll={"y"}
      shadowBottom={width > 1240}
    >
      <Container
        display={width > 960 ? "flex" : "inline"}
        height={"max-content"}
        justify={"center"}
        mb={3}
      >
        <Container maxWidth={width > 1200 ? "460px" : "1440px"} pb={4} ph={4}>
          <Container
            borderBottomColor={"#dddde3"}
            height={"36px"}
            mb={3}
            mt={3}
            pb={3}
          >
            <Text color={"#8f8fa3"} size={"xs"}>
              {translate.t("menu.platform.aSinglePane.title")}
            </Text>
          </Container>
          <Container>
            <AirsLink
              hoverColor={"#bf0b1a"}
              href={"/platform/"}
              onClick={handleClick}
            >
              <Text color={"#2e2e38"} mb={3} size={"small"} weight={"bold"}>
                {translate.t(
                  "menu.platform.aSinglePane.platformOverview.title"
                )}
              </Text>
            </AirsLink>
            <Text color={"#535365"} mb={3} size={"xs"}>
              {translate.t(
                "menu.platform.aSinglePane.platformOverview.subtitle"
              )}
            </Text>
            <AirsLink
              hoverColor={"#bf0b1a"}
              href={"/platform/arm/"}
              onClick={handleClick}
            >
              <Text
                color={"#2e2e38"}
                mb={3}
                mt={2}
                size={"small"}
                weight={"bold"}
              >
                {translate.t("menu.platform.aSinglePane.ARMplatform.title")}
              </Text>
            </AirsLink>
            <Text color={"#535365"} size={"xs"}>
              {translate.t("menu.platform.aSinglePane.ARMplatform.subtitle")}
            </Text>
          </Container>
        </Container>
        <Container maxWidth={width > 960 ? "833px" : "1440px"} ph={4}>
          <Container
            borderBottomColor={"#dddde3"}
            height={"36px"}
            mt={3}
            pb={3}
          >
            <Text color={"#8f8fa3"} size={"xs"}>
              {translate.t("menu.platform.products.title")}
            </Text>
          </Container>
          <Grid
            columns={width < 1201 ? 1 : 2}
            gap={width > 1200 ? "1rem" : "0rem"}
            ph={"0px"}
          >
            <Container width={"370px"} widthSm={"300px"}>
              <AirsLink
                hoverColor={"#bf0b1a"}
                href={"/product/sast/"}
                onClick={handleClick}
              >
                <Text color={"#2e2e38"} mb={3} size={"small"} weight={"bold"}>
                  {translate.t("menu.platform.products.links.sast")}
                </Text>
              </AirsLink>
              <AirsLink
                hoverColor={"#bf0b1a"}
                href={"/product/dast/"}
                onClick={handleClick}
              >
                <Text color={"#2e2e38"} mb={3} size={"small"} weight={"bold"}>
                  {translate.t("menu.platform.products.links.dast")}
                </Text>
              </AirsLink>
              <AirsLink
                hoverColor={"#bf0b1a"}
                href={"/product/sca/"}
                onClick={handleClick}
              >
                <Text color={"#2e2e38"} mb={3} size={"small"} weight={"bold"}>
                  {translate.t("menu.platform.products.links.sca")}
                </Text>
              </AirsLink>
            </Container>
            <Container>
              <AirsLink
                hoverColor={"#bf0b1a"}
                href={"/product/re/"}
                onClick={handleClick}
              >
                <Text color={"#2e2e38"} mb={3} size={"small"} weight={"bold"}>
                  {translate.t("menu.platform.products.links.re")}
                </Text>
              </AirsLink>
              <AirsLink
                hoverColor={"#bf0b1a"}
                href={"/product/ptaas/"}
                onClick={handleClick}
              >
                <Text color={"#2e2e38"} mb={3} size={"small"} weight={"bold"}>
                  {translate.t("menu.platform.products.links.ptaas")}
                </Text>
              </AirsLink>
              <AirsLink
                hoverColor={"#bf0b1a"}
                href={"/product/mast/"}
                onClick={handleClick}
              >
                <Text color={"#2e2e38"} mb={3} size={"small"} weight={"bold"}>
                  {translate.t("menu.platform.products.links.mast")}
                </Text>
              </AirsLink>
            </Container>
          </Grid>
        </Container>
      </Container>
    </Container>
  );
};

export { PlatformMenu };
