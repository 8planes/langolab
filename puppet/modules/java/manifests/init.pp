# Class: java
#
# This module manages the Java runtime package
#
# Parameters:
#
# Actions:
#
# Requires:
#
# Sample Usage:
#
# [Remember: No empty lines between comments and class definition]
class java(
  $distribution = 'jdk',
  $version      = 'installed'
  ) {

  $distribution_debian = $distribution ? {
    jdk => 'sun-java6-jdk',
    jre => 'sun-java6-jre',
  }
  class { 'java::package_debian':
    version      => $version,
    distribution => $distribution_debian;
  }  
}
