%define name            api-installer
%define release         1

%define SCRIPT_NAME     api-install
%define TEMPL_NAME		api.initd.template
%define CRON_SCRIPT		cron-list-apis
%define UNINSTALL_SCRIPT_NAME     api-uninstall
%define DISPLAY_VERSION %{version}-b%{?BUILD_NUMBER}


Summary:        Java API environment builder
Name:           %{name}
Version:        %{version}
Release:        %{?BUILD_NUMBER}
Epoch:          0
Group:          Data/Template
License:        Proprietary
BuildArch:      noarch
Source0:        %{SCRIPT_NAME}
Source1:        %{TEMPL_NAME}
Source2:        %{CRON_SCRIPT}
Source3:        %{UNINSTALL_SCRIPT_NAME}
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}

%description
Java API environment builder

%prep
sed -i 's/$(build_version)/%{DISPLAY_VERSION}/' %{SOURCE0}
sed -i 's/$(build_version)/%{DISPLAY_VERSION}/' %{SOURCE1}
sed -i 's/$(build_version)/%{DISPLAY_VERSION}/' %{SOURCE2}
sed -i 's/$(build_version)/%{DISPLAY_VERSION}/' %{SOURCE3}

%install
rm -rf %{buildroot}

# Create directories
[ ! -d %{buildroot}/etc/%{name} ] && mkdir -p %{buildroot}/etc/%{name}
[ ! -d %{buildroot}/usr/bin ] && mkdir -p %{buildroot}/usr/bin
[ ! -d %{buildroot}/var/apiservices ] && mkdir -p %{buildroot}/var/apiservices

# Add the script
cp %{SOURCE0} %{buildroot}/etc/%{name}

# Add the jar runner template 
cp %{SOURCE1} %{buildroot}/etc/%{name}

# Add script executed by cron
cp %{SOURCE2} %{buildroot}/etc/%{name}

# Add uninstall script. Do NOT add it to /usr/bin
cp %{SOURCE3} %{buildroot}/etc/%{name}

# add link
ln -s /etc/%{name}/%{SCRIPT_NAME} %{buildroot}/usr/bin/%{SCRIPT_NAME}


%pre
# create cron job if not created yet
if [[ $(crontab -l) =~ "/etc/%{name}" ]]; then
	echo "The cron job is already defined"
else
	CRON_EXPRESSION="* * * * * /etc/%{name}/%{CRON_SCRIPT} >/dev/null 2>&1"
	crontab -l | { cat; echo "$CRON_EXPRESSION"; } | crontab -
fi

%files
%defattr(0744,root,root,0744)
/etc/%{name}/%{UNINSTALL_SCRIPT_NAME}

%defattr(0755,root,root,0755)
/etc/%{name}/%{SCRIPT_NAME}
/etc/%{name}/%{TEMPL_NAME}
/etc/%{name}/%{CRON_SCRIPT}
/usr/bin/%{SCRIPT_NAME}

%defattr(0664,root,root,2775)
/var/apiservices
