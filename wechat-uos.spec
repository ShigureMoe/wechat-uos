%global _missing_build_ids_terminate_build 0
%global debug_package %{nil}
%define __requires_exclude libnode\.so|libffmpeg\.so
Name:wechat-uos 
Version: 2.0.0
Release: 3%{?dist}
Summary: UOS Wechat
License: MIT
URL: https://www.chinauos.com/resource/download-professional
Source0: %{name}.tar.gz
BuildArch: x86_64
BuildRequires: ImageMagick
Requires: gtk2 gtk3 libXss.so.1 GConf2 nss bubblewrap

%description
UOS Wechat 

%prep
%setup -qn %{name}
echo "Decompressing Debian Package..."
tar -xf data.tar.xz
echo "Patching Incorrect Size Icons..."
for s in 128 64 48 16; do
    newsize="${s}x${s}"
    echo "Downsampling from 256x256 to $newsize..."
    convert -geometry $newsize \
        opt/apps/com.qq.weixin/entries/icons/hicolor/256x256/apps/wechat.png \
        opt/apps/com.qq.weixin/entries/icons/hicolor/$newsize/apps/wechat.png
done


%build

%install
echo "Copying Application Binaries..."
%{__mkdir_p} %{buildroot}/opt/wechat-uos
%{__cp} -r opt/apps/com.qq.weixin/files/* %{buildroot}/opt/wechat-uos
install -Dm644 usr/lib/license/libuosdevicea.so -t %{buildroot}/usr/lib/license/

echo "Copying Patched Icons..."
%{__mkdir_p} %{buildroot}/usr/share/icons
%{__cp} -r opt/apps/com.qq.weixin/entries/icons/hicolor %{buildroot}/usr/share/icons/

echo "Linking Binaries..."
%{__mkdir_p} %{buildroot}/%{_bindir}/
install -Dm755 wechat-uos -t %{buildroot}/%{_bindir}/

echo "Creating Desktops and Hacks..."
%{__mkdir_p} %{buildroot}/opt/wechat-uos/crap/
%{__mkdir_p} %{buildroot}/usr/share/applications/
install -Dm644 uos-lsb uos-release -t %{buildroot}/opt/wechat-uos/crap/
install -Dm644 wechat-uos.desktop -t %{buildroot}/usr/share/applications/

%files
%{_bindir}/*
/opt/wechat-uos/*
/usr/share/applications/*
/usr/share/icons/*
/usr/lib/license/*


%changelog
* Thu Apr 01 2021 KleeMoe <feng591892871@gmail.com> - 2.0.0-3
Remove dependencies libnode.so libffmpeg.so

* Tue Mar 30 2021 KleeMoe <feng591892871@gmail.com> - 2.0.0-2
Migrate From AUR
