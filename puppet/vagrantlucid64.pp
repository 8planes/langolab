class vagrantlucid64 {
  $projectdir = "/opt/langolab/"
  $venv = "${projectdir}venv"
  
  group { "puppet": ensure => "present"; } ->
  class { 'aptitude': } ->
  class { 'java': } ->
  class { 'activemq': } ->
  class { 'rabbitmq::server': } ->
  class { 'langolab::rabbitmq': } ->
  class { 'python': } ->
  python::venv { "langolabvenv": path => $venv } ->
  class { 'langolab::closure': project_dir => "${projectdir}web/" } ->
  class { 'langolab::pip': venv => $venv, projectdir => $projectdir } 
  class { 'langolab::db': } ->
  class { 'celeryd':
    project_dir => "${projectdir}web/",
    settings_module => "settings",
    venv => $venv;
  }
}

class { 'vagrantlucid64': }
