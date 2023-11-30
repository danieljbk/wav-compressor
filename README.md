
# WAV Compressor

## Overview

`wav_compressor.py` is a Python script for compressing WAV audio files to a specific target size in megabytes. It is designed to iterate over all WAV files in a given directory, calculate the optimal frame rate for compression, and adjust the sample rate of each file to reach the desired file size. This tool aims to reduce the file size effectively while maintaining a balance between space efficiency and audio quality.

## Features

- **Automated File Processing**: Processes all WAV files in a given directory.
- **Dynamic Frame Rate Calculation**: Calculates the new frame rate to meet the target size.
- **Size Control**: Compresses files to a specified target size in megabytes.
- **Enhanced Modularity and Readability**: Refactored to follow industry standards and best practices for Python code.

## Prerequisites

Ensure you have the following installed:

- **Python**: Required for running the script.
- **FFmpeg**: Used by Pydub for audio processing. Installation for Mac using Homebrew:

  ```bash
  brew install ffmpeg
  ```

## Installation

1. Clone or download the repository to your local machine.
2. Navigate to the script directory.
3. Install the required Python libraries. A `requirements.txt` file is provided for easy installation of dependencies. Run the following command:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Place your WAV files in a specified directory.
2. Run the script from the command line, specifying the path to the directory containing the WAV files and the target size in MB. For example:

   ```bash
   python wav_compressor.py /path/to/directory 100
   ```

   This command will process all WAV files in the specified directory, compressing them to a target size of 100 MB each.

## Important Notes

- **File Format**: Supports WAV files for input and outputs the compressed files in WAV format.
- **Backup Your Files**: Keep a backup of your original files.
- **Quality vs. Size**: As the compression changes the frame rate, there may be a trade-off between audio quality and file size.
- **Error Handling**: Includes error handling for common issues, but ensure correct file paths and formats are used.

## Customization

The script can be customized for different target sizes or modified for other audio formats. Adjust the script parameters as needed.

## License

This tool is open-source and free to use. Feel free to modify and distribute it according to your needs.

---

For any issues or suggestions regarding the tool, please feel free to open an issue in the repository or submit a pull request with your changes.
