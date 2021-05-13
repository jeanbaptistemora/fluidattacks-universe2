/* eslint react/forbid-component-props: 0 */
import React, { useCallback, useState } from "react";
import type { StyledComponent } from "styled-components";
import styled from "styled-components";

const MenuItem: StyledComponent<
  "li",
  Record<string, unknown>
> = styled.li.attrs({
  className: `
    ph2
    di
    `,
})``;

const RadioButton: StyledComponent<
  "input",
  Record<string, unknown>
> = styled.input.attrs({
  className: `
    op7
    dn
    transparent
    `,
  type: `radio`,
})``;

const RadioLabel: StyledComponent<
  "label",
  Record<string, unknown>
> = styled.label.attrs({
  className: `
    c-fluid-gray
    f4-ns
    f5
    roboto
    no-underline
    fw3
    hv-fluid-dkred
    pointer
    `,
})``;

const ResourcesMenuElements: React.FC = (): JSX.Element => {
  const [filter, setFilter] = useState("all");
  const filterCards = useCallback(
    ({ target }: React.ChangeEvent<HTMLInputElement>): void => {
      const targetId = (target as HTMLInputElement).id;
      setFilter(targetId);
      const cards = document.getElementsByClassName("all-card");
      const arrayCards = Array.from(cards);
      arrayCards.forEach((card): void => {
        const classes = Array.from(card.classList);
        if (classes.includes(`${targetId}-card`)) {
          card.classList.remove("dn");
          card.classList.add("dt-ns");
        } else {
          card.classList.remove("dt-ns");
          card.classList.add("dn");
        }
      });
    },
    []
  );

  return (
    <React.Fragment>
      <MenuItem>
        <RadioButton
          checked={filter === "all"}
          className={"all"}
          id={"all"}
          name={"resourcesMenu"}
          onChange={filterCards}
        />
        <RadioLabel className={"all-tag"} htmlFor={"all"}>
          {"All"}
        </RadioLabel>
      </MenuItem>
      <MenuItem>
        <RadioButton
          checked={filter === "ebook"}
          className={"ebook"}
          id={"ebook"}
          name={"resourcesMenu"}
          onChange={filterCards}
        />
        <RadioLabel className={"ebook-tag"} htmlFor={"ebook"}>
          {"eBook"}
        </RadioLabel>
      </MenuItem>
      <MenuItem>
        <RadioButton
          checked={filter === "report"}
          className={"report"}
          id={"report"}
          name={"resourcesMenu"}
          onChange={filterCards}
        />
        <RadioLabel className={"report-tag"} htmlFor={"report"}>
          {"Report"}
        </RadioLabel>
      </MenuItem>
      <MenuItem>
        <RadioButton
          checked={filter === "webinar"}
          className={"webinar"}
          id={"webinar"}
          name={"resourcesMenu"}
          onChange={filterCards}
        />
        <RadioLabel className={"webinar-tag"} htmlFor={"webinar"}>
          {"Webinar"}
        </RadioLabel>
      </MenuItem>
    </React.Fragment>
  );
};

export { ResourcesMenuElements };
