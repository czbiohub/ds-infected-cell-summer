import { BiohubUI } from "@czbiohub/cz-ui";
import "@czbiohub/cz-ui/dist/main.css";
import "../styles/globals.css";
import NavBar from "../components/NavBar/NavBar";
import Footer from "../components/Footer/Footer";

function MyApp({ Component, pageProps }) {
  return (
    <BiohubUI>
      <div className="layout">
        <div className="content">
          <NavBar />
          <Component {...pageProps} />
        </div>
        <Footer />
      </div>
    </BiohubUI>
  );
}

export default MyApp;
