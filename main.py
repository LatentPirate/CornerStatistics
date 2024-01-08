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
        # TODO: Maybe add floor vs ceiling deviations?
        

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