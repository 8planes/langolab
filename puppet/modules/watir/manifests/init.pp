class watir {
  package {
    "ruby": ensure => "latest";
    "ruby-dev": ensure => "latest";
    "rubygems": ensure => "latest";
    "libopenssl-ruby": ensure => "latest";
    "firefox": ensure => "latest";
    "xvfb": ensure => "latest";
  }

  package { "watir-webdriver":
    ensure => "0.3.3",
    provider => gem,
    require => [Package[ruby], Package[ruby-dev], Package[rubygems]];
  }
  
  package { "headless":
    ensure => "0.2.2",
    provider => gem,
    require => Package[watir-webdriver];
  }
  
  
  
}

