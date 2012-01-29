class rabbitmq::repo::apt {
  package { "rabbitmq-server":
    ensure => "latest";
  }
}
