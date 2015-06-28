Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/vivid64"
  config.vm.synced_folder ".", "/home/vagrant/lymph-talk"

  # TODO: configure memory, cpus, et al.

  config.vm.provision "ansible" do |ansible|
    ansible.playbook = "playbook.yml"
  end
end
