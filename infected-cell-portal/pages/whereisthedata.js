import { Container, Heading } from "@czbiohub/cz-ui";
import React from "react";
import DataSummary from "../components/LemurSummary/DataSummary";
import path from "path";
import { promises as fs } from "fs";
import { csvParse } from "d3-dsv";

export default function whereisthedata({
  csvData,
  columns,
  filterItems,
  filterKey,
}) {
  return (
    <div>
      <Container>
        <div>
          <Heading title="Data Release Policy" />
          <p>
            Our goal is to make the data generated within this project rapidly and broadly available to
            the scientific community as a community resource. It is our
            intention to publish the work of this project in a timely fashion,
            and we welcome collaborative interaction on the project and
            analyses. However, considerable investment was made in generating
            these data and we ask that you respect rights of first publication
            and acknowledgment as outlined in the Toronto agreement (Toronto
            International Data Release Workshop Authors. Prepublication data
            sharing.{" "}
            <a
              href="https://www.nature.com/articles/461168a"
              target="_blank"
              rel="noreferrer"
            >
              Nature. 2009 Sep 10;461(7261):168-70
            </a>
            ). By accessing these data, you agree not to publish any articles
            prior to initial publication by the Infected Cell Consortium and its
            collaborating scientists. If you wish to make use of restricted data
            for publication or are interested in collaborating on the analyses
            of these data, please use the{" "}
            <a
              href="https://docs.google.com/forms/d/e/1FAIpQLSfiFpDh2sHO2gXWngdHU6i-_Nsofzi_BGO9XLlIhWeZeIHffA/viewform?usp=sf_link"
              target="_blank"
              rel="noreferrer"
            >
              contact form
            </a>
            . Redistribution of these data should include the full text of the
            data use policy.
          </p>
        </div>
      </Container>
      <div>
        <DataSummary
          data={csvData}
          columns={columns}
          filterItems={filterItems}
          filterKey={filterKey}
        />
      </div>
    </div>
  );
}

export async function getStaticProps() {
  const columns = [
    {
      dataKey: "First Author",
      header: "First Author",
      bold: true,
      width: 100,
      flexGrow: 3,
    },
    {
      dataKey: "Virus Acronym",
      header: "Virus Acronym",
      width: 100,
      flexGrow: 3,
    },
    {
      dataKey: "Virus",
      header: "Virus",
      width: 100,
      flexGrow: 3,
    },
    {
      dataKey: "Publication",
      header: "Publication",
      width: 400,
      flexGrow: 3,
    },
    {
      dataKey: "Link to raw data",
      header: "Link to raw data",
      width: 400,
      flexGrow: 3,
    },
    {
      dataKey: "Library Used",
      header: "Library Used",
      width: 100,
      flexGrow: 3,
    },
    {
      dataKey: "Status",
      header: "Status",
      width: 100,
      flexGrow: 3,
    },
  ];

  const filterItems = [
    {
      value: "",
      label: "Show all",
    },
    {
      value: "Dengue virus 2 16681 strain",
      label: "Dengue",
    },
    {
      value: "SARS-CoV-2",
      label: "SARS-CoV-2",
    },
    {
      value: "Human coronavirus OC43",
      label: "Human coronavirus",
    },
    {
      value: "Human coronavirus 229E",
      label: "Human coronavirus",
    },
    {
      value: "Human coronavirus NL63",
      label: "Human coronavirus",
    },
    {
      value: "Hepatitis C virus JFH1",
      label: "Hepatitis C",
    },
    {
      value: "Hepatitis A virus",
      label: "Hepatitis A",
    },
    {
      value: "West Nile virus",
      label: "West Nile",
    },
    {
      value: "enterovirus D68",
      label: "enterovirus",
    },
    {
      value: "Rhinovirus C15",
      label: "Rhinovirus",
    },
    {
      value: "Ebola (Mayinga)",
      label: "Ebola",
    },
  ];

  const filterKey = "Virus";

  const csvFilePath = path.join(
    process.cwd(),
    "public",
    "data",
    "CRISPR_screen_datasets.csv"
  );
  const csvFile = await fs.readFile(csvFilePath, "utf-8");

  const csvData = await csvParse(csvFile);
  return {
    props: { csvData, columns, filterItems, filterKey },
  };
}
