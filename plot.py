import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

def plot_lightcurve(processed_data, figsize=(10, 6), invert_yaxis=True,
                    ylabel='Magnitude (V)', xlabel='Phase', title='Partial Lightcurve',
                    xlim=(0.0, 1.0), xformatter=lambda x, _: '{:.2f}'.format(x),
                    grid=True, error_bars=False):
    """
    Plot light curves from processed data.

    Parameters:
    processed_data (list): List of tuples containing (processed DataFrame, first BJD_normalized value, last BJD_normalized value, label_str).
    figsize (tuple, optional): Figure size (width, height). Default is (10, 6).
    invert_yaxis (bool, optional): Whether to invert the y-axis. Default is True.
    ylabel (str, optional): Y-axis label. Default is 'Magnitude (V)'.
    xlabel (str, optional): X-axis label. Default is 'Phase'.
    title (str, optional): Plot title. Default is 'Partial Lightcurve'.
    xlim (tuple, optional): X-axis limits (min, max). Default is (0.0, 1.0).
    xformatter (function, optional): Formatter function for x-axis ticks. Default formats to two decimal places.
    grid (bool, optional): Whether to show grid lines. Default is True.
    error_bars (bool, optional): Whether to plot error bars using 'Source_AMag_Err_T1' column. Default is False.

    Raises:
    ValueError: If 'Source_AMag_T1' column is missing in any processed DataFrame.
    KeyError: If 'Source_AMag_Err_T1' column is requested for error bars but is missing in any processed DataFrame.
    """
    plt.figure(figsize=figsize)

    try:
        for idx, (df, _, _, label) in enumerate(processed_data):
            if 'Source_AMag_T1' not in df.columns:
                raise ValueError("Missing 'Source_AMag_T1' column in DataFrame.")

            if error_bars and 'Source_AMag_Err_T1' not in df.columns:
                raise KeyError("Missing 'Source_AMag_Err_T1' column for error bars.")

            if error_bars:
                plt.errorbar(df['BJD_normalized'], df['Source_AMag_T1'], yerr=df['Source_AMag_Err_T1'],
                             marker='.', linestyle='None', markersize=5, capsize=3, label=label)
            else:
                plt.plot(df['BJD_normalized'], df['Source_AMag_T1'], marker='.', linestyle='None', markersize=5, label=label)

        if invert_yaxis:
            plt.gca().invert_yaxis()

        plt.ylabel(ylabel, fontsize=14)
        plt.xlabel(xlabel, labelpad=15, fontsize=14)
        plt.title(title, fontsize=14)
        plt.xlim(*xlim)
        plt.gca().xaxis.set_major_formatter(ticker.FuncFormatter(xformatter))

        plt.legend()  # Automatically uses labels from each plot

        if grid:
            plt.grid(True)

        plt.tight_layout()
        plt.show()

    except ValueError as ve:
        print(f"ValueError: {ve}")

    except KeyError as ke:
        print(f"KeyError: {ke}")

    except Exception as e:
        print(f"Error plotting lightcurve: {e}")
