#!/usr/bin/env bash
check_python3 (){
  python3=$(which python3)
  echo "[1/3]Checking Python3."
  if [ -z "$python3" ]; then
    echo "Python3's missing, install by 'sudo apt install python3-full'"
    exit 1
  fi
  echo "[2/3]Install Required Packages."
  $python3 -m pip install -r requirements.txt
  if [ "$?" != "0" ];then
    echo "Failed to install required python packages."
    exit 1
  fi
  echo "[3/3]All Done!"
}
check_python3