# Class: activemq::packages
#
#   ActiveMQ Packages
#
# Parameters:
#
# Actions:
#
# Requires:
#
# Sample Usage:
#
class activemq::packages (
  $version,
  $home = '/usr/share/activemq'
) {

  $version_real = $version
  $home_real    = $home

  # Manage the user and group in Puppet rather than RPM
  group { 'activemq':
    ensure => 'present',
    gid    => '92',
    before => User['activemq']
  }
  user { 'activemq':
    ensure  => 'present',
    comment => 'Apache Activemq',
    gid     => '92',
    home    => '/usr/share/activemq',
    shell   => '/bin/bash',
    uid     => '92',
    before  => Class['activemq::package'],
  }
  file { $home_real:
    ensure => directory,
    owner  => '0',
    group  => '0',
    mode   => '0755',
    before => Class['activemq::package'],
  }

  class { 'activemq::package':
    notify  => Service['activemq'],
  }

  file { '/etc/init.d/activemq':
    ensure  => link,
    target => "/opt/activemq/bin/activemq",
    owner   => '0',
    group   => '0',
    mode    => '0755',
    require => Class["activemq::package"];
  }

}
