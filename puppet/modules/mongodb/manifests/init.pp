# Class: mongodb
#
# This class installs MongoDB (stable)
#
# Notes:
#  This class is Ubuntu specific.
#  By Sean Porter, Gastown Labs Inc.
#
# Actions:
#  - Install MongoDB using a 10gen Ubuntu repository
#  - Manage the MongoDB service
#  - MongoDB can be part of a replica set
#
# Sample Usage:
#  include mongodb
#
class mongodb {
  class { "mongodb::apt":
    notify => Service["mongodb"];
  }

  service { "mongodb":
    enable => true,
    ensure => running,
    require => Class["mongodb::apt"],
  }

  define replica_set {
    file { "/etc/init/mongodb.conf":
      content => template("mongodb/mongodb.conf.erb"),
      mode => "0644",
      notify => Service["mongodb"],
      require => Package["mongodb"],
    }
  }
}
