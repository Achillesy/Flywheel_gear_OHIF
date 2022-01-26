from pathlib import Path
import pathvalidate as pv
import sys
import logging
import zipfile

import flywheel
import flywheel_gear_toolkit as gt

from utils import load_data as ld, import_data as id, csv_utils as cu

log = logging.getLogger()


def main(sag_file, api_key, dry_run, output_dir, destination):

    exit_status = 0

    try:
        # Initialize the flywheel client using an API-ket
        fw = flywheel.Client(api_key)

        destination = fw.get(destination["id"])
        # group = fw.get_group(destination.parents.group)
        # project = fw.get_project(destination.parents.project)

        cur_files = []
        if sag_file is None or not Path(sag_file).exists():
            cur_session = fw.get_session(destination.parents.session)
            cur_acquisitions = cur_session.acquisitions()
            for cur_acquisition in cur_acquisitions:
                for cur_file in cur_acquisition.files:
                    if cur_file.type == 'dicom':
                        cur_files.append(cur_file)
        else:
            cur_files.append(sag_file)
        
        sagzip_files = []
        for cur_file in cur_files:
            low_name = cur_file.name.lower()
            if low_name.find(".dicom.zip") > 0 and low_name.find('sag') >= 0:
                file_name = Path(cur_file.name)
                sagzip_name = file_name.stem
                sagzip_file = pv.sanitize_filename(sagzip_name)
                sagzip_files.append(sagzip_file)

        for sagzip_file in sagzip_files:
            zFile = zipfile.ZipFile("sagzip_file", "r")
            for fileM in zFile.namelist():
                zFile.extract(fileM, "/tmp/DZIP")

        # log.debug(f"destination {destination}")
        # log.debug(f'group {destination.parents.group}')
        # log.debug(f"working in project {project.label}")

        # log.debug(f'sag_file {sag_file}')
        # log.debug(f'api_key {api_key}')
        # log.debug(f'output_dir {output_dir}')

        # # We now assume that this data is being uploaded to the group/project that the gear is being run on.

        # # import the csv file as a dataframe
        # df = ld.load_text_dataframe(csv_file, first_row, delimiter)

        # # Format the data for ROI's from the data headers and upload to flywheel
        # df = id.import_data(fw, df, group, project, dry_run)

        # # Save a report
        # cu.save_df_to_csv(df, output_dir)

    except Exception as e:
        log.exception(e)
        exit_status = 1

    return exit_status


def process_gear_inputs(context):

    # First extract the configuration options
    config = context.config

    # Examine the inputs for the "api-key" token and extract it
    for inp in context.config_json["inputs"].values():
        if inp["base"] == "api-key" and inp["key"]:
            api_key = inp["key"]

    # Setup basic logging and log the configuration for this job
    if config["gear_log_level"] == "INFO":
        context.init_logging("info")
    else:
        context.init_logging("debug")
    context.log_config()

    # Get the path of the CSV file provided by the user
    sag_file = context.get_input_path("input_sag")

    # Extract the various config options from the gear's config.json file.
    # These options are created in the manifest and set by the user upon runtime.
    dry_run = config.get("dry-run", False)
    log.debug(f"dry_run is {dry_run}")

    # Check to make sure we have a valid destination container for this gear.
    destination_level = context.destination.get("type")
    if destination_level is None:
        log.error(f"invalid destination {destination_level}")
        raise Exception("Invalid gear destination")

    # Get the destination group/project
    destination = context.destination
    output_dir = context.output_dir

    return sag_file, api_key, dry_run, output_dir, destination


if __name__ == "__main__":

    (sag_file, api_key, dry_run, output_dir, destination) = process_gear_inputs(
        gt.GearToolkitContext()
    )

    result = main(sag_file, api_key, dry_run, output_dir, destination)
    sys.exit(result)
