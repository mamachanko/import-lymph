Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/vivid64"

  config.vm.synced_folder ".", "/home/vagrant/lymph-talk", :nfs => true
  config.vm.network :private_network, ip: "10.11.12.13"

  # TODO: configure memory, cpus, et al.

  config.vm.provision "ansible" do |ansible|
    ansible.playbook = "provisioning/playbook.yml"
  end
end
