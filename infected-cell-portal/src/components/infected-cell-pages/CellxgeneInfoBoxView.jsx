import React, { Component } from "react";

import { InfoBox } from "hub-ui";
import { Banner } from "cz-ui";
import Heading from "./Heading.jsx";
import cs from "./Cellxgene.module.scss";

class CellxgeneInfoBoxView extends Component {
  render() {
    return (
      <div>
        <Banner
          backgroundUrl={"../../images/opencell_logo.png"}
          mainText="Infected Cell"
          paragraph="portal for the infected cell project"
        />
        <div className={cs.content}>
          <Heading title="Mouse lemur" />
          <InfoBox
            title={"The infected cell"}
            description={"The Infected Cell, an atlas of viral infection"}
            buttonTitle="Read more about it"
            buttonLink="https://opencell.czbiohub.org/"
            openInNewTab={true}
            image={"../../images/opencell_logo.png"}
          />
        </div>
      </div>
    );
  }
}

export default CellxgeneInfoBoxView;
