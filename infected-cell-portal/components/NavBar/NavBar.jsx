import React, { useState, useEffect } from "react";
import { NavBar as Bar, MobileNavBar as MBar, NavLink } from "@czbiohub/cz-ui";
import Link from "next/link";
import styles from "./NavBar.module.scss";
import { useRouter } from "next/router";
import Head from "next/head";

const pages = [
  {
    title: "Home",
    path: "/",
  },
  {
    title: "About",
    path: "/about",
  },
  {
    title: "Data",
    path: "/whereisthedata",
  },
  {
    title: "Explore Screens",
    path: "/explorescreens",
  },
  {
    title: "Compare Screens",
    path: "/comparescreens",
  },
];

const menuTitle = "Infected Cell";

export default function NavBar() {
  const router = useRouter();
  const [menuOpen, setMenuOpen] = useState(false);
  const [width, setWidth] = useState(999);

  useEffect(() => {
    setWidth(window.innerWidth);
  }, []);

  const updateSize = () => {
    setWidth(window.innerWidth);
  };

  useEffect(() => {
    window.addEventListener("resize", updateSize);
    return () => {
      window.removeEventListener("resize", updateSize);
    };
  }, []);

  const MobileMenu = () => {
    return (
      <MBar
        title={menuTitle}
        accent
        menuOpen={menuOpen}
        onHamburgerClick={setMenuOpen}
      >
        {pages.map((page, i) => (
          <NavLink key={i} selected={router.pathname === page.path}>
            <Link href={page.path}>
              <a className={styles.link} onClick={() => setMenuOpen(false)}>
                {page.title}
              </a>
            </Link>
          </NavLink>
        ))}
      </MBar>
    );
  };

  const DesktopMenu = () => {
    return (
      <Bar title={menuTitle} accent>
        {pages.map((page, i) => (
          <NavLink key={i} selected={router.pathname === page.path}>
            <Link href={page.path}>
              <a className={styles.link} onClick={() => setMenuOpen(false)}>
                {page.title}
              </a>
            </Link>
          </NavLink>
        ))}
      </Bar>
    );
  };

  return (
    <div>
      <Head>
        <title>
          {pages.find((page) => page.path == router.pathname)?.title +
            " - " +
            menuTitle}
        </title>
      </Head>
      {width < 980 && <MobileMenu />}
      {width > 980 && <DesktopMenu />}
    </div>
  );
}
