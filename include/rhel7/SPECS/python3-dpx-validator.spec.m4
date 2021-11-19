# vim:ft=spec
%define file_prefix M4_FILE_PREFIX
%define file_ext M4_FILE_EXT

%define file_version M4_FILE_VERSION
%define file_release_tag %{nil}M4_FILE_RELEASE_TAG
%define file_release_number M4_FILE_RELEASE_NUMBER
%define file_build_number M4_FILE_BUILD_NUMBER
%define file_commit_ref M4_FILE_COMMIT_REF

Name:           python3-dpx-validator
Version:        %{file_version}
Release:        %{file_release_number}%{file_release_tag}.%{file_build_number}.git%{file_commit_ref}%{?dist}
Summary:        Python validator for DPX files
Group:          Development/Tools
License:        LGPLv3+
URL:            https://www.csc.fi/
Source0:        %{file_prefix}-v%{file_version}%{?file_release_tag}-%{file_build_number}-g%{file_commit_ref}.%{file_ext}
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

Requires:       python3 python36-six
BuildRequires:  python3-setuptools

%description
Python validator for DPX files

%prep
%setup -n %{file_prefix}-v%{file_version}%{?file_release_tag}-%{file_build_number}-g%{file_commit_ref}

%build

%install
rm -rf $RPM_BUILD_ROOT
%{__python3} setup.py install -O1 --root $RPM_BUILD_ROOT --record=INSTALLED_FILES.in
cat INSTALLED_FILES.in | sed 's/^/\//g' >> INSTALLED_FILES
rm INSTALLED_FILES.in

# Rename executable to prevent name collision with Python 2 RPM
sed -i 's/\/bin\/dpxv$/\/bin\/dpxv-3/g' INSTALLED_FILES

mv %{buildroot}%{_bindir}/dpxv %{buildroot}%{_bindir}/dpxv-3

%post

%clean
rm -rf $RPM_BUILD_ROOT

%files -f INSTALLED_FILES
%defattr(-,root,root,-)

# TODO: For now changelog must be last, because it is generated automatically
# from git log command. Appending should be fixed to happen only after %changelog macro
%changelog
