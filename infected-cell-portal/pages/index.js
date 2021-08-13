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
          <Heading title="Mouse Lemur" />
          <div className={styles.container}>
            <InfoBox
              title={"The infected cell"}
              description={"The Infected Cell, an atlas of viral infection"}
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
