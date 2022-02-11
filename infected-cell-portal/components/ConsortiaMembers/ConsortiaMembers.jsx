import { LogoComplete } from "@czbiohub/cz-ui";
import Image from "next/image";
import React from "react";
import styles from "./ConsortiaMembers.module.scss";

export default function ConsortiaMembers() {
  return (
    <div className={styles.container}>
      <LogoComplete className={styles.picture} />
      
    </div>
  );
}
