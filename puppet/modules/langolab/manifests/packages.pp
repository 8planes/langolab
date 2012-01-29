class langolab::packages {
  package {
    "curl": ensure => "installed";
    "openssl": ensure => "installed";
    "libcurl4-openssl-dev": ensure => "installed";
    "build-essential": ensure  => "installed";
  }
}
