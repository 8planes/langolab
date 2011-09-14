class activemq::package {
  exec { "activemq_download":
    path => "/usr/local/bin:/usr/bin:/bin",
    command => "wget http://apache.ziply.com//activemq/apache-activemq/5.5.0/apache-activemq-5.5.0-bin.tar.gz -O /opt/activemq.tar.gz",
    unless => "/usr/bin/test -d /opt/apache-activemq-5.5.0",
    creates => "/opt/activemq.tar.gz";
  }
  exec { "activemq_targz":
    path => "/usr/local/bin:/usr/bin:/bin",
    command => "tar xvf activemq.tar.gz",
    creates => "/opt/apache-activemq-5.5.0",
    require => Exec["activemq_download"],
    cwd => "/opt";
  }
}
