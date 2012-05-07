class vagrantlucid64 {
  $projectdir = "/opt/langolab/"
  
  group { "puppet": ensure => "present"; } ->
  class { "langolab::packages": } ->
  class { "mongodb": } ->
  class { "redis":
    data_dir => "/opt/redis-data";
  } ->
  class { "nodejs": } ->
  class { "langolab::closure": } ->
  class { "::nginx": } ->
  nginx::vhost { "ll.example.com":
    name => "langolab",
    source => "puppet:///modules/langolab/vhost.nginx";
  }
  file { "/home/vagrant/.bashrc":
    source => "puppet:///modules/langolab/bashrc",
    owner => "vagrant",
    group => "vagrant",
    mode => "755";
  }
}

class { 'vagrantlucid64': }
