# Release process for new container version

 - All unit tests passed
 - Commit and push all changes (to master branch)
 - run codefreshRelease.sh this will:
   - Increment version
   - tag git repo with that version number
   - push repo and tags to git
   - codefresh will see new tag and start pipeline
   - Builds an image, tests it and pushes it to dockerhub
 - Deploy new container to metcarob.com with name virtualpresencepicture_VERSION
 - Add Kong upstream for new container with 0%
 - Switch kong test endpoint to new container (Any old endpoint removed)
 - make sure test endpoint is working
 - Switch kong upstreams from current to new
 - make sure production endpoint is working
 - delete old upstream
 - stop old container version

