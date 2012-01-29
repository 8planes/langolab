class mongodb::apt {
  apt::source { 'mongodb':
    location    => 'http://downloads-distro.mongodb.org/repo/ubuntu-upstart',
    release     => 'dist',
    repos       => '10gen',
    include_src => false,
    key         => '7F0CEB10',
    required_packages => 'mongodb-10gen',
    key_server => "keyserver.ubuntu.com";
  }
}
