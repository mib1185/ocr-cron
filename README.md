# ocr-cron

Read files from INPUTDIR, generate searchable PDF and store in OUTPUTDIR

## installation

#### clone repository

```
git clone https://github.com/mib1185/ocr-cron.git
```

#### change into directory

```
cd ocr-cron
```

#### install dependencies

```
pip install -r requirements.txt
```

#### add cronjob
example `crontab` entry
```
# m h  dom mon dow   command
*/5 * * * * /usr/bin/python3 /root/ocr-cron/main.py -i <input-dir> -o <output-dir> -d
```

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
