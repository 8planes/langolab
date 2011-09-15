class flashpolicytwistd($domain = "*") {
  package {
    "python-twisted": ensure => "present";
  }

  file { "/tmp/flashpolicytwistd.deb":
    ensure => file,
    source => "puppet:///modules/flashpolicytwistd/flashpolicytwistd.deb";
  }

  package { "flashpolicytwistd":
    require => File["/tmp/flashpolicytwistd.deb"],
    provider => dpkg,
    ensure => present,
    # for some reason puppet doesn't like using a puppet:/// location here.
    source => "/tmp/flashpolicytwistd.deb";
  }

  file { "/etc/flashpolicy.xml":
    ensure => file,
    owner => '0',
    group => '0',
    content => template("${module_name}/flashpolicy.xml.erb");
  }

  service { "flashpolicytwistd":
    require => [Package["flashpolicytwistd"], File["/etc/flashpolicy.xml"]],
    ensure => "running";
  }
}
