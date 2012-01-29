class watir {
  package {
    "ruby": ensure => "latest";
    "ruby-dev": ensure => "latest";
    "rubygems": ensure => "latest";
    "libopenssl-ruby": ensure => "latest";
    "firefox": ensure => "latest";
  }

  package { "watir-webdriver":
    ensure => "latest",
    provider => gem,
    require => [Package[ruby], Package[ruby-dev], Package[rubygems]];
  }
}
