class langolab::rabbitmq {
  rabbitmq_user { "llrmquser":
    password => "llrmqpassword",
    provider => "rabbitmqctl";
  }
  rabbitmq_vhost { "llhost":
    ensure => present,
    provider => "rabbitmqctl";
  }
  rabbitmq_user_permissions { 'llrmquser@llhost':
    configure_permission => '.*',
    read_permission      => '.*',
    write_permission     => '.*',
    provider => 'rabbitmqctl',
    require => [Rabbitmq_User['llrmquser'], Rabbitmq_Vhost['llhost']];
  }
}
