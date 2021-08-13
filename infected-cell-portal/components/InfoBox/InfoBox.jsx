// From hub-ui, but with Next.js Image component

import React from "react";
import Image from "next/image";

import cs from "./InfoBox.module.scss";
import { Button } from "@czbiohub/cz-ui";

const InfoBox = function (props) {
  const anchorProps = {};
  if (props.openInNewTab) {
    anchorProps.target = "_blank";
  }
  return (
    <div className={cs.container}>
      <div className={cs.image}>
        <Image
          src={props.image}
          alt={props.alt}
          layout="fill"
          objectFit="cover"
          objectPosition="left"
        />
      </div>
      <div className={cs.text}>
        <h2 className={cs.title}>{props.title}</h2>
        <p>{props.description}</p>
        <a href={props.buttonLink} className={cs.buttonLink} {...anchorProps}>
          <Button color="primary">{props.buttonTitle}</Button>
        </a>
      </div>
    </div>
  );
};

export default InfoBox;
