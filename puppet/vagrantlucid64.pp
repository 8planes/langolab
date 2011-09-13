class vagrantlucid64 {
  $projectdir = "/opt/langolab/"
  $venv = "${projectdir}venv"
  
  group { "puppet": ensure => "present"; } ->
  class { 'aptitude': } ->
  class { 'watir': } ->
  class { 'python': } ->
  python::venv { "langolabvenv": path => $venv }
}

class { 'vagrantlucid64': }
