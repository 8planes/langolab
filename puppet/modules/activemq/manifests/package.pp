class activemq::package {
  exec { "activemq_download":
    path => "/usr/local/bin:/usr/bin:/bin",
    command => "wget http://apache.ziply.com//activemq/apache-activemq/5.5.0/apache-activemq-5.5.0-bin.tar.gz -o /opt/activemq.tar.gz",
    creates => "/opt/activemq.tar.gz";
  }
  exec { "activemq_targz":
    path => "/usr/local/bin:/usr/bin:/bin",
    command => "tar xvf activemq.tar.gz",
    cwd => "/opt";
  }
}
