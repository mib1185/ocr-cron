#!/usr/bin/python3
import argparse
import logging
from datetime import datetime
from os import listdir, remove, stat
from os.path import exists, isfile, join
from pytesseract import image_to_pdf_or_hocr
from time import sleep

argparser = argparse.ArgumentParser(description="Read files from INPUTDIR, generate searchable PDF and store in OUTPUTDIR")
argparser.add_argument("-i", "--inputdir", required=True, type=str, help="input directory where to search for files")
argparser.add_argument("-o", "--outputdir", required=True, type=str, help="output directory where to store processed files")
argparser.add_argument("-d", "--deletesource", action='store_true', help="delete source file, after processing (default: false)", default=False)
argparser.add_argument("-l", "--language", type=str, help="language string for tesseract (default: deu+eng)", default="deu+eng")
argparser.add_argument("--wait-file-finished", type=int, help="seconds to wait for file changes to consider input file is complete (default: 5)", default="5")
argparser.add_argument("--lockfile", type=str, help="lockfile (default: /tmp/ocr-cron.lock)", default="/tmp/ocr-cron.lock")
argparser.add_argument("--logfile", type=str, help="logfile (default: /var/log/ocr-cron.log)", default="/var/log/ocr-cron.log")
args = argparser.parse_args()

filestoprocess = [f for f in listdir(args.inputdir) if isfile(join(args.inputdir,f))]

def _log(*msg,level=logging.INFO,printout=True):
    if printout:
        print(*msg)
    
    logging.basicConfig(filename=args.logfile, level=logging.INFO)
    logmsg = "%s %s" % (str(datetime.now()), str(*msg))

    if level == logging.DEBUG:
        logging.debug(logmsg)
    if level == logging.INFO:
        logging.info(logmsg)
    if level == logging.WARN:
        logging.warn(logmsg)
    if level == logging.ERROR:
        logging.error(logmsg)
    if level == logging.CRITICAL:
        logging.critical(logmsg)

def _wait_file_finished(file):
    filename_in = join(args.inputdir,file)
    file_time_old = stat(filename_in).st_ctime
    while True:
        sleep(args.wait_file_finished)
        file_time_new = stat(filename_in).st_ctime
        if file_time_new > file_time_old:
            _log("%s wait for file ..." % file)
            file_time_old = file_time_new
        else:
            break

def process(file):
    filename_in = join(args.inputdir,file)
    filename_out = "%s.pdf" % join(args.outputdir,file)
    _log("%s start ..." % file)
    _wait_file_finished(file)
    pdf = image_to_pdf_or_hocr(
        filename_in,
        lang=args.language,
        extension='pdf')
    with open(filename_out, "w+b") as outfile:
        outfile.write(pdf)
    if args.deletesource:
        remove(filename_in)
        _log("%s deleted ..." % file)
    _log("%s finished ..." % file)

if __name__ == "__main__":

    # lockfile handling
    if exists(args.lockfile):
        _log("already running (lockfile %s found)" % args.lockfile, level=logging.WARN)
        exit(1)
    else:
        open(args.lockfile, "a").close()

    # main loop
    _log("started with arguments: %s" % vars(args))
    for file in filestoprocess:
        process(file)

    # lockfile handling
    remove(args.lockfile)
