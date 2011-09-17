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
  
  file { '/etc/default/celeryd':
    ensure => "present",
    source => template("${module_name}/celeryd.erb");
  }

  file { '/etc/default/celerybeat':
    ensure => "present",
    source => template("${module_name}/celerybeat.erb");
  }

  file { '/etc/init.d/celeryd':
    require => File['/etc/default/celeryd'],
    ensure => present,
    source => 'puppet:///modules/celeryd/celeryd';
  }

  file { '/etc/init.d/celerybeat':
    require => File['/etc/default/celerybeat'],
    ensure => present,
    source => 'puppet:///modules/celeryd/celerybeat';
  }

  file { '/etc/init.d/celeryevcam':
    require => File['/etc/default/celeryevcam'],
    ensure => present,
    source => 'puppet:///modules/celeryd/celeryd';
  }

  service { "celeryd":
    require => [File['/etc/init.d/celeryd'], User['celery']],
    ensure => "running",
    hasstatus => true,
    hasrestart => true;
  }

  service { "celerybeat":
    require => [File['/etc/init.d/celerybeat'], User['celery']],
    ensure => "running",
    hasstatus => true,
    hasrestart => true;    
  }

  service { "celeryevcam":
    require => [File['/etc/init.d/celeryevcam'], User['celery']],
    ensure => "running",
    hasstatus => true,
    hasrestart => true;
  }
}
