# Expects parameter:
#    VERSION=0.16
#    RELEASE_URL=Path to release to Nexus
# Clean up and create directories
for dir in BUILD RPMS SOURCES SPECS SRPMS
do
 [[ -d $dir ]] && rm -Rf $dir
  mkdir $dir
done

# Put our files in the right place
mv api-install SOURCES/.
mv api.initd.template SOURCES/.
mv cron-list-apis SOURCES/.
mv api.installer.spec SPECS/.
mv api-uninstall SOURCES/.

# Create rpm in RPMS/noarch/
rpmbuild --define '_topdir '`pwd` --define 'BUILD_NUMBER '$BUILD_NUMBER -ba -D "version "$VERSION SPECS/api.installer.spec

RPMFILE=api-installer-$VERSION-$BUILD_NUMBER.noarch.rpm

# pass a variable to the rest of build steps
echo "RPMFILE=$RPMFILE" > env_rpmfile.txt

#upload rpm to Nexus
if [[ $uploadToNexus == true ]]; then
  curl -v -u $USERNAME:$PASSWORD --upload-file RPMS/noarch/$RPMFILE $RELEASE_URL/api-installer/$VERSION/$RPMFILE
fi  