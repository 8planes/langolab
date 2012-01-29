class redis::build($version, $bin_path) {
  $owner = 'redis'
  $group = 'redis'

  exec { "redis_download":
    cwd => "/opt",
    path => "/usr/local/bin:/usr/bin:/bin",
    command => "wget http://redis.googlecode.com/files/redis-${version}.tar.gz",
    unless => "/usr/bin/test -d /opt/redis-${version}",
    creates => "/opt/redis-${version}.tar.gz";
  }
  exec { "redis_targz":
    path => "/usr/local/bin:/usr/bin:/bin",
    command => "tar xvf redis-${version}.tar.gz",
    creates => "/opt/redis-${version}",
    require => Exec["redis_download"],
    cwd => "/opt";
  }
  exec { "redis_make":
    require => Exec["redis_targz"],
    cwd => "/opt/redis-${version}",
    path => "/usr/local/bin:/usr/bin:/bin",
    command => "make",
    creates => "/opt/redis-${version}/src/redis-server";
  } ->
  file { "${bin_path}/redis-server":
    require => Exec["redis_make"],
    ensure => "present",
    source => "/opt/redis-${version}/src/redis-server",
    owner => $owner,
    group => $group;
  } ->
  file { "${bin_path}/redis-cli":
    require => Exec["redis_make"],
    ensure => "present",
    source => "/opt/redis-${version}/src/redis-cli",
    owner => $owner,
    group => $group;
  }
}
