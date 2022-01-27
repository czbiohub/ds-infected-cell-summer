import { LogoComplete } from "@czbiohub/cz-ui";
import Image from "next/image";
import React from "react";
import styles from "./ConsortiaMembers.module.scss";

export default function ConsortiaMembers() {
  return (
    <div className={styles.container}>
      <LogoComplete className={styles.picture} />
      <div className={styles.picture}>
        <Image
          src="/images/consortia_members/stanford_logo.webp"
          layout="fill"
          objectFit="contain"
          alt="Logo"
        />
      </div>
      <div className={styles.picture}>
        <Image
          src="/images/consortia_members/MNHN-logo.webp"
          layout="fill"
          objectFit="contain"
          alt="Logo"
        />
      </div>
      <div className={styles.picture}>
        <Image
          src="/images/consortia_members/hkust_logo.webp"
          layout="fill"
          objectFit="contain"
          alt="Logo"
        />
      </div>
      <div className={styles.picture}>
        <Image
          src="/images/consortia_members/amel_logo.webp"
          layout="fill"
          objectFit="contain"
          alt="Logo"
        />
      </div>
      <div className={styles.picture}>
        <Image
          src="/images/consortia_members/ucsf_logo.webp"
          layout="fill"
          objectFit="contain"
          alt="Logo"
        />
      </div>
    </div>
  );
}
