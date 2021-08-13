import React, { Component } from "react";
import { orderBy, filter } from "lodash/fp";

import { Container, Select, Table, Heading } from "@czbiohub/cz-ui";
import cs from "./DataSummary.module.scss";
import loadingStyles from "../../styles/loading.module.scss";

import { csv } from "d3-fetch";

const COLUMNS = [
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

const Individuals = [
  {
    value: null,
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

class DataSummary extends Component {
  constructor(props) {
    super(props);

    this.state = {
      selectedIndividual: null,
      searchQuery: "",
      sortParams: null,
      tableData: null,
    };
  }

  setSelectedIndividual = (selectedIndividual) => {
    this.setState({
      selectedIndividual,
    });
  };

  setSearchQuery = (searchQuery) => {
    this.setState({
      searchQuery,
    });
  };

  setSortParams = (sortParams) => {
    this.setState({
      sortParams,
    });
  };

  setTableData = (tableData) => {
    this.setState({
      tableData,
    });
  };

  componentDidMount() {
    csv("/data/CRISPR_screen_datasets.csv").then((csvData) => {
      this.setTableData(csvData);
    });
  }

  // Sort the data based on the sort params.
  sortData = (data) => {
    const { sortParams } = this.state;
    if (!sortParams) return data;

    return orderBy([sortParams.dataKey], [sortParams.order], data);
  };

  matchesQuery = (datum, attribute, searchQuery) =>
    datum[attribute] &&
    datum[attribute]
      .toString()

      .toLowerCase()
      .includes(searchQuery.toLowerCase());

  // Filter the data based on various options.
  filterData = (data) => {
    const { selectedIndividual, searchQuery } = this.state;
    let filteredData = data;
    console.log(filteredData);
    if (selectedIndividual) {
      filteredData = filter(["Individual", selectedIndividual], filteredData);
    }

    if (searchQuery) {
      filteredData = filter(
        (datum) =>
          this.matchesQuery(datum, "sex", searchQuery) ||
          this.matchesQuery(datum, "age", searchQuery),
        filteredData
      );
    }
    return filteredData;
  };

  processData = (data) => {
    return this.sortData(this.filterData(data));
  };

  // const VerboseTableStory = () => {
  render() {
    const { selectedIndividual, sortParams, tableData } = this.state;
    // Sorting is not implemented in the Table.
    // You must store the sortParams and implement the sorting logic in the parent component.
    // const [sortParams, setSortParams] = React.useState(null);

    // function processData(data) {
    //   // Sort data according to the sortParams.
    //   if (!sortParams) return data;

    //   return orderBy([sortParams.dataKey], [sortParams.order], data);
    // }

    return (
      <div className={loadingStyles.container}>
        {!tableData && (
          <div className={loadingStyles.loadingContainer}>
            <div className={loadingStyles.loadingCenter}>Loading...</div>
          </div>
        )}
        <div className={cs.container}>
          <Container>
            <Heading title="Data summary" />
            <div className={cs.controls}>
              {/* <Search className={cs.search} onSearch={this.setSearchQuery} /> */}
              <Select
                // items={statuses.map((status, i) => ({value: i, label: status}))}
                className={cs.select}
                items={Individuals}
                value={selectedIndividual}
                onChange={this.setSelectedIndividual}
                placeholder="Filter by individual..."
              />
            </div>
            <div className={cs.description}>
              Click on the table headers to sort by column.
            </div>
          </Container>
          <div className={cs.tableContainer}>
            {tableData && (
              <Table
                data={this.processData(tableData)}
                columns={COLUMNS}
                className={cs.table}
                onSortParamChange={this.setSortParams}
                sortParams={sortParams}
              />
            )}
          </div>
        </div>
      </div>
    );
  }
}

export default DataSummary;
