import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import pandas as pd
import matplotlib.dates as mdates
import seaborn as sns

def scaled_plots(df: pd.DataFrame, x_range: float) -> None:
    num_cols = len(df.columns)
    fig, axs = plt.subplots(1, num_cols, figsize=(5 * num_cols, 4))

    if num_cols == 1:
        axs = [axs]  # Sicherstellen, dass axs iterierbar ist

    for i, col in enumerate(df.columns):
        sns.histplot(df[col], bins=30, kde=True, ax=axs[i])
        axs[i].set_title(f"Verteilung: {col}")
        axs[i].set_xlim(-x_range, x_range)

    plt.tight_layout()
    plt.show()

def plot_3d_clusters(X: np.ndarray,
                     labels: np.ndarray,
                     feature_names: list[str] = None,
                     title: str = "3D-Clusterdarstellung",
                     cluster_colors: dict = None,
                     alpha: float = 0.5) -> None:

    if X.shape[1] != 3:
        raise ValueError("X muss exakt 3 Spalten haben für eine 3D-Darstellung.")

    fig = plt.figure(figsize=(5, 5))
    ax = fig.add_subplot(111, projection='3d')

    if cluster_colors:
        for label in np.unique(labels):
            idx = labels == label
            ax.scatter(X[idx, 0], X[idx, 1], X[idx, 2],
                       c=cluster_colors.get(label, "gray"),
                       alpha=alpha, s=30, label=f"Cluster {label}")
    else:
        ax.scatter(X[:, 0], X[:, 1], X[:, 2],
                   c=labels, cmap='viridis', s=30, alpha=alpha)


    if feature_names and len(feature_names) == 3:
        ax.set_xlabel(feature_names[0])
        ax.set_ylabel(feature_names[1])
        ax.set_zlabel(feature_names[2])
    else:
        ax.set_xlabel("Feature 1")
        ax.set_ylabel("Feature 2")
        ax.set_zlabel("Feature 3")

    ax.set_title(title)
    ax.legend()
    plt.tight_layout()
    plt.show()


def plot_2d_projections(X: np.ndarray,
                        labels: np.ndarray = None,
                        centers: np.ndarray = None,
                        feature_names: list[str] = None,
                        title: str = "2D-Projektionen der Cluster",
                        cluster_colors: dict = None,
                        alpha: float = 0.5) -> None:

    if X.shape[1] != 3:
        raise ValueError("X muss exakt 3 Spalten haben (3 Features)")

    fig, axs = plt.subplots(1, 3, figsize=(18, 5))
    combinations = [(0, 1), (0, 2), (1, 2)]

    for i, (x_idx, y_idx) in enumerate(combinations):
        ax = axs[i]

        if labels is not None and cluster_colors:
            for label in np.unique(labels):
                idx = labels == label
                ax.scatter(X[idx, x_idx], X[idx, y_idx],
                           s=20, color=cluster_colors.get(label, "gray"),
                           alpha=alpha, label=f"Cluster {label}")
        elif labels is not None:
            ax.scatter(X[:, x_idx], X[:, y_idx], c=labels, cmap='viridis', s=20, alpha=alpha)
        else:
            ax.scatter(X[:, x_idx], X[:, y_idx], s=20, color='gray', alpha=alpha)

        if centers is not None:
            ax.scatter(centers[:, x_idx], centers[:, y_idx],
                       c='black', marker='x', s=100, label='Zentrum')

        if feature_names:
            ax.set_xlabel(feature_names[x_idx])
            ax.set_ylabel(feature_names[y_idx])
        else:
            ax.set_xlabel(f'Feature {x_idx + 1}')
            ax.set_ylabel(f'Feature {y_idx + 1}')

        ax.set_title(f'{ax.get_xlabel()} vs {ax.get_ylabel()}')
        ax.legend()

    fig.suptitle(title)
    plt.tight_layout()
    plt.show()


def plots(df: pd.DataFrame,
          startdatum: str,
          tage: int,
          licht_limits: tuple = None,
          temperatur_limits: tuple = None,
          feuchtigkeit_limits: tuple = None,
          cluster_column: str = None,
          cluster_colors: dict = None):

    df['zeit'] = pd.to_datetime(df['zeit'])
    start = pd.to_datetime(startdatum)
    ende = start + pd.Timedelta(days=tage)
    df_filter = df[(df['zeit'] >= start) & (df['zeit'] < ende)].copy()

    fig, axs = plt.subplots(3, 1, figsize=(12, 8), sharex=True)

    # --- Clusterhintergrund einzeichnen ---
    if cluster_column and cluster_column in df_filter.columns:
        if cluster_colors is None:
            # Standardfarben für Cluster 0, 1, 2, ...
            cluster_colors = {i: f"C{i}" for i in df_filter[cluster_column].unique()}
        
        current_cluster = None
        start_time = None

        for i, row in df_filter.iterrows():
            cluster = row[cluster_column]
            zeit = row['zeit']

            if current_cluster is None:
                current_cluster = cluster
                start_time = zeit

            elif cluster != current_cluster:
                for ax in axs:
                    ax.axvspan(start_time, zeit, color=cluster_colors.get(current_cluster, "gray"), alpha=0.6)
                current_cluster = cluster
                start_time = zeit

        # Letzten Abschnitt noch einfärben
        for ax in axs:
            ax.axvspan(start_time, df_filter['zeit'].iloc[-1], color=cluster_colors.get(current_cluster, "gray"), alpha=0.2)

    # --- Datenlinien zeichnen ---
    axs[0].plot(df_filter['zeit'], df_filter['licht'], color='orange')
    axs[0].set_ylabel('Licht [lux]')
    axs[0].set_title('Lichtverlauf')
    if licht_limits:
        axs[0].set_ylim(licht_limits)

    axs[1].plot(df_filter['zeit'], df_filter['temperatur'], color='red')
    axs[1].set_ylabel('Temperatur [°C]')
    axs[1].set_title('Temperaturverlauf')
    if temperatur_limits:
        axs[1].set_ylim(temperatur_limits)

    axs[2].plot(df_filter['zeit'], df_filter['feuchtigkeit'], color='blue')
    axs[2].set_ylabel('Feuchtigkeit [%]')
    axs[2].set_title('Feuchtigkeitsverlauf')
    axs[2].set_xlabel('Zeit')
    if feuchtigkeit_limits:
        axs[2].set_ylim(feuchtigkeit_limits)

    # Optional: schöneres Zeitformat
    axs[2].xaxis.set_major_formatter(mdates.DateFormatter('%d.%m %H:%M'))

    plt.tight_layout()
    plt.show()

def plot_hours(df: pd.DataFrame,
                                        cluster_col: str = 'cluster',
                                        time_col: str = 'zeit',
                                        cluster_colors: dict = None,
                                        title: str = "Zeitliche Verteilung der Cluster") -> None:
    if time_col not in df.columns or cluster_col not in df.columns:
        raise ValueError("Zeit- oder Cluster-Spalte fehlt")

    df = df.copy()
    df['uhrzeit'] = df[time_col].dt.hour + df[time_col].dt.minute / 60

    unique_clusters = sorted(df[cluster_col].unique())
    palette = None
    if cluster_colors:
        # Baue eine Farbpalette in Reihenfolge der Cluster
        palette = [cluster_colors.get(cl, 'gray') for cl in unique_clusters]

    plt.figure(figsize=(10, 5))
    sns.histplot(data=df,
                 x='uhrzeit',
                 hue=cluster_col,
                 multiple='stack',
                 bins=48,
                 palette=palette,
                 edgecolor=None)

    plt.xlabel('Uhrzeit (Stunden)')
    plt.ylabel('Anzahl Datenpunkte')
    plt.title(title)
    plt.xticks(range(0, 25, 2))
    plt.tight_layout()
    plt.show()