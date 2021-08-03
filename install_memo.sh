#!/bin/bash
# install memo
# requirements:
# tar -xvf memo_1.0.15.tar.gz
# . prepare_tar.sh [1.0.15]
# usage: . install_memo.sh [email]
# logic:
# if email then
#   launch ./memo -i email
# else
#   launch ./memo -i

# if enter a parameter set it to email
if [ -n "$1" ]; then
  #echo "$1"
  email="$1"
  #echo "<$email>"
else
  # no parameter entered please enter one or enter	
  read -p 'Please enter your email or enter for default: ' email
fi

# if parameter empty
if [ -z "${email}" ]; then
  ./memo -i -d
else
  #echo 'email exists...'
  #echo "<${email}>"
  ./memo -i -e $email -d
fi

ret=$?

#echo "<$ret>"

# check return value of memo
if [ $ret -eq 0 ];then
  crontab -l
  source ~/.bashrc
  ./memo -p
  alias memo
  echo "Successfully installed..."
elif [ $ret -eq 255 ];then
  echo "memo is already Installed..." >&2
else
  #echo $ret
  echo "Installation failed, please provide an email..." >&2
fi

