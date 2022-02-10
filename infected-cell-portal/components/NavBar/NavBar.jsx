import React, { useState, useEffect, useRef } from "react";
import { useRouter } from "next/router";
import { NextSeo } from "next-seo";
import MobileMenu from "./MobileMenu";
import DesktopMenu from "./DesktopMenu";

/**
 * Edit the website title, description, and URL here.
 */
const menuTitle = "Infected Cell";
const description = "Infected Cell description";
const url = "https://czbiohub-portal-template.vercel.app";

/**
 * Edit the SEO here.
 * Title, description, and canonical URL are already added.
 */
const Seo = ({ title, description, pathname }) => {
  return (
    <NextSeo
      title={title}
      description={description}
      canonical={url + pathname}
      openGraph={{
        title: title,
        description: description,
        images: [
          {
            url: "/images/sapiens_logo.webp",
            width: 1887,
            height: 2487,
            alt: "Tabula Sapiens Logo",
          },
        ],
        site_name: title,
      }}
      twitter={{
        handle: "@czbiohub",
        site: "@czbiohub",
        cardType: "summary_large_image",
      }}
    />
  );
};

/**
 * Depending on how many menu items there are,
 * you may need to change the breakpoint for when
 * the menu switches from the desktop version to
 * the mobile version.
 *
 * The breakpoint here means that the website window
 * has to be at least 1150px wide for the desktop menu
 * to show.
 */
const menuBreakpoint = 1150;

/**
 * Edit the nav bar pages here.
 *
 * The hide boolean disables the page name
 * from showing up in the page title. For example,
 * the page title for "Home" won't be
 * "Home - Tabula Sapiens", it will just be "Tabula Sapiens"
 * since the hide boolean is true.
 */
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
    title: "Single Screens",
    path: "/singlescreens",
  },
  {
    title: "Compare Screens",
    path: "/comparescreens",
  },

  {
    title: "Heatmaps",
    path: "/heatmaps",
  },
];

export default function NavBar() {
  const router = useRouter();
  const [menuOpen, setMenuOpen] = useState(false);
  const [width, setWidth] = useState(0);
  const wrapperRef = useRef(null);

  function useOutsideAlerter(ref) {
    useEffect(() => {
      function handleClickOutside(event) {
        if (ref.current && !ref.current.contains(event.target)) {
          setMenuOpen(false);
        }
      }
      document.addEventListener("mousedown", handleClickOutside);
      return () => {
        document.removeEventListener("mousedown", handleClickOutside);
      };
    }, [ref]);
  }

  useOutsideAlerter(wrapperRef);

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

  let pageObject = pages.find((page) => page.path == router.pathname);
  if (!pageObject) {
    pages.forEach((page) => {
      if (page.group) {
        pageObject = page.links.find((page) => page.path == router.pathname);
      }
    });
  }

  const title = pageObject?.hide
    ? menuTitle
    : pageObject?.title + " - " + menuTitle;

  return (
    <div>
      <Seo title={title} description={description} pathname={router.pathname} />
      {width < menuBreakpoint ? (
        <MobileMenu
          menuTitle={menuTitle}
          menuOpen={menuOpen}
          setMenuOpen={setMenuOpen}
          pages={pages}
        />
      ) : (
        <DesktopMenu menuTitle={menuTitle} pages={pages} />
      )}
    </div>
  );
}
