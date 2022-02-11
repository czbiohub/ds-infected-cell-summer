import React from "react";
import { Footer as F, NavLink } from "@czbiohub/cz-ui";
import Link from "next/link";
import styles from "./Footer.module.scss";

export default function Footer() {
  return (
    <F>
      <NavLink>
        <Link href="/">
          <a className={styles.link}>Home</a>
        </Link>
      </NavLink>
      <NavLink>
        <a
          href="http://www.czbiohub.org/"
          target="_blank"
          rel="noreferrer"
          className={styles.link}
        >
          CZ Biohub
        </a>
      </NavLink>
      <NavLink>
        <a
          href="https://docs.google.com/forms/d/e/1FAIpQLSfiFpDh2sHO2gXWngdHU6i-_Nsofzi_BGO9XLlIhWeZeIHffA/viewform?usp=sf_link"
          target="_blank"
          rel="noreferrer"
          className={styles.link}
        >
          Contact Us
        </a>
      </NavLink>
    </F>
  );
}
