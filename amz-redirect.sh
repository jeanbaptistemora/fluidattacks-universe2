PATTERN="output"
PATTERN2="/index.html"

for FILE in $(find output -iname '*.html'); do
	STRING=${FILE/$PATTERN/}
	NAME=${STRING/$PATTERN2/}
	if [[ ! $NAME = *".html" ]]; then
		aws s3api put-object --acl public-read-write \
		--bucket $S3_BUCKET --key $NAME --content-type text/html \
		--website-redirect-location "$NAME/"
	fi;	
done