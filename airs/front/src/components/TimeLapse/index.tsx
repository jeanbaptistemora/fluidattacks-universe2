import React from "react";

import { LineItem } from "./LineItem";
import { Container } from "./styledComponents";
import { TimeItem } from "./TimeItem";

interface IProps {
  confirmed: string;
  contacted: string;
  disclosure: string;
  discovered: string;
  patched: string;
  replied: string;
}

const TimeLapse: React.FC<IProps> = ({
  confirmed,
  contacted,
  disclosure,
  discovered,
  patched,
  replied,
}: IProps): JSX.Element => (
  <Container>
    <TimeItem date={discovered} text={"Vulnerability discovered."} />
    <LineItem />
    <TimeItem date={contacted} text={"Vendor contacted."} />
    {replied ? (
      <React.Fragment>
        <LineItem />
        <TimeItem
          date={replied}
          text={"Vendor replied acknowledging the report."}
        />
      </React.Fragment>
    ) : undefined}
    {confirmed ? (
      <React.Fragment>
        <LineItem />
        <TimeItem
          date={confirmed}
          text={"Vendor Confirmed the vulnerability."}
        />
      </React.Fragment>
    ) : undefined}
    {patched ? (
      <React.Fragment>
        <LineItem />
        <TimeItem date={patched} text={"Vulnerability patched."} />
      </React.Fragment>
    ) : undefined}
    {disclosure ? (
      <React.Fragment>
        <LineItem />
        <TimeItem date={disclosure} text={"Public Disclosure."} />
      </React.Fragment>
    ) : undefined}
  </Container>
);

export { TimeLapse };
