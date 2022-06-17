import styles from "../styles/Dash.module.scss";

export default function MarkerGenes() {
  return (
    <iframe
      src="https://onclass-dash-development.ds.czbiohub.org/ic-app"
      className={styles.dash}
      title="Heatmap"
    />
  );
}
