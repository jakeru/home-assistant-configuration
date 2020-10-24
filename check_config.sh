#!/bin/bash
IMAGE="homeassistant/home-assistant:0.110.0"
CONFIG_PATH=$(perl -e 'use File::Basename; use Cwd "abs_path"; print dirname(abs_path(@ARGV[0]));' -- "$0")
CMD="python -m homeassistant --script check_config --config /config"
docker run --rm --volume ${CONFIG_PATH}:/config $IMAGE $CMD
