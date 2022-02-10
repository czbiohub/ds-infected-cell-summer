import { Banner, Container, Heading } from "@czbiohub/cz-ui";
import InfoBox from "../components/InfoBox/InfoBox";
import styles from "../styles/InfoBoxes.module.scss";

export default function Home() {
  return (
    <div>
      <Banner
        mainText="Infected Cell"
        paragraph="Portal for the infected cell project"
        backgroundUrl="/images/opencell_logo.webp"
      />
      <Container>
        <div>
          <Heading title="Infected Cell" />
          <div className={styles.container}>
            <InfoBox
              title={"The Infected Cell: An Atlas for Viral Infection"}
              description={"As the COVID-19 pandemic has shown, infectious diseases and emerging new viruses remain a major threat to human health. Our goals are three-fold: first, to understand virus-host interactions as a guide for developing antiviral therapeutics, second to develop vaccines and preemptively identify emerging viruses, and finally, to disseminate technologies needed to diagnose and discover the source of microbial infections."}
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
