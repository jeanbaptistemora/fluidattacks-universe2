import styled from "styled-components";

import style from "utils/forms/index.css";

const ActionsContainer = styled.div.attrs({
  className: "flex",
})``;

const Filters = styled.div.attrs({
  className: "flex flex-wrap flex-auto mv2",
})``;

const Select = styled.select.attrs({
  className: `${style["form-control"]} black-40 border-box`,
})``;

const SelectContainer = styled.div.attrs({
  className: "flex-auto mh1",
})``;

const SearchText = styled.input.attrs({
  className: `${style["form-control"]} black-40 border-box`,
})``;

const SelectDate = styled.input.attrs({
  className: `${style["form-control"]} black-40 border-box`,
  type: `date`,
})``;

export {
  SelectDate,
  ActionsContainer,
  Filters,
  Select,
  SelectContainer,
  SearchText,
};
