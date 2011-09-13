class watir {
  package {
    "ruby": ensure => "latest";
    "rubygems": ensure => "latest";
  }

  package { "watir-webdriver":
    ensure => "latest",
    provider => gem,
    require => Package["ruby"];
  }
}
