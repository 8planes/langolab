class redis::conf($data_dir, $version, $bin_path) {
  $redis_timeout = 0
  $owner = 'redis'
  $group = 'redis'

  file { $data_dir:
    ensure => "directory",
    owner => $owner,
    group => $group;
  }
  file { "/etc/init.d/redis-server":
    content => template("${module_name}/redis-server.erb"),
    owner => root,
    group => root,
    mode => 744,
    notify => Service["redis-server"];
  }
  file { "/etc/redis.conf":
    ensure => present,
    content => template("${module_name}/redis.conf.erb"),
    notify => Service["redis-server"];
  }
}
