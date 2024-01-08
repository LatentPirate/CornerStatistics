import sys

import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns


class PlotDrawer:
    """
    Class for drawing statistics
    """
    def __init__(self):
        self.plot_folder = "plots"
        if not os.path.exists(self.plot_folder):
            os.makedirs(self.plot_folder)

    def draw_plots(self, dataframe: pd.DataFrame) -> list:
        """
        Draw plots for comparing different columns of dataframe
        :param dataframe: input data
        :return: list of paths to plots
        """
        paths = []

        # Plot and save for each relevant comparison
        paths.append(self._plot_and_save(dataframe, 'Ground Truth vs Model Corners', 'gt_corners', 'rb_corners'))
        paths.append(self._plot_and_save(dataframe, 'Mean Max Min Deviations', 'mean', 'max', 'min'))
        paths.append(self._plot_and_save(dataframe, 'Floor Deviations', 'floor_mean', 'floor_max', 'floor_min'))
        paths.append(self._plot_and_save(dataframe, 'Ceiling Deviations', 'ceiling_mean', 'ceiling_max', 'ceiling_min'))

        # Plot correlations between floor and ceiling values
        paths.append(self._plot_and_save_correlation(dataframe, 'floor_mean', 'ceiling_mean',
                                                     'Floor Mean vs Ceiling Mean Correlation'))
        paths.append(self._plot_and_save_correlation(dataframe, 'floor_min', 'ceiling_min',
                                                     'Floor Min vs Ceiling Min Correlation'))
        paths.append(self._plot_and_save_correlation(dataframe, 'floor_max', 'ceiling_max',
                                                     'Floor Max vs Ceiling Max Correlation'))

        # Plot correlations between gt_corners and other values
        paths.append(self._plot_and_save_bar(dataframe, 'gt_corners', 'mean', 'GT corners vs Mean Deviation '
                                                                              'Correlation'))
        paths.append(self._plot_and_save_bar(dataframe, 'gt_corners', 'floor_mean', 'GT corners vs Floor Mean '
                                                                                    'Deviation Correlation'))
        paths.append(self._plot_and_save_bar(dataframe, 'gt_corners', 'ceiling_mean', 'GT corners vs Ceiling Mean '
                                                                                      'Deviation Correlation'))

        return paths

    def _plot_and_save(self, dataframe: pd.DataFrame, title: str, *columns) -> str:
        """
        Plot pairwise relationships of specific columns from dataframe
        and save it as .png file
        :param dataframe: input dataframe
        :param title: plot title
        :param columns: columns for pairwise relationships
        :return: path to plot
        """
        # Create a pair plot for the specified columns
        plot_data = dataframe[[*columns]]
        plot = sns.pairplot(plot_data)
        plot.fig.suptitle(title, y=1.02)

        # Save the plot
        plot_path = os.path.join(self.plot_folder, f"{title.replace(' ', '_').lower()}_plot.png")
        plot.savefig(plot_path)
        plt.close()

        return plot_path

    def _plot_and_save_correlation(self, dataframe: pd.DataFrame, x_column: str, y_column: str, title: str) -> str:
        """
        Plot regression correlation x and y columns from dataframe
        and save it as .png file
        :param dataframe: input dataframe
        :param x_column: x value
        :param y_column: y value
        :param title: plot title
        :return: path to plot
        """
        # Create a scatter plot with regression line for correlation
        plot = sns.regplot(x=dataframe[x_column], y=dataframe[y_column])
        plot.set(title=title)

        # Save the plot
        plot_path = os.path.join(self.plot_folder, f"{title.replace(' ', '_').lower()}_plot.png")
        plot.figure.savefig(plot_path)
        plt.close()

        return plot_path

    def _plot_and_save_bar(self, dataframe: pd.DataFrame, x_column: str, y_column: str, title: str) -> str:
        """
        Plot statistical estimate of x and y columns from dataframe
        and save it as .png file
        :param dataframe: input dataframe
        :param x_column: x value
        :param y_column: y value
        :param title: plot title
        :return: path to plot
        """
        # Create a bar plot for the correlation
        plot = sns.barplot(x=dataframe[x_column], y=dataframe[y_column])
        plot.set(title=title)

        # Save the plot
        plot_path = os.path.join(self.plot_folder, f"{title.replace(' ', '_').lower()}_plot.png")
        plot.figure.savefig(plot_path)
        plt.close()

        return plot_path


def read_and_draw_plots(json_file_path: str) -> list:
    """
    Read json dataframe and plot relationships between
    it columns
    :param json_file_path: path to file
    :return: list of plot paths
    """
    # Read JSON file into a pandas dataframe
    dataframe = pd.read_json(json_file_path)

    # Create PlotDrawer instance and draw plots
    plot_drawer = PlotDrawer()
    plot_paths = plot_drawer.draw_plots(dataframe)

    return plot_paths


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("error: incorrect input arguments")
        print("example:")
        print("\tpython main.py path/to/deviation.json")
        sys.exit(1)
    json_file_path = sys.argv[1]
    result_paths = read_and_draw_plots(json_file_path)
    print("Plots saved at the following paths:")
    for path in result_paths:
        print(path)

