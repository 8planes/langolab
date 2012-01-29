# Class: activemq::config
#
#   class description goes here.
#
# Parameters:
#
# Actions:
#
# Requires:
#
# Sample Usage:
#
class activemq::config (
  $server_config,
  $path = '/etc/default/activemq.xml'
) {

  $path_real = $path

  $server_config_real = $server_config

  # Resource defaults
  File {
    owner   => 'activemq',
    group   => 'activemq',
    mode    => '0644',
    notify  => Service['activemq'],
    require => Class['activemq::package'],
  }

  file { "/etc/default":
    ensure => directory;
  }

  # The configuration file itself.
  file { 'activemq.xml':
    ensure => file,
    path    => $path_real,
    owner   => '0',
    group   => '0',
    require => File["/etc/default"],
    content => $server_config_real,
  }

}
