import argparse
import glob
import logging
import os
from pydub import AudioSegment
from tqdm import tqdm

# Constants
BITS_PER_BYTE = 8
BYTES_PER_KILOBYTE = 1024
BYTES_PER_MEGABYTE = BYTES_PER_KILOBYTE * 1024
MIN_FRAME_RATE = 1
SAFETY_FACTOR = 0.95


def configure_logging():
    """Configure the logging for the application."""
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )


def calculate_file_size_in_kb(
    frame_rate: int, bit_depth: int, channels: int, duration_sec: float
) -> float:
    """Calculate the file size of a WAV audio in kilobytes."""
    size_in_bits = frame_rate * bit_depth * channels * duration_sec
    return (size_in_bits / BITS_PER_BYTE) / BYTES_PER_KILOBYTE


def calculate_new_frame_rate(
    current_frame_rate: int, target_size_mb: float, current_size_kb: float
) -> int:
    """Calculate the new frame rate to achieve the target file size in megabytes."""
    target_size_kb = target_size_mb * BYTES_PER_MEGABYTE / BYTES_PER_KILOBYTE
    reduction_factor = target_size_kb / current_size_kb
    reduction_factor *= SAFETY_FACTOR
    return max(int(current_frame_rate * reduction_factor), MIN_FRAME_RATE)


def compress_audio_file(file_path: str, output_directory: str, target_size_mb: float):
    """Compress a WAV file to a specified size in megabytes by adjusting the sample rate."""
    try:
        audio = AudioSegment.from_file(file_path)
        duration_sec = len(audio) / 1000.0
        frame_rate, bit_depth = audio.frame_rate, audio.sample_width * 8
        channels = audio.channels

        current_size_kb = calculate_file_size_in_kb(
            frame_rate, bit_depth, channels, duration_sec
        )
        if current_size_kb <= target_size_mb * BYTES_PER_MEGABYTE / BYTES_PER_KILOBYTE:
            logging.info(f"Skipping {file_path}: File size already under target.")
            return

        new_frame_rate = calculate_new_frame_rate(
            frame_rate, target_size_mb, current_size_kb
        )
        compressed_audio = audio.set_frame_rate(new_frame_rate)
        compressed_file_path = os.path.join(
            output_directory,
            f"{os.path.splitext(os.path.basename(file_path))[0]}_compressed.wav",
        )
        compressed_audio.export(compressed_file_path, format="wav")
        logging.info(f"Compressed {file_path} to {compressed_file_path}")
    except Exception as e:
        logging.error(f"Error processing {file_path}: {e}")


def setup_arg_parser() -> argparse.ArgumentParser:
    """Set up the argument parser for command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Compress WAV files by adjusting sample rate."
    )
    parser.add_argument(
        "directory_path", type=str, help="Directory containing WAV files."
    )
    parser.add_argument(
        "target_size_mb", type=float, help="Target size for each file in megabytes."
    )
    return parser


def main():
    """Main function to process WAV files in the specified directory."""
    configure_logging()

    parser = setup_arg_parser()
    args = parser.parse_args()

    output_directory = os.path.join(args.directory_path, "Compressed_WAVs")
    os.makedirs(output_directory, exist_ok=True)

    wav_files = [
        f
        for f in glob.glob(os.path.join(args.directory_path, "*.wav"))
        if f.lower().endswith(".wav")
    ]

    with tqdm(
        total=len(wav_files), desc="Processing WAV files", unit="file", ncols=100
    ) as progress_bar:
        for file_path in wav_files:
            compress_audio_file(file_path, output_directory, args.target_size_mb)
            progress_bar.update(1)


if __name__ == "__main__":
    main()
