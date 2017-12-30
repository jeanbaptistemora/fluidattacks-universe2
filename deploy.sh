if [ "$EUID" -ne 0 ];then
	echo "Please run as root"
	exit
else
	echo "Deploying FLUID Website (local environment)"
	echo ""
	
	echo "Verifying content (1/5) . . ."
	cd ./content
	if egrep -r 'Fluid|Fluidsignal\ Group|fluidsignal'; then echo "El único nombre aceptado es FLUID"; exit 1; fi
	cd ..
	
	echo "Removing older builds (2/5) . . ."
	rm -rf ./output
	
	echo "Generating build (3/5) . . ."
	sed -i 's/https/http/g' pelicanconf.py
	sed -i 's/fluid.la/localhost:8000/g' pelicanconf.py
	
	pelican --fatal errors content/
	if [ $? == 0 ];then
	
		mv output/web/en/blog-en output/web/en/blog && mv output/web/es/blog-es output/web/es/blog
		
		echo "Updating sitemap (4/5) . . ."
		./xmlcombine.sh
		mv output/web/en/redirect/index.html output/web/ && rmdir output/web/en/redirect/

		echo "Starting local HTTP server on port 8000 (5/5) . . ."
		cd ./output
		python -m SimpleHTTPServer
		cd ..
		git checkout -- pelicanconf.py
	else
		echo "Build error! Fix it and try again."
	fi
fi