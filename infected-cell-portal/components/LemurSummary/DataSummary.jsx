import React, { Component } from "react";
import { orderBy, filter } from "lodash/fp";

import { Container, Select, Table } from "@czbiohub/cz-ui";
import cs from "./DataSummary.module.scss";
import loadingStyles from "../../styles/loading.module.scss";

class DataSummary extends Component {
  constructor(props) {
    super(props);

    this.state = {
      selectedDonor: "",
      searchQuery: "",
      sortParams: null,
    };
  }

  setSelectedDonor = (selectedDonor) => {
    this.setState({
      selectedDonor,
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
  filterData = (data, filterKey) => {
    const { selectedDonor, searchQuery } = this.state;
    let filteredData = data;
    if (selectedDonor) {
      filteredData = filter([filterKey, selectedDonor], filteredData);
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

  processData = (data, filterKey) => {
    return this.sortData(this.filterData(data, filterKey));
  };

  // const VerboseTableStory = () => {
  render() {
    const { selectedDonor, sortParams } = this.state;
    const { data, columns, filterItems, filterKey } = this.props;
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
        <div className={cs.container}>
          <Container>
            <div className={cs.controls}>
              {/* <Search className={cs.search} onSearch={this.setSearchQuery} /> */}
              <Select
                // items={statuses.map((status, i) => ({value: i, label: status}))}
                className={cs.select}
                items={filterItems}
                value={selectedDonor}
                onChange={this.setSelectedDonor}
                placeholder="Filter by donor..."
              />
            </div>
            <div className={cs.description}>
              Click on the table headers to sort by column.
            </div>
          </Container>
          <div className={cs.tableContainer}>
            {data && (
              <Table
                data={this.processData(data, filterKey)}
                columns={columns}
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
