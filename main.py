import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns


class PlotDrawer:
    def __init__(self):
        self.plot_folder = "plots"
        if not os.path.exists(self.plot_folder):
            os.makedirs(self.plot_folder)

    def draw_plots(self, dataframe):
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

        return paths

    def _plot_and_save(self, dataframe, title, *columns):
        # Create a pair plot for the specified columns
        plot_data = dataframe[[*columns]]
        plot = sns.pairplot(plot_data)
        plot.fig.suptitle(title, y=1.02)

        # Save the plot
        plot_path = os.path.join(self.plot_folder, f"{title.replace(' ', '_').lower()}_plot.png")
        plot.savefig(plot_path)
        plt.close()

        return plot_path

    def _plot_and_save_correlation(self, dataframe, x_column, y_column, title):
        # Create a scatter plot with regression line for correlation
        plot = sns.regplot(x=dataframe[x_column], y=dataframe[y_column])
        plot.set(title=title)

        # Save the plot
        plot_path = os.path.join(self.plot_folder, f"{title.replace(' ', '_').lower()}_plot.png")
        plot.figure.savefig(plot_path)
        plt.close()

        return plot_path


def read_and_draw_plots(json_file_path):
    # Read JSON file into a pandas dataframe
    dataframe = pd.read_json(json_file_path)

    # Create PlotDrawer instance and draw plots
    plot_drawer = PlotDrawer()
    plot_paths = plot_drawer.draw_plots(dataframe)

    return plot_paths


# Example usage:
json_file_path = 'deviation.json'
result_paths = read_and_draw_plots(json_file_path)
print("Plots saved at the following paths:")
for path in result_paths:
    print(path)
