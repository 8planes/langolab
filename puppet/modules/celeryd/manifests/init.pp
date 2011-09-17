class celeryd($project_dir, $settings_module, $venv) {
  group { 'celery':
    ensure => "present"
  }

  user { 'celery':
    ensure => "present",
    comment => "Runs celeryd, celerybeat, celeryevcam daemons",
    shell => "/bin/bash",
    gid => "celery",
    require => Group['celery'];
  }

  file { '/var/log/celery':
    ensure => directory,
    owner => 'celery',
    group => 'celery',
    mode => '0755';
  }

  file { '/var/run/celery':
    ensure => directory,
    owner => 'celery',
    group => 'celery',
    mode => '0755';
  }
  
  file { '/etc/default/celeryd':
    ensure => file,
    owner   => '0',
    group   => '0',
    mode    => '0644',
    content => template("${module_name}/celeryd.erb");
  }

  file { '/etc/default/celerybeat':
    ensure => file,
    owner   => '0',
    group   => '0',
    mode    => '0644',
    content => template("${module_name}/celerybeat.erb");
  }

  file { '/etc/init.d/celeryd':
    require => File['/etc/default/celeryd'],
    ensure => present,
    owner   => '0',
    group   => '0',
    mode    => '0755',
    source => 'puppet:///modules/celeryd/celeryd';
  }

  file { '/etc/init.d/celerybeat':
    require => File['/etc/default/celerybeat'],
    ensure => present,
    owner   => '0',
    group   => '0',
    mode    => '0755',
    source => 'puppet:///modules/celeryd/celerybeat';
  }

  file { '/etc/init.d/celeryevcam':
    require => File['/etc/default/celeryd'],
    ensure => present,
    owner   => '0',
    group   => '0',
    mode    => '0755',
    source => 'puppet:///modules/celeryd/celeryd';
  }

  service { "celeryd":
    require => [File['/etc/init.d/celeryd'], File['/var/log/celery'], File['/var/run/celery'], User['celery']],
    ensure => "running",
    hasrestart => true;
  }

  service { "celerybeat":
    require => [Service['celeryd']],
    ensure => "running",
    hasrestart => true;    
  }

  service { "celeryevcam":
    require => [File['/etc/init.d/celeryevcam'], User['celery']],
    ensure => "running",
    hasrestart => true;
  }
}
