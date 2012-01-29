class langolab::activemq($stomp_debug = false) {
  class { "activemq::packages":
    version => "present";
  }
  class { "activemq::config":
    require => Class["activemq::packages"],
    notify  => Class['activemq::service'],
    path => "/opt/activemq/conf/activemq.xml",
    server_config => template("${module_name}/activemq.xml.erb");
  }
  file { "/var/log/activemq":
    ensure => directory,
    owner => "activemq",
    group => "activemq",
    mode => "0755";
  }
  file { "log4j.properties":
    require => [File["/var/log/activemq"], Class["activemq::config"]],
    notify  => Class['activemq::service'],
    ensure => file,
    path    => "/opt/activemq/conf/log4j.properties",
    owner   => '0',
    group   => '0',
    content => template("${module_name}/activemqlog4j.properties.erb");
  }
  class { "activemq::service":
    ensure => "running",
    require => [Class["activemq::config"], File["log4j.properties"]];
  }
}
