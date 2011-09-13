class flashpolicytwistd {
  package {
    "python-twisted": ensure => "present";
  }

  package { "flashpolicytwistd":
    provider => dpkg,
    ensure => latest,
    source => "puppet:///modules/flashpolicytwistd/flashpolicytwistd.deb";
  }
}
