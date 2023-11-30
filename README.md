
# WAV Compressor

## Overview

The WAV Compressor is a Python tool for reducing the size of WAV audio files. It achieves this by adjusting the sample rate of the files, aiming to compress them to a specific size in megabytes (MB).

## Features

- **Sample Rate Adjustment**: Modifies the sample rate to reduce file size.
- **Multiprocessing**: Uses Python's `multiprocessing` for faster processing.
- **Logging**: Provides basic logging for tracking the compression process.
- **Command-Line Interface**: Allows users to specify the directory and target file size via command line.

## Prerequisites and Installation

To set up the WAV Compressor, follow these steps:

1. **Python 3.x**: Required to run the tool. [Download Python 3.x](https://www.python.org/downloads/).

2. **FFmpeg**: Necessary for audio file processing. Install FFmpeg on macOS with:

   ```bash
   brew install ffmpeg
   ```

   On other systems, follow the respective installation instructions.

3. **Setup**: Download or clone the WAV Compressor repository.

4. **Install Dependencies**: In the tool's folder, run:

   ```bash
   pip install -r requirements.txt
   ```

   to install the necessary Python packages.

## Usage

Run the script in the command line, specifying the directory of WAV files and the target size in megabytes:

```bash
python wav_compressor.py <directory_path> <target_size_mb>
```

Example:

```bash
python wav_compressor.py /path/to/wav/files 5
```

## Command-Line Arguments

- `directory_path`: The directory with WAV files.
- `target_size_mb`: Desired size for the compressed files in megabytes.

## Functionality

- `main()`: Starts the compression process.
- `compress_audio_file()`: Handles the compression of each WAV file.
- `calculate_file_size_in_kb()`: Computes the initial size of the file.
- `calculate_new_frame_rate()`: Determines the new frame rate for the target file size.

## Logging and Multiprocessing

- Basic logging setup to monitor the process.
- Multiprocessing to handle multiple files simultaneously.

## Error Handling

Includes basic error handling to catch and log issues during compression.

## Output

Compressed files are saved in a `Compressed_WAVs` folder in the specified directory.

## Limitations

- Only supports WAV files.
- Compression is done by changing the sample rate, which may affect sound quality.

## License

This is an open-source tool, free for personal and commercial use.

## Contributions

Feel free to contribute or suggest improvements via the project's repository.
