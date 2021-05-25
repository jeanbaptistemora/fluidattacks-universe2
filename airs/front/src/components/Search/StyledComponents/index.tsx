import type {
  FlattenInterpolation,
  StyledComponent,
  ThemeProps,
} from "styled-components";
import styled, { css } from "styled-components";

import SearchBoxMain from "../SearchBox";
import { SearchResult } from "../SearchResults";

interface IThemeProps {
  theme: {
    background?: string;
    faded?: string;
    foreground?: string;
  };
}

const StyledSearchRoot: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    fr
    mr3
    pr2
    pv4
    mv1
  `,
})``;

const open = css`
  background: #f9f9f9;
  cursor: text;
  margin-left: -1.6em;
  padding-left: 1.6em;
  width: 10em;
`;

const closed = css`
  background: transparent;
  cursor: pointer;
  margin-left: -1em;
  padding-left: 1em;
  width: 0;
`;

const StyledSearchBox = styled(SearchBoxMain)`
  align-items: center;
  display: flex;
  flex-direction: row-reverse;
  margin-bottom: 0;

  .SearchInput {
    border: ${({ hasFocus }: { hasFocus: boolean }): string =>
      hasFocus ? "auto" : "none"};
    border-color: #b0b0b0;
    border-radius: 5px;
    border-width: 1px;
    color: ${({ theme }: IThemeProps): string => theme.foreground as string};
    font-size: 1em;
    outline: none;
    padding: 0.5rem;
    transition: 100ms;

    ::placeholder {
      color: ${({ theme }: IThemeProps): string => theme.faded as string};
    }
    ${({
      hasFocus,
    }: {
      hasFocus: boolean;
    }): FlattenInterpolation<ThemeProps<string>> => (hasFocus ? open : closed)}
  }

  .SearchIcon {
    color: ${({ theme }: IThemeProps): string => theme.foreground as string};
    margin: 0.3em;
    pointer-events: none;
    width: 1em;
  }
`;

const Popover = css`
  background: #f9f9f9;
  margin-top: 0.5em;
  max-height: 80vh;
  max-width: 30em;
  overflow-y: auto;
  padding: 1em;
  position: absolute;
  right: 0;
  scrollbar-color: #b0b0b0 #f9f9f9;
  scrollbar-width: thin;
  top: auto;
  width: 80vw;
  z-index: 2;

  ::-webkit-scrollbar {
    width: 7px;
  }

  ::-webkit-scrollbar-track {
    background: #f9f9f9;
  }

  ::-webkit-scrollbar-thumb {
    background-color: #b0b0b0;
    border-radius: 15px;
  }
`;

const display = (props: { show: boolean }): string =>
  props.show ? `block` : `none`;

const StyledSearchResult = styled(SearchResult).attrs({})<{ show: boolean }>`
  display: ${display};
  ${Popover}
  .HitCount {
    display: flex;
    justify-content: flex-end;
  }

  .ais-Hits {
    ul {
      list-style: none;
      margin-left: 0;
      padding-left: 0;
    }

    li.ais-Hits-item {
      margin-bottom: 1em;

      a {
        color: #272727 !important;
        text-decoration: none !important;

        h4 {
          margin: 0;
          padding: 1rem 0.5rem;

          &:hover {
            color: #ff3435;
          }
        }
      }
    }
  }

  .ais-PoweredBy {
    display: flex;
    font-size: 80%;
    justify-content: flex-end;

    svg {
      width: 70px;
    }
  }
`;
export { StyledSearchBox, StyledSearchResult, StyledSearchRoot };
