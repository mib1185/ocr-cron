# ocr-cron

Read files from INPUTDIR, generate searchable PDF and store in OUTPUTDIR

## options

```
usage: main.py [-h] -i INPUTDIR -o OUTPUTDIR [-d] [-l LANGUAGE]
               [--wait-file-finished WAIT_FILE_FINISHED] [--lockfile LOCKFILE]
               [--logfile LOGFILE]

Read files from INPUTDIR, generate searchable PDF and store in OUTPUTDIR

optional arguments:
  -h, --help            show this help message and exit
  -i INPUTDIR, --inputdir INPUTDIR
                        input directory where to search for files
  -o OUTPUTDIR, --outputdir OUTPUTDIR
                        output directory where to store processed files
  -d, --deletesource    delete source file, after processing (default: false)
  -l LANGUAGE, --language LANGUAGE
                        language string for tesseract (default: deu+eng)
  --wait-file-finished WAIT_FILE_FINISHED
                        seconds to wait for file changes to consider input
                        file is complete (default: 5)
  --lockfile LOCKFILE   lockfile (default: /tmp/ocr-cron.lock)
  --logfile LOGFILE     logfile (default: /var/log/ocr-cron.log)
```

## crontab example

```
# m h  dom mon dow   command
*/5 * * * * /usr/bin/python3 /root/ocr-cron/main.py -i <input-dir> -o <output-dir> -d
```
