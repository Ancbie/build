#!/usr/bin/env bash
check_python3 (){
  python3=$(which python3)
  if [ -z "$python3" ]; then
    echo "Python3's missing, install by 'sudo apt install python3-full'"
    exit
  fi
  $python3 -m pip install -r requirements.txt
  if [ "$?" != "0" ];then
    echo "Failed to install required python packages."
  fi
  echo "Check pass."
}
check_python3