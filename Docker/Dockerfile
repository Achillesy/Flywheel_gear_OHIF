## docker build -t ahsoka/python-rush:3.7.0 .
# FROM python:3.7
# ARG DEBIAN_FRONTEND=noninteractive
# ENV TZ=America/Chicago
# RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
# RUN apt-get -qq update && \
#     apt-get -qq -y upgrade && \
#     apt-get -qq install -y --no-install-recommends \
#     apt-utils unzip jq tree && \
#     pip install --upgrade pip && \
#     pip install flywheel-sdk flywheel_gear_toolkit \
#     numpy pandas rtstatlib pathvalidate && \
#     rm -rf /var/cache/apt/*

## docker build -t ahsoka/python-rush:3.7.12 .
FROM ahsoka/python-rush:3.7.0

ENV FLYWHEEL /flywheel/v0
RUN mkdir -p $FLYWHEEL

COPY ohifimport.py $FLYWHEEL
COPY manifest.json $FLYWHEEL
COPY run $FLYWHEEL

COPY utils/load_data.py $FLYWHEEL
COPY utils/import_data.py $FLYWHEEL
COPY utils/ROI_Template.py $FLYWHEEL
COPY utils/fwobject_utils.py $FLYWHEEL
COPY utils/csv_utils.py $FLYWHEEL