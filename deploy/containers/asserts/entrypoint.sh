#!/bin/sh

if [[ -z ${REVIEW} ]]; then
	export FI_ENVIRONMENT=fluidattacks.com/integrates
else
	export FI_ENVIRONMENT="$BRANCH.integrates.env.fluidattacks.com"
fi
sed -i 's#$FI_ENVIRONMENT#'"$FI_ENVIRONMENT"'#g' /exploit.py

python /exploit.py
retval=$?
curl -u ${USER}:${PASS} -T /tmp/fluidasserts.log https://fluid.jfrog.io/fluid/generic/fluidasserts_${ORG}_${APP}_$(date +%Y%m%d%H%M%S).log
exit $retval
