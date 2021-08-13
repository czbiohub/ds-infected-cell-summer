import styles from "../styles/Dash.module.scss";

export default function MarkerGenes() {
  return (
    <iframe
      src="http://127.0.0.1:8050/"
      className={styles.dash}
      title="Dash Visualization"
    />
  );
}
