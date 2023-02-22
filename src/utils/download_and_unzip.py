import logging
import os
from .PPrinter import PPrinter
from src.utils.path import ASRPath, SlotFillingPath, VelocityEstimatorPath

Printer = PPrinter()

def download_and_unzip(force=False):
    #################################### Download ASR model #####################################
    ASR_path = ASRPath()
    # Check if exist exp/ folder
    if not ASR_path.exists() or force:
        Printer.log('Downloading ASR model...')
        try:
            print(ASR_path.url, ASR_path.file_path)
            os.system(f"wget -c {ASR_path.url} -P {ASR_path.folder_path}")
        except Exception as e:
            Printer.error(e)
        Printer.success('Finished downloading ASR model.')
    else:
        Printer.log(f"{ASR_path.filename} already exist, skip downloading.")
    ##################################### Download Slot Filling model ###########################
    SF_path = SlotFillingPath()
    if not SF_path.exists() or force:
        if not SF_path.downloaded_zip() or force:
            Printer.log('Downloading Slot Filling model...')
            try:
                os.system(f"wget -c {SF_path.url}")
            except Exception as e:
                Printer.error(e)
            Printer.log('Finished downloading Slot Filling model.')
        else:
            Printer.log(f"{SF_path.filename} already exist, skip downloading.")

        Printer.log('Unzipping Slot Filling model...')
        try:
            os.system(f"unzip -o -d {SF_path.folder_path} {SF_path.filename}")
        except Exception as e:
            logging.error(e)
        Printer.log('Finished unzipping Slot Filling model.')
        Printer.log('Deleting zip file.')
        os.system(f"rm {SF_path.filename}")
    else:
        Printer.log(f"Directory {SF_path.sf_bert_path} and {SF_path.sf_crf_path} already exist.")
    ##################################### Download VELOCITY estimator necessities ###########################
    estimator_path = VelocityEstimatorPath()
    if not estimator_path.exists() or force:
        if not estimator_path.downloaded_zip() or force:
            Printer.log('Downloading velocity estimator necessities...')
            try:
                os.system(f"wget -c {estimator_path.url}")
            except Exception as e:
                Printer.error(e)
            Printer.log('Finished downloading velocity estimator necessities.')
        else:
            Printer.log(f"{estimator_path.filename} already exist, skip downloading.")

        Printer.log('Unzipping velocity estimator necessities...')
        try:
            os.system(f"unzip -o -d {estimator_path.folder_path} {estimator_path.filename}")
        except Exception as e:
            logging.error(e)
        Printer.log('Finished unzipping velocity estimator necessities.')
        Printer.log('Deleting zip file.')
        os.system(f"rm {estimator_path.filename}")
    else:
        Printer.log(f"Directory {estimator_path.data_path}, {estimator_path.encoder_path} and {estimator_path.model_path} already exist.")
