import React, { Component } from "react";
import { BrowserRouter as Router, Route, Link, Switch } from "react-router-dom";

import { BiohubUI, Banner, Footer, NavBar, Link as CZUILink } from "cz-ui";

import AboutLemur from "./infected-cell-pages/About.jsx";
import DataAccess from "./infected-cell-pages/DataAccess.jsx";
import CellxgeneInfoBoxView from "./infected-cell-pages/CellxgeneInfoBoxView.jsx";
import DataVizs from "./infected-cell-pages/DataVizs.jsx";
import CompareScreens from "./infected-cell-pages/CompareScreens.jsx";

import cs from "./appIC.module.scss";
import { StylesProvider } from "@material-ui/core/styles";

/**
 * How to add a new page:
 * 1. Import the components at the top
 * 2. Fill the pages array below in the desired page order
 */

const pages = [
  {
    menuTitle: "HOME", // what shows up on the menu
    title: "Home", // the actual page title
    path: "/", // the path passed to <Route />
    exact: true, // path has to be exactly a "/"
    component: CellxgeneInfoBoxView, // the component
  },
  {
    menuTitle: "ABOUT",
    title: "About",
    path: "/about",
    component: AboutLemur,
  },
  {
    menuTitle: "DATA",
    title: "Data",
    path: "/whereisthedata",
    component: DataAccess,
  },
  {
    menuTitle: "EXPLORE SCREENS",
    title: "Explore Screens",
    path: "/datavizs",
    component: DataVizs,
  },
  {
    menuTitle: "COMPARE SCREENS",
    title: "Compare Screens",
    path: "/comparescreens",
    component: CompareScreens,
  },
];

class AppInfectedCell extends Component {
  constructor(props) {
    super(props);
    this.state = {
      selectedIndex: 0,
    };
  }

  componentDidMount() {
    // Page user is on when refreshed or newly loaded
    const path = this.props.location.pathname;
    const pageIndex = pages.findIndex((x) => x.path === path);
    this.setState({ selectedIndex: pageIndex });
  }

  render() {
    return (
      <StylesProvider injectFirst>
        <BiohubUI>
          <Router basename="/">
            <div class={cs.layout}>
              <div class={cs.content}>
                <NavBar
                  accent
                  title={"Tabula Sapiens"}
                  // titleOptions={[
                  //   <CZUILink
                  //     component={Button}
                  //     href="http://www.czbiohub.org"
                  //     target="_blank"
                  //   >
                  //     CZ BIOHUB
                  //   </CZUILink>,
                  // ]}
                  navLinks={pages.map((page, i) => (
                    <CZUILink
                      component={Link}
                      to={page.path}
                      key={i}
                      onClick={() => this.setState({ selectedIndex: i })}
                    >
                      {page.menuTitle}
                    </CZUILink>
                  ))}
                  navSelectedLinkIndex={this.state.selectedIndex}
                />
                <Switch>
                  {pages.map((route, i) => (
                    <Route key={i} {...route} />
                  ))}
                </Switch>
              </div>

              <div className={cs.footer}>
                <Footer
                  navLinks={[
                    <CZUILink href="/">HOME</CZUILink>,
                    <CZUILink href="http://www.czbiohub.org/" target="_blank">
                      CZ BIOHUB
                    </CZUILink>,
                    <CZUILink
                      href="https://docs.google.com/forms/d/e/1FAIpQLSeWMqdbrCtSZ2U-cp7OELswEMVchPUJZ-L8REwQf3-nC0JmWQ/viewform?usp=sf_link"
                      target="_blank"
                    >
                      CONTACT US
                    </CZUILink>,
                  ]}
                />
              </div>
            </div>
          </Router>
        </BiohubUI>
      </StylesProvider>
    );
  }
}

export default AppInfectedCell;
