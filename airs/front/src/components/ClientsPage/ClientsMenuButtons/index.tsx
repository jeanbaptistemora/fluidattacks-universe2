/* eslint react/forbid-component-props: 0 */
import React, { useCallback, useState } from "react";

import {
  MenuItem,
  RadioButton,
  RadioLabel,
} from "../../../styles/styledComponents";

const ClientsMenuButtons: React.FC = (): JSX.Element => {
  const [filter, setFilter] = useState("all-clients");
  const filterCards = useCallback(
    ({ target }: React.ChangeEvent<HTMLInputElement>): void => {
      const targetId = (target as HTMLInputElement).id;
      setFilter(targetId);
      const cards = document.getElementsByClassName("all-clients-cards");
      const arrayCards = Array.from(cards);
      arrayCards.forEach((card): void => {
        const classes = Array.from(card.classList);
        if (classes.includes(`${targetId}-cards`)) {
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
          checked={filter === "all-clients"}
          className={"all-clients"}
          id={"all-clients"}
          name={"clientsMenu"}
          onChange={filterCards}
        />
        <RadioLabel className={"tag-all"} htmlFor={"all-clients"}>
          {"All"}
        </RadioLabel>
      </MenuItem>
      <MenuItem>
        <RadioButton
          checked={filter === "banking"}
          className={"banking"}
          id={"banking"}
          name={"clientsMenu"}
          onChange={filterCards}
        />
        <RadioLabel className={"tag-banking"} htmlFor={"banking"}>
          {"Banking/Financial Services"}
        </RadioLabel>
      </MenuItem>
      <MenuItem>
        <RadioButton
          checked={filter === "fintech"}
          className={"fintech"}
          id={"fintech"}
          name={"clientsMenu"}
          onChange={filterCards}
        />
        <RadioLabel className={"tag-fintech"} htmlFor={"fintech"}>
          {"Fintech"}
        </RadioLabel>
      </MenuItem>
      <MenuItem>
        <RadioButton
          checked={filter === "oil-energy"}
          className={"oil-energy"}
          id={"oil-energy"}
          name={"clientsMenu"}
          onChange={filterCards}
        />
        <RadioLabel className={"tag-oil-energy"} htmlFor={"oil-energy"}>
          {"Oil & Energy"}
        </RadioLabel>
      </MenuItem>
      <MenuItem>
        <RadioButton
          checked={filter === "automotive"}
          className={"automotive"}
          id={"automotive"}
          name={"clientsMenu"}
          onChange={filterCards}
        />
        <RadioLabel className={"tag-automotive"} htmlFor={"automotive"}>
          {"Automotive"}
        </RadioLabel>
      </MenuItem>
      <MenuItem>
        <RadioButton
          checked={filter === "pharmaceuticals"}
          className={"pharmaceuticals"}
          id={"pharmaceuticals"}
          name={"clientsMenu"}
          onChange={filterCards}
        />
        <RadioLabel
          className={"tag-pharmaceuticals"}
          htmlFor={"pharmaceuticals"}
        >
          {"Pharmaceuticals"}
        </RadioLabel>
      </MenuItem>
      <MenuItem>
        <RadioButton
          checked={filter === "healthcare"}
          className={"healthcare"}
          id={"healthcare"}
          name={"clientsMenu"}
          onChange={filterCards}
        />
        <RadioLabel className={"tag-healthcare"} htmlFor={"healthcare"}>
          {"Healthcare"}
        </RadioLabel>
      </MenuItem>
      <MenuItem>
        <RadioButton
          checked={filter === "airlines"}
          className={"airlines"}
          id={"airlines"}
          name={"clientsMenu"}
          onChange={filterCards}
        />
        <RadioLabel className={"tag-airlines"} htmlFor={"airlines"}>
          {"Airlines/Aviation"}
        </RadioLabel>
      </MenuItem>
      <MenuItem>
        <RadioButton
          checked={filter === "telecommunications"}
          className={"telecommunications"}
          id={"telecommunications"}
          name={"clientsMenu"}
          onChange={filterCards}
        />
        <RadioLabel
          className={"tag-telecommunications"}
          htmlFor={"telecommunications"}
        >
          {"Telecommunications"}
        </RadioLabel>
      </MenuItem>
      <MenuItem>
        <RadioButton
          checked={filter === "human-resources"}
          className={"human-resources"}
          id={"human-resources"}
          name={"clientsMenu"}
          onChange={filterCards}
        />
        <RadioLabel
          className={"tag-human-resources"}
          htmlFor={"human-resources"}
        >
          {"Human Resources"}
        </RadioLabel>
      </MenuItem>
      <MenuItem>
        <RadioButton
          checked={filter === "technology"}
          className={"technology"}
          id={"technology"}
          name={"clientsMenu"}
          onChange={filterCards}
        />
        <RadioLabel className={"tag-technology"} htmlFor={"technology"}>
          {"Technology"}
        </RadioLabel>
      </MenuItem>
    </React.Fragment>
  );
};

export { ClientsMenuButtons };
