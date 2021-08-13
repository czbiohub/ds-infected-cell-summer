import React from "react";
import { Container, Heading } from "@czbiohub/cz-ui";
import Image from "next/image";
import Link from "next/link";
import ConsortiaMembers from "../components/ConsortiaMembers/ConsortiaMembers";

export default function about() {
  return (
    <div>
      <Container>
        <div>
          <Heading title="About" />
          <p>
            The Infected Cell Project presents a unique oppotunity to understand
            <ul>
              <li>
                <b>viruses as a threat:</b> defining essential host pathways for
                infection and building assays for anti-viral screening
              </li>
              <li>
                <b>viruses as a tool:</b> following viruses to illuminate human
                cell biology
              </li>
              <li>
                <b>viruses as a forcing function:</b> to integrate Biohub’s
                multi-disciplinary expertise
              </li>
            </ul>
          </p>
          <p>
            The challenge we aim to solve is how can we build approaches that
            can address both the diversity of viral families and the diversity
            of cellular responses that they generate.
          </p>
          <p>
            This current version of the Infected Cell Project utilizes CRISPR
            screen data from 10+ families of viruses in order to explore
            host-factor interactions. This enhances our understanding of the
            mechanisms of viral infection and helps to develop new technologies
            that will lead to actionable diagnostics and effective therapies.
          </p>
          <Image
            src="/images/opencell_logo.webp"
            width={1660 / 5}
            height={1840 / 5}
          />
          <p>
            Our goal is to make sequence data rapidly and broadly available to
            the scientific community as a community resource. Before you use our
            data, please read our{" "}
            <Link href="/whereisthedata">
              <a>Data Release Policy</a>
            </Link>{" "}
            and feel free to reach out to our group using the{" "}
            <a
              href="https://docs.google.com/forms/d/e/1FAIpQLSeWMqdbrCtSZ2U-cp7OELswEMVchPUJZ-L8REwQf3-nC0JmWQ/viewform?usp=sf_link"
              target="_blank"
              rel="noreferrer"
            >
              contact form.
            </a>
          </p>
        </div>
        <div>
          <Heading title="Consortium Members" />
          <ConsortiaMembers />
        </div>
        <div>
          <Heading title="Acknowledgments" />
          <p>thank you thank you thank you</p>
        </div>
      </Container>
    </div>
  );
}
