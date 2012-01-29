class python {
  package {
    "build-essential": ensure => "latest";
    "python": ensure => "2.6.5-0ubuntu1";
    "python-dev": ensure => "2.6.5-0ubuntu1";
    "python-setuptools": ensure => "latest";
    "python-imaging": ensure => "installed";
    "python-memcache": ensure => "installed";
    "python-virtualenv": ensure => "installed";
  }
  exec { "easy_install pip":
    path => "/usr/local/bin:/usr/bin:/bin",
    refreshonly => true,
    require => Package["python-setuptools"],
    subscribe => Package["python-setuptools"],
  }
}
