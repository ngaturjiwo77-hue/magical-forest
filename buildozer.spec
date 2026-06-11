[app]
title = Magical Forest
package.name = magicalforest
package.domain = org.dustin
source.dir = .
source.include_exts = py,png,jpg,ttf
version = 0.1
requirements = pygame,sdl2,sdl2_ttf,sdl2_image,sdl2_mixer
orientation = portrait
fullscreen = 1
android.permissions = INTERNET
android.api = 33
android.minapi = 21
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True
android.accept_sdk_license = True
android.ndk = 25b
android.ndk_api = 21

[buildozer]
log_level = 2
p4a.branch = master
# Kita gunakan versi Python yang paling cocok dengan NDK r25b
p4a.python_version = 3.10
