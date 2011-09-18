Vagrant::Config.run do |config|
  config.vm.host_name = "langolab"
  config.vm.box = "lucid64"
  config.vm.box_url = "http://files.vagrantup.com/lucid64.box"

  config.vm.forward_port "http", 8000, 8000
  config.vm.forward_port "stomp", 61613, 61613
  config.vm.forward_port "activemq console", 8161, 8161

  config.vm.share_folder "project", "/opt/langolab", "."

  config.vm.provision :puppet do |puppet|
    puppet.manifests_path = "puppet"
    puppet.module_path = "puppet/modules"
    puppet.manifest_file  = "vagrantlucid64.pp"
    puppet.options = "--verbose --debug"
  end
end
