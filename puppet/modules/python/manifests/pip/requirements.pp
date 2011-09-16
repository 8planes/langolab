# Installs packages in a requirements file for a virtualenv.
# Pip tries to upgrade packages when the requirements file changes.
define python::pip::requirements($venv, $cwd, $owner=undef, $group=undef) {
  $requirements = $name
  $checksum = "$venv/requirements.checksum"
  
  Exec {
    user => $owner,
    group => $group,
    cwd => "/tmp",
  }
  
  file { $requirements:
    ensure => present,
    replace => false,
    owner => $owner,
    group => $group,
    content => "# Puppet will install packages listed here and update them if
    # the the contents of this file changes.",
  }
  
  # We create a sha1 checksum of the requirements file so that
  # we can detect when it changes:
  exec { "create new checksum of $name requirements":
    path => "/usr/local/bin:/usr/bin:/bin",
    command => "sha1sum $requirements > $checksum",
    unless => "sha1sum -c $checksum",
    require => File[$requirements],
  }
  
  exec { "update $name requirements":
    command => "$venv/bin/pip install -Ur $requirements",
    cwd => $cwd,
    subscribe => Exec["create new checksum of $name requirements"],
    logoutput => true,
    timeout => 0,
    refreshonly => true;
  }
}
