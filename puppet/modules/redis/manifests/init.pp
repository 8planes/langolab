class redis($data_dir="/vol/redis") {
  $version = "2.4.6"
  $bin_path = '/usr/local/bin'

  package {
    "tcl8.5" : ensure => "present";
  } ->
  user { "redis":
    ensure => "present";
  } ->
  class { "redis::build":
    version => $version,
    bin_path => $bin_path;
  } ->
  class { "redis::conf":
    data_dir => $data_dir,
    version => $version,
    bin_path => $bin_path;
  } ->
  service { "redis-server":
    ensure => running,
    enable => true,
    hasrestart => true;
  }
}
