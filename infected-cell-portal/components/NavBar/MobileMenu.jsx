import React from "react";
import { MobileNavBar, NavLink, MobileNavLinkGroup } from "@czbiohub/cz-ui";
import Link from "next/link";
import styles from "./NavBar.module.scss";
import { useRouter } from "next/router";

export default function MobileMenu({
  menuTitle,
  menuOpen,
  setMenuOpen,
  pages,
}) {
  const router = useRouter();

  return (
    <MobileNavBar
      title={menuTitle}
      accent
      menuOpen={menuOpen}
      onHamburgerClick={setMenuOpen}
      onLogoClick={() => router.push("/")}
    >
      {pages.map((page, i) => (
        <React.Fragment key={i}>
          {!page.group && (
            <NavLink iselected={router.pathname === page.path}>
              <Link href={page.path}>
                <a className={styles.link} onClick={() => setMenuOpen(false)}>
                  {page.title}
                </a>
              </Link>
            </NavLink>
          )}
          {page.group && (
            <MobileNavLinkGroup title={page.title}>
              {page.links.map((page, j) => (
                <NavLink key={j} selected={router.pathname === page.path}>
                  <Link href={page.path}>
                    <a
                      className={styles.link}
                      onClick={() => setMenuOpen(false)}
                    >
                      {page.title}
                    </a>
                  </Link>
                </NavLink>
              ))}
            </MobileNavLinkGroup>
          )}
        </React.Fragment>
      ))}
    </MobileNavBar>
  );
}
