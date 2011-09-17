class langolab::closure($project_dir) {
  $current_revision = 1196
  $svn_repo = 'http://closure-library.googlecode.com/svn/trunk/'
  $local_dir = '/opt/google-closure'
  
  package { "subversion":
    ensure => "installed";
  }
  exec { "svn_checkout_closure":
    require => Package['subversion'],
    path => "/usr/local/bin:/usr/bin:/bin",
    command => "svn checkout -r ${current_revision} ${svn_repo} ${local_dir}";
  }
  file { "${project_dir}media/js/closure":
    require => Exec["svn_checkout_closure"],
    ensure => link,
    target => "${local_dir}/closure";
  }
}
