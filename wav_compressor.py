# Standard Library Imports
import argparse
import glob
import logging
import logging.handlers
import multiprocessing
from multiprocessing import Manager
import os
import queue
import sys

# Third-Party Imports
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


def listener_configurer():
    """Configure the listener for logging."""
    root = logging.getLogger()
    h = logging.StreamHandler()
    f = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    h.setFormatter(f)
    root.addHandler(h)


def listener_process(queue):
    """Process that listens for logging messages."""
    listener_configurer()
    while True:
        try:
            record = queue.get()
            if record is None:
                # A None record indicates to terminate
                break
            logger = logging.getLogger(record.name)
            logger.handle(record)
            # Explicitly flush the logs
            sys.stdout.flush()
        except Exception:
            import sys, traceback

            print("Whoops! Problem:", file=sys.stderr)
            traceback.print_exc(file=sys.stderr)


def worker_configurer(queue):
    """Configure logging for each worker process."""
    h = logging.handlers.QueueHandler(queue)
    root = logging.getLogger()
    root.addHandler(h)
    root.setLevel(logging.INFO)


def compress_audio_worker(arguments):
    file_path, output_directory, target_size_mb, log_queue = arguments
    worker_configurer(log_queue)
    compress_audio_file(file_path, output_directory, target_size_mb)


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
    logging.info("Starting the audio compression application...")

    parser = setup_arg_parser()
    args = parser.parse_args()

    output_directory = os.path.join(args.directory_path, "Compressed_WAVs")
    os.makedirs(output_directory, exist_ok=True)
    logging.info(f"Output directory created at {output_directory}")

    wav_files = [
        f
        for f in glob.glob(os.path.join(args.directory_path, "*.wav"))
        if f.lower().endswith(".wav")
    ]
    logging.info(f"Found {len(wav_files)} WAV files for processing.")

    with Manager() as manager:
        log_queue = manager.Queue(-1)
        listener = multiprocessing.Process(target=listener_process, args=(log_queue,))
        listener.start()  # Start listener before processing

        # Setting up multiprocessing pool
        with multiprocessing.Pool() as pool:
            logging.info("Starting the multiprocessing pool for audio compression.")
            pool.map(
                compress_audio_worker,
                [
                    (file_path, output_directory, args.target_size_mb, log_queue)
                    for file_path in wav_files
                ],
            )

        # Clean up
        log_queue.put_nowait(None)
        listener.join()

        logging.info("Audio compression completed.")


if __name__ == "__main__":
    main()
