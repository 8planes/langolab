class nodejs {
  $version = "0.4.7"
  $tar = "node-v${version}.tar.gz"

  exec { "download_node":
    cwd => "/tmp",
    path => "/usr/local/bin:/usr/bin:/bin",
    command => "wget http://nodejs.org/dist/${tar}",
    creates => "/tmp/${tar}",
    unless => "/usr/bin/test /usr/local/bin/node";
  }
  exec { "extract_node":
    cwd => "/tmp",
    path => "/usr/local/bin:/usr/bin:/bin",
    command => "tar xvf $node_tar",
    creates => "/tmp/node-v${node_ver}",
    unless => "/usr/bin/test /usr/local/bin/node",
    require => Exec["download_node"];
  }
  exec { "configure_node":
    cwd => "/tmp/node-v${version}",
    path => "/usr/local/bin:/usr/bin:/bin",
    command => "bash configure",
    creates => "/tmp/node-v${node_ver}/.lock-wscript",
    unless => "/usr/bin/test /usr/local/bin/node",
    require => Exec["extract_node"];
  }
  exec { "make_node":
    cwd => "/tmp/node-v${version}",
    path => "/usr/local/bin:/usr/bin:/bin",
    command => "make"
    creates => "/tmp/node-v${version}/build",
    unless => "/usr/bin/test /usr/local/bin/node",
    require => Exec["configure_node"];
  }
  exec { "make_install_node":
    cwd => "/tmp/node-v${version}",
    path => "/usr/local/bin:/usr/bin:/bin",
    command => "make install"
    creates => "/usr/local/bin/node",
    require => Exec["configure_node"];
  }
  exec { "install_npm":
    path => "/usr/local/bin:/usr/bin:/bin",
    command => "curl http://npmjs.org/install.sh | sudo sh",
    creates => "/usr/local/lib/node_modules/npm",
    require => Exec["make_install_node"];
  }
}
