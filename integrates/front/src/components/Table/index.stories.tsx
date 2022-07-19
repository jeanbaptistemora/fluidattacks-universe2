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

const dataset = [
  {
    artist: "Placebo",
    song: "A Million Little Pieces",
    year: "2010",
  },
  {
    artist: "Nirvana",
    song: "Heart Shaped Box",
    year: "1992",
  },
  {
    artist: "Ghost",
    song: "Zenith",
    year: "2015",
  },
  {
    artist: "Def Leppard",
    song: "Lysteria",
    year: "1987",
  },
  {
    artist: "Louis Armstrong",
    song: "What A Wonderful World",
    year: "1967",
  },
  {
    artist: "Ed Sheeran",
    song: "Perfect",
    year: "2017",
  },
  {
    artist: "Queen",
    song: "Bohemian Rhapsody",
    year: "1975",
  },
  {
    artist: "Gotye",
    song: "Somebody That I Used To Know",
    year: "2011",
  },
  {
    artist: "Israel Kamakawiwo'ole",
    song: "Somewhere Over The Rainbow",
    year: "1990",
  },
  {
    artist: "Michael Jackson",
    song: "Beat It",
    year: "1982",
  },
  {
    artist: "Passenger",
    song: "Let Her Go",
    year: "2012",
  },
];

const headers = [
  {
    dataField: "artist",
    header: "Artist name",
  },
  {
    dataField: "song",
    header: "Song name",
  },
  {
    dataField: "year",
    header: "Year of release",
  },
];

const Template: Story<ITableProps> = (props): JSX.Element => {
  return <Table {...props} />;
};

const Default = Template.bind({});
Default.args = {
  dataset,
  exportCsv: false,
  headers,
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
  dataset,
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
