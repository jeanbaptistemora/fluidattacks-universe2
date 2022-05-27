/* eslint-disable fp/no-mutation, import/no-default-export, react/jsx-props-no-spreading, react/no-multi-comp */
import type { Meta, Story } from "@storybook/react";
import React from "react";
import { MemoryRouter, Route, Switch } from "react-router-dom";

import { linkFormatter } from "./formatters";
import type { ITableProps } from "./types";

import { Table } from ".";

const config: Meta = {
  component: Table,
  title: "components/Table",
};

const Template: Story<ITableProps> = (props): JSX.Element => {
  return <Table {...props} />;
};

const Default = Template.bind({});
Default.args = {
  dataset: [
    { artist: "placebo", song: "a million little pieces", year: "2010" },
    { artist: "nirvana", song: "heart shaped box", year: "1992" },
    { artist: "ghost", song: "zenith", year: "2015" },
    { artist: "def leppard", song: "hysteria", year: "1987" },
  ],
  exportCsv: false,
  headers: [
    { dataField: "artist", header: "Artist name" },
    { dataField: "song", header: "Song name" },
    { dataField: "year", header: "Year of release" },
  ],
  id: "songsTable",
  pageSize: 10,
  search: false,
};

const TemplateWithRouter: Story<ITableProps> = (props): JSX.Element => {
  return (
    <MemoryRouter initialEntries={["/"]}>
      <Table {...props} />
      <Switch>
        <Route path={"/music/:artist/:song"}>
          {({ match }): JSX.Element => (
            <p>
              {"Viewing artist:"}&nbsp;{match?.params.artist}
              <br />
              {"Song:"}&nbsp;{match?.params.song}
            </p>
          )}
        </Route>
      </Switch>
    </MemoryRouter>
  );
};

const WithLinks = TemplateWithRouter.bind({});
WithLinks.args = {
  dataset: [
    { artist: "placebo", song: "a million little pieces", year: "2010" },
    { artist: "nirvana", song: "heart shaped box", year: "1992" },
    { artist: "ghost", song: "zenith", year: "2015" },
    { artist: "def leppard", song: "hysteria", year: "1987" },
  ],
  exportCsv: false,
  headers: [
    { dataField: "artist", header: "Artist name" },
    {
      dataField: "song",
      formatter: linkFormatter<Record<string, string>>(
        (cell, row): string => `/music/${row.artist}/${cell}`
      ),
      header: "Song name",
    },
    { dataField: "year", header: "Year of release" },
  ],
  id: "songsTable",
  pageSize: 10,
  search: false,
};

export { Default, WithLinks };
export default config;
