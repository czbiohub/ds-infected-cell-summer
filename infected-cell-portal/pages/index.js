import { Banner, Container, Heading } from "@czbiohub/cz-ui";
import InfoBox from "../components/InfoBox/InfoBox";
import styles from "../styles/InfoBoxes.module.scss";

export default function Home() {
  return (
    <div>
      <Banner
        mainText="The Infected Cell"
        paragraph="A complete exploration of essential virus-host interactions using multimodal approaches"
        backgroundUrl="/images/opencell_logo.webp"
      />
      <Container>
        <div>
          <Heading title="Projects" />
          <div className={styles.container}>
            <InfoBox
              title={"The Infected Cell: An Atlas for Viral Infection"}
              description={"As the COVID-19 pandemic has shown, infectious diseases and emerging new viruses remain a major threat to human health. Our goals are three-fold: first, to understand virus-host interactions as a guide for developing antiviral therapeutics, second to develop vaccines and preemptively identify emerging viruses, and finally, to disseminate technologies needed to diagnose and discover the source of microbial infections."}
              buttonTitle="Read more about it"
              buttonLink="https://ds-infected-cell-summer.vercel.app/"
              openInNewTab={true}
              image={"/images/opencell_logo.webp"}
            />
            <InfoBox
              title={"OpenCell"}
              description={"Proteome-scale measurements of human protein localization and interactions."}
              buttonTitle="Read more about it"
              buttonLink="https://opencell.czbiohub.org/"
              openInNewTab={true}
              image={"/images/opencell_logo.webp"}
            />
          </div>
        </div>
      </Container>
    </div>
  );
}
