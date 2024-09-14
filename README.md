# Lyra

Lyra is a post-processing Python package developed for the University of Massachusetts Hirshfield Dowd Observatory. It is designed for the analysis and visualization of raw astronomical light curve data. The package is named after the first collection of scientific data gathered on a full period of a variable star in the constellation Lyra during the summer of 2024.

## Description

Lyra provides tools to process and analyze photometric data from astronomical observations. It is intended to be used directly after the photometric analysis performed by the AstroimageJ program, offering advanced capabilities for data analysis and visualization.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Command-Line Interface](#command-line-interface)
- [Contributing](#contributing)
- [License](#license)
- [Authors](#authors)
- [Contact](#contact)
- [Changelog](#changelog)

## Installation

You can install Lyra using either the wheel file or the source archive.

### Using Wheel File
1. **Ensure Python is installed**:
   - Python 3.x is required. Verify your Python version with:
     ```bash
     python --version
     ```

2. **Install using pip**:
   - Run the following command to install from the wheel file:
     ```bash
     pip install lyra-1.0-py3-none-any.whl
     ```

### Using Source Archive
1. **Ensure Python and pip are installed**:
   - Verify Python and pip are installed and updated:
     ```bash
     python --version
     pip --version
     ```

2. **Install from the source archive**:
   - Download the `lyra-1.0.tar.gz` file if you haven't already.
   - Install the package using pip:
     ```bash
     pip install lyra-1.0.tar.gz
     ```
   - Or in the Lyra download folder (unzipped):
     ```bash
     pip install .
     ```

3. **Alternative Installation via Source Code**:
   - If you have the source code and `setup.py`, you can install Lyra with:
     ```bash
     python setup.py install
     ```

## Usage

Here's a quick guide on how to use Lyra for analyzing and visualizing your astronomical data.

### Importing the Package

```python
from lyra.core import process_dfs, norm
from lyra.plot import plot_lightcurve
from lyra.data import load_data, clean_data, aavso_conv

```
Or import the entire package as:

```python
import lyra as ly
```

### Example Workflow

1. **Load and Clean Data**

```python
data = ly.load_data('datafile.csv')
cleaned_data = ly.clean_data(data)
```

2. **Process Data**

The `process_dfs` function processes multiple DataFrames, normalizing the BJD time column and returning processed data:

```python
dataframes = [('file1.csv', 'label1'), ('file2.csv', 'label2')]
period = 0.1
processed_data = ly.process_dfs(dataframes, period, clean=True)
```

3. **Plot Data**

```python
ly.plot_lightcurve(processed_data)
```

## Command-Line Interface

Lyra includes a command-line interface (CLI) for processing and visualizing data. To use the CLI, run the following command:

```bash
lyra <files> [-l <labels>] [-t <title>] [-p <period>] [-c]
```

- `<files>`: Data files to process.
- `-l <labels>`: Labels for each data file (must match the number of files).
- `-t <title>`: Title for the plot (default is "Partial Lightcurve").
- `-p <period>`: Period of orbit (default is 1.0).
- `-c`: Perform data cleaning.

**Example**:

```bash
lyra datafile1.csv datafile2.csv -l label1 label2 -t "Lightcurve Analysis" -p 0.1 -c
```

## Features

- **Data Processing**: Normalize and process multiple DataFrames.
- **Data Loading and Cleaning**: Load data from CSV or Excel files and clean datasets.
- **Visualization**: Plot light curves with various customization options.

## Contributing

Contributions to Lyra are welcome! To contribute, please fork the repository, make your changes, and submit a pull request. For detailed guidelines, please refer to the `CONTRIBUTING.md` file.

## License

Lyra is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.

## Authors

- **Zachary Pereira**: [zacharypereira14@gmail.com](mailto:zacharypereira14@gmail.com)

## Contact

For any questions or issues, please contact Zachary Pereira at [zacharypereira14@gmail.com](mailto:zacharypereira14@gmail.com).


## Changelog

**1.0 (2024-09-14)**  
- Initial release with data processing, cleaning, normalization, and plotting functionalities.
- GUI in version 1

---

Feel free to adjust any sections or add additional details as needed. Let me know if there's anything else you'd like to include or modify!

