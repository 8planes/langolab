class vagrantlucid64 {
  $projectdir = "/opt/langolab/"
  
  group { "puppet": ensure => "present"; } ->
  class { "langolab::packages": } ->
  class { "mongodb": } ->
  class { "redis":
    data_dir => "/opt/redis-data";
  } ->
  class { "nodejs": }
}

class { 'vagrantlucid64': }
