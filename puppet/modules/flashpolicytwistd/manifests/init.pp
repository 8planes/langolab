class flashpolicytwistd {
  package {
    "python-twisted": ensure => "present";
  }

  file { "/tmp/flashpolicytwistd.deb":
    source => "puppet:///modules/flashpolicytwistd/flashpolicytwistd.deb";
  }

  package { "flashpolicytwistd":
    require => File["/tmp/flashpolicytwistd.deb"],
    provider => dpkg,
    ensure => latest,
    # for some reason puppet doesn't like using a puppet:/// location here.
    source => "/tmp/flashpolicytwistd.deb";
  }
}
