#!/bin/sh
set -e
GITLAB_TEAM=gruifor-team
GITLAB_PROJECT=hyventaminen-backend

docker login registry.gitlab.com
docker build -t registry.gitlab.com/${GITLAB_TEAM}/${GITLAB_PROJECT} .
docker push registry.gitlab.com/${GITLAB_TEAM}/${GITLAB_PROJECT}
