[app]
title = Magical Forest
package.name = magicalforest
package.domain = org.dustin
source.dir = .
source.include_exts = py,png,jpg,ttf
version = 0.1
requirements = python3,kivy
orientation = portrait
fullscreen = 1
android.permissions = INTERNET
android.api = 33
android.minapi = 21
android.archs = arm64-v8a, armeabi-v7a

[buildozer]
log_level = 2
# Gunakan dist terbaru yang kompatibel dengan Ubuntu 24.04/22.04
p4a.branch = master
