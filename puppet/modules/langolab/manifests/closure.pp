class langolab::closure {
  # happens to be the latest revision as of 10/24/2011
  $revision = 1376
  $svn_repo = 'http://closure-library.googlecode.com/svn/trunk/'
  $local_closure_dir = '/opt/google-closure'

  exec { "svn_checkout_closure":
    require => Package['subversion'],
    path => "/usr/local/bin:/usr/bin:/bin",
    command => "svn checkout -r ${revision} ${svn_repo} ${local_closure_dir}";
  }
}
