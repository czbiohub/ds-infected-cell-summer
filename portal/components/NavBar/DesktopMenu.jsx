import React from "react";
import { NavBar, NavLink, NavLinkGroup, GroupNavLink } from "@czbiohub/cz-ui";
import Link from "next/link";
import styles from "./NavBar.module.scss";
import { useRouter } from "next/router";

export default function DesktopMenu({ menuTitle, pages }) {
  const router = useRouter();

  return (
    <NavBar title={menuTitle} accent onLogoClick={() => router.push("/")}>
      {pages.map((page, i) => (
        <React.Fragment key={i}>
          {!page.group && (
            <NavLink selected={router.pathname === page.path}>
              <Link href={page.path}>
                <a className={styles.link}>{page.title}</a>
              </Link>
            </NavLink>
          )}
          {page.group && (
            <NavLinkGroup
              title={page.title}
              accent
              selected={page.links.find((e) => e.path === router.pathname)}
            >
              {page.links.map((page, j) => (
                <GroupNavLink key={j} selected={router.pathname === page.path}>
                  <Link href={page.path}>
                    <a className={styles.link}>{page.title}</a>
                  </Link>
                </GroupNavLink>
              ))}
            </NavLinkGroup>
          )}
        </React.Fragment>
      ))}
    </NavBar>
  );
}
