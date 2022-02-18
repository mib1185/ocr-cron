#!/usr/bin/python3
import argparse
import logging
import sys
import imutils
import cv2
from PIL import Image
from os import listdir, remove, stat
from os.path import exists, isfile, join
from pytesseract import image_to_pdf_or_hocr, image_to_osd, Output
from time import sleep

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)
LOGGER.addHandler(logging.StreamHandler(sys.stdout))

argparser = argparse.ArgumentParser(
    description="Read files from INPUTDIR, generate searchable PDF and store in OUTPUTDIR"
)
argparser.add_argument(
    "-i",
    "--inputdir",
    required=True,
    type=str,
    help="input directory where to search for files",
)
argparser.add_argument(
    "-o",
    "--outputdir",
    required=True,
    type=str,
    help="output directory where to store processed files",
)
argparser.add_argument(
    "-d",
    "--deletesource",
    action="store_true",
    help="delete source file, after processing (default: false)",
    default=False,
)
argparser.add_argument(
    "-l",
    "--language",
    type=str,
    help="language string for tesseract (default: deu+eng)",
    default="deu+eng",
)
argparser.add_argument(
    "--wait-file-finished",
    type=int,
    help="seconds to wait for file changes to consider input file is complete (default: 5)",
    default="5",
)
args = argparser.parse_args()


def _wait_file_finished(file):
    filename_in = join(args.inputdir, file)
    file_time_old = stat(filename_in).st_ctime
    while True:
        sleep(args.wait_file_finished)
        file_time_new = stat(filename_in).st_ctime
        if file_time_new > file_time_old:
            LOGGER.info("%s wait for file ..." % file)
            file_time_old = file_time_new
        else:
            break


def process(file):
    filename_in = join(args.inputdir, file)
    filename_out = f"{join(args.outputdir, file)}.pdf"

    if exists(filename_out):
        LOGGER.info(
            f"{file}: ignored, since outfile '{filename_out}' already exists ..."
        )
        return

    LOGGER.info("-" * 40)
    LOGGER.info(f"{file}: wait to be finished ...")
    _wait_file_finished(file)

    LOGGER.info(f"{file}: check and correct orientation")
    image_orig = cv2.imread(filename_in)
    osd_results = image_to_osd(image_orig, output_type=Output.DICT)
    image_rotated = imutils.rotate_bound(image_orig, angle=osd_results["rotate"])

    LOGGER.info(f"{file}: detected orientation: {osd_results['orientation']}")
    LOGGER.info(f"{file}: rotate by {osd_results['rotate']} degrees to correct")
    LOGGER.info(f"{file}: detected script: {osd_results['script']}")

    LOGGER.info(f"{file}: start ocr and write to {filename_out}")
    pdf = image_to_pdf_or_hocr(
        Image.fromarray(image_rotated), lang=args.language, extension="pdf"
    )
    with open(filename_out, "w+b") as outfile:
        outfile.write(pdf)
    if args.deletesource:
        remove(filename_in)
        LOGGER.info(f"{file}: deleted ...")
    LOGGER.info(f"{file}: finished ...")


if __name__ == "__main__":
    LOGGER.info("started with arguments: %s" % vars(args))
    while True:
        files = [f for f in listdir(args.inputdir) if isfile(join(args.inputdir, f))]
        LOGGER.info(f"files found to process: {files}")
        for file in files:
            process(file)

        # wait 5 min
        sleep(600)
