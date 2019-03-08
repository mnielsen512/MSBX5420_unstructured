#!/usr/bin/env bash
CURR_DIR=/home/vagrant/work/week6_2/cwl-data/data/structured
NEW_DIR=/home/vagrant/work/week7/cwlData_2

for f in structured-2018*.tar.gz;
do
  tar -zxvf "${f}" -C  "$NEW_DIR"
  cd "$CURR_DIR"
done

echo ALL DONE
