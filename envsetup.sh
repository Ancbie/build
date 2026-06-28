#!/usr/bin/env bash
check_python3 (){
  python3=$(which python3)
  all_done=0
  echo "[1/3]Checking Python3."
  if [ -z "$python3" ]; then
    echo "Python3's missing, install by 'sudo apt install python3-full'"
    sudo apt install python3-full
    all_done=$?
  fi
  echo "[2/3]Install Required Packages."
  $python3 -m pip install -r requirements.txt
  if [ "$?" != "0" ];then
    echo "Failed to install required python packages."
    all_done=1
  fi
  if [ "$all_done" != 0 ];then
    echo "[Error]Something went wrong!"
  else
    echo "[3/3]All Done!"
  fi
}
check_python3