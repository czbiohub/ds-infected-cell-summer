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
          href="https://docs.google.com/forms/d/e/1FAIpQLSeeB0N7TrklXbCbpc6nDi5e77uad3uZDZ4WCMV77jwhVzxUtQ/viewform?usp=sf_link"
          target="_blank"
          rel="noreferrer"
          className={styles.link}
        >
          Contact Us (this link is still for Tabula Sapiens)
        </a>
      </NavLink>
    </F>
  );
}
