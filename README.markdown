To set up your local dev environment:

1. Git clone the repo:

        git clone git@github.com:8planes/langolab.git

    Now the entire project will be in the langolab directory.

2. Install VirtualBox and Vagrant if you don't have them yet. Then, from the 
   langolab directory, type:

        vagrant up

    This creates a vm and provisions it. It builds redis and nodejs from 
    scratch, so sit back and have a nice cool drink.