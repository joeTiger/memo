crontab -l
./memo -p -d
./memo -r -d
./memo -k -d
source ~/.bashrc
unalias memo
echo 'crontab -l'
crontab -l

