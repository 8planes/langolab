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
}

class { 'vagrantlucid64': }
