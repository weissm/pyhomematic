sudo sed -i /boot/cmdline.txt -e "s/console=serial0,[0-9]\+ //"
sudo sed -i /boot/cmdline.txt -e "s/console=ttyAMA0,[0-9]\+ //"
sudo bash -c 'cat << EOT > /etc/network/interfaces
source-directory /etc/network/interfaces.d
auto lo
iface lo inet loopback
iface eth0 inet manual
auto br0
iface br0 inet dhcp
  bridge_ports eth0
EOT'
sudo systemctl restart pivccu.service
ssh root@192.168.10.22
sudo vi /etc/piVCCU3/lxc.config
sudo systemctl restart pivccu.service
ssh root@192.168.10.22
sudo dpkg-reconfigure pivccu3
vi /lib/systemd/system/pivccu.service
vi /lib/systemd/system/monitor-hb-rf-eth.service

git fetch upstream dev # to pull the latest changes into a local dev branch
git rebase upstream/dev # to put those changes into your feature branch before your changes
git rebase -i devel
git rebase --continue
git rebase --abort
git remote add devel https://github.com/danielperna84/pyhomematic.git
git clone git@github.com:weissm/pyhomematic.git
git remote add upstream https://github.com/danielperna84/pyhomematic.git
git rebase -i HEAD~1
git fetch upstream devel # to pull the latest changes into a local dev branch
git rebase -i upstream/devel
vi pyhomematic/_hm.py
git branch -d homeassistant/improve/cover
git branch -D homeassistant/improve/cover
git push origin --delete homeassistant/improve/cover
git checkout -b homeassistant/improve/cover
git push origin homeassistant/improve/cover
git cherry-pick 33d5b53
git cherry-pick a23b45f
git fetch upstream master # to pull the latest changes into a local dev branch
git rebase upstream/master # to put those changes into your feature branch before your changes
git status
git branch -d dev
git branch -D dev
git checkout dev
git checkout --track origin/dev
git branch
git push
git branch master

python3 -m debugpy --listen 0.0.0.0:5678 --wait-for-client manual_test.py -r ccu3-webui -rp 2010 -a 001658A99FD725 -c 6 -u PmaticAdmin -p EPIC-SECRET-PW -to
python3 -m debugpy --listen 0.0.0.0:5678 --wait-for-client manual_test.py -r ccu3-webui -rp 2010 -a 00085A499BE380 -u PmaticAdmin -p EPIC-SECRET-PW -c 1 -to -s 0
python3 -m debugpy --listen 0.0.0.0:5678 --wait-for-client manual_test.py -r ccu3-webui -rp 2010 -a 001858A996BB80 -u PmaticAdmin -p EPIC-SECRET-PW
python3 -m debugpy --listen 0.0.0.0:5678 --wait-for-client manual_test.py -r ccu3-webui -rp 8701 -a CUX2801006 -c 1 -u PmaticAdmin -p EPIC-SECRET-PW


