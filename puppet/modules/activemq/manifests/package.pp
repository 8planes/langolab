class activemq::package {
  exec { "activemq_download":
    path => "/usr/local/bin:/usr/bin:/bin",
    command => "wget http://apache.ziply.com//activemq/apache-activemq/5.5.0/apache-activemq-5.5.0-bin.tar.gz -O /opt/activemq.tar.gz",
    unless => "/usr/bin/test -d /opt/activemq/bin",
    creates => "/opt/activemq.tar.gz";
  }
  file { "/opt/activemq":
    ensure => "directory"
  }
  exec { "activemq_targz":
    path => "/usr/local/bin:/usr/bin:/bin",
    command => "tar --extract --file=activemq.tar.gz --strip-components=1 --directory=/opt/activemq",
    creates => "/opt/activemq/bin",
    require => [Exec["activemq_download"], File["/opt/activemq"]],
    cwd => "/opt";
  }
}
